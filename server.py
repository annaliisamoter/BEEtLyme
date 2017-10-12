from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Symptom, Treatment, UserSymptom
from model import UserTreatment, SymptomEntry, TreatmentEntry, FullMoon, NewMoon
import helper
import json

app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    session['user_id'] = 1
    return render_template("homepage.html")


@app.route('/register', methods=["GET"])
def register_form():
    """ Renders registration form """

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def register_process():
    """ Checks if user is registered, if not adds new user to database """

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')

    q = db.session.query(User).filter(User.email == email).all()

    if q:
        print "user already exists"
        flash("User already exists")
        return redirect('/login')

    else:
        new_user = User(fname=fname, lname=lname, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        print "new user has been added to the database"
        flash("Welcome!")
        return render_template('/login')


@app.route('/login', methods=["GET"])
def login_display():
    """ Returns login page """

    return render_template('login.html')


@app.route('/login', methods=["POST"])
def login_process():
    """ Validates email & pass & stores in session """
    email = request.form.get("email")
    password = request.form.get("password")

    q = db.session.query(User).filter(User.email == email).first()

    if q.user_id == session['user_id']:
        flash("You are already logged in")
        print "User already logged in"
        return redirect('profile')

    elif q and q.password == password:
        print q, q.password
        session['user_id'] = q.user_id
        session['logged_in'] = True
        flash("Login successful. Welcome back.")
        print "login success"
        return redirect('/profile')

    else:
        flash("Your email or password do not match our records, please try again")
        print "login failed"
        return redirect('/login')


@app.route('/logout')
def log_out():
    """Logs a user out"""
    session['user_id'] = None
    session['logged_in'] = False
    flash("You have logged out.  Goodbye.")

    return redirect("/")


@app.route('/profile')
def show_profile():
    """Displays profile page of logged in user"""

    if session['user_id']:
        u = session['user_id']
        q = User.query.filter(User.user_id == u).first()
        symptoms = q.user_symptom
        treatments = q.user_treatment

        return render_template('/profile.html', user=q, symptoms=symptoms, treatments=treatments)

    else:
        flash("You must be logged in to access this page")
        return redirect('/login')


@app.route('/set_symptom', methods=["GET"])
def show_set_symptoms():
    """Shows set symptoms page"""

    return render_template('/set_symptom.html')


@app.route('/auto_symptom', methods=['GET'])
def set_auto_complete_symp():
    """Handles autocomplete ajax request"""
    print "this is printing from the auto_symptom app route"

    symptoms = db.session.query(Symptom.name).all()
    options = [symptom.name for symptom in symptoms]

    return jsonify(options)


@app.route('/set_symptom', methods=["POST"])
def set_new_symptom():
    """Adds a user-generated symptom to the user_symptom table.
        If not already there, also creates new Symptom and adds to symptoms table.
    """

    symptom = request.form.get("symptom")
    symptom = symptom.capitalize()
    print "Symptom captured from set-symptom form is", symptom

    user = session['user_id']
    symptoms_master_list = db.session.query(Symptom.name).all()
    user_symptoms = db.session.query(UserSymptom).filter(UserSymptom.user_id == user).all()
    user_symptom_names = [symptoms.symptom.name for symptoms in user_symptoms]

    # if symptom in user_symptom_names:
    #     flash("You are already tracking that symptom.")
    #     return redirect('/profile')

    # elif symptom not in user_symptom_names:
    for symp in symptoms_master_list:

        if symptom in symp:
            symptom = Symptom.query.filter_by(name=symptom).first()
            user_symptom = UserSymptom(symptom_id=symptom.symptom_id, user_id=user)
            db.session.add(user_symptom)
            print
            print "Existing Symptom: ", symptom.name, ", added to user_symptom db."
            break

    else:
        symptom = Symptom(name=symptom)
        db.session.add(symptom)
        symptom_id = db.session.query(Symptom.symptom_id).filter_by(name=symptom.name)
        user_symptom = UserSymptom(symptom_id=symptom_id, user_id=user)
        db.session.add(user_symptom)
        print
        print "New Symptom: ", symptom.name, ", added to user_symptom db."

    db.session.commit()

    return redirect('/profile')


@app.route('/set_treatment', methods=["GET"])
def show_set_treatment():
    """Shows set treatment page"""

    return render_template('/set_treatment.html')


@app.route('/auto_treatment', methods=['GET'])
def set_auto_complete_treat():
    """Handles autocomplete ajax request"""
    print "this is printing from the auto_symptom app route"

    treatments = db.session.query(Treatment.name).all()
    options = [treatment.name for treatment in treatments]

    return jsonify(options)


@app.route('/set_treatment', methods=["POST"])
def set_new_treatment():
    """Adds a user-generated treatment to the user_treatment table.
        If not already there, also creates new Treatment and adds to symptoms table.
    """

    treatment = request.form.get("treatment")
    treatment = treatment.capitalize()
    print "Treatment captured from set-treatment form is", treatment
    user = session['user_id']
    treatments_master_list = db.session.query(Treatment.name).all()
    user_treatments = db.session.query(UserTreatment).filter(UserTreatment.user_id == user).all()
    user_treatment_names = [treatments.treatment.name for treatments in user_treatments]

    # if treatment in user_treatment_names:
    #     flash("You are already tracking that treatment.")
    #     return redirect('/profile')

    # elif treatment not in user_treatment_names:
    for treat in treatments_master_list:

        if treatment in treat:
            treatment = Treatment.query.filter_by(name=treatment).first()
            user_treatment = UserTreatment(treatment_id=treatment.treatment_id, user_id=user)
            db.session.add(user_treatment)
            print
            print "Existing Treatment: ", treatment.name, ", added to user_treatment db."
            break

    else:
        treatment = Treatment(name=treatment)
        db.session.add(treatment)
        treatment_id = db.session.query(Treatment.treatment_id).filter_by(
                                                        name=treatment.name)
        user_treatment = UserTreatment(treatment_id=treatment_id, user_id=user)
        db.session.add(user_treatment)
        print
        print "New Treatment: ", treatment.name, ", added to user_treatment db."

    db.session.commit()

    return redirect('/profile')


@app.route('/track', methods=["GET", "POST"])
def show_track_symptoms():
    """Shows track page"""

    user = session['user_id']
    symptoms = UserSymptom.query.filter(UserSymptom.user_id == user).all()
    treatments = UserTreatment.query.filter(UserTreatment.user_id == user).all()

    return render_template('/track.html', symptoms=symptoms, treatments=treatments)


@app.route('/track_symptoms', methods=["POST"])
def add_symptom_entries():
    """Takes in the values given by the user for symptoms and adds entries to
        symptom_entries table.
    """

    user = session['user_id']
    symptoms = request.form.items()
    print "This is from the symptom request.form: ", symptoms

    for key, value in symptoms:
        print key, value
        symptom_name = key
        symptom_id = db.session.query(Symptom.symptom_id).filter(
                                        Symptom.name == symptom_name).first()
        score = int(value)
        user_symp_id = db.session.query(UserSymptom.user_symp_id).filter(
                                                UserSymptom.user_id== user,
                                                UserSymptom.symptom_id == symptom_id).first()
        symptom_entry = SymptomEntry(user_symp_id=user_symp_id, value=score)
        db.session.add(symptom_entry)

    db.session.commit()
    return "Your symptoms have been logged."


# @app.route('/track_treatments', methods=["GET"])
# def show_track_treatments():
#     """Shows track treatments page"""

#     user = session['user_id']
#     treatments = UserTreatment.query.filter(UserTreatment.user_id == user).all()

#     return render_template('/track_treatments.html', treatments=treatments)


@app.route('/track_treatments', methods=["POST"])
def add_treatment_entries():
    """Takes in the values given by the user for symptoms and adds entries to
        symptom_entries table.
    """

    user = session['user_id']
    treatments = request.form.items()
    print "This is from the treatment request.form: ", treatments

    for key, value in treatments:
        print key, value
        treatment_name = key
        treatment_id = db.session.query(Treatment.treatment_id).filter(
                                        Treatment.name == treatment_name).first()
        score = int(value)
        user_treat_id = db.session.query(UserTreatment.user_treat_id).filter(
                                        UserTreatment.user_id == user,
                                        UserTreatment.treatment_id == treatment_id).first()
        treatment_entry = TreatmentEntry(user_treat_id=user_treat_id, value=score)
        db.session.add(treatment_entry)

    db.session.commit()
    return "Your treatments have been logged."


@app.route('/graph_options', methods=["GET"])
def show_graph_options_page():
    """Shows the page where users can choose what to graph."""
    user = session['user_id']
    symptom_options = UserSymptom.query.filter(UserSymptom.user_id == user).all()
    treatment_options = UserTreatment.query.filter(UserTreatment.user_id == user).all()

    return render_template('/graph_options.html', symptom_options=symptom_options,
                                                treatment_options=treatment_options)


@app.route('/graph_options', methods=["POST"])
def get_graph_options():
    """Gets the symptoms the user wishes to track."""

    user = session['user_id']
    symptom_options = request.form.getlist('symptom')
    treatment_option = request.form.get('treatment')

    print "these are the graph options captured from user:", symptom_options, treatment_option

    return render_template('/chart_2.html', symptom_options=symptom_options,
                                        treatment_option=treatment_option)


@app.route('/graph_data', methods=['GET'])
def assemble_graph_data():
    """queries db and properly formats a json to seed graph data."""

    user_id = session['user_id']
    symptom_options = request.args.get('symptom_options')
    treatment_option = request.args.get('treatment_option')
    print "graph_options from inside graph_data route", symptom_options, treatment_option
    symptom_options = json.loads(symptom_options)
    treatment_option = json.loads(treatment_option)

    total_data = {'data': []}
    # create trace_data for symptoms and add to total_data
    if len(symptom_options) > 1:
        for option in symptom_options:
            trace_data = helper.plotly_helper_1(option, user_id)
            total_data['data'].append(trace_data)
    else:
        total_data['data'].append(helper.plotly_helper_1(symptom_options[0], user_id))
    # create trace_data for treatment and add to total_data
    total_data['data'].append(helper.plotly_helper_treat(treatment_option, user_id))

    #add full moon and new moon traces to the total_data set:
    date_range = helper.get_date_range(total_data)
    print date_range
    total_data['data'].append(helper.full_moon_phase_overlay(date_range))
    total_data['data'].append(helper.new_moon_phase_overlay(date_range))

    print total_data
    return jsonify(total_data)


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
