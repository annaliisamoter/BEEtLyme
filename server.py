from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Symptom, Treatment, UserSymptom, Comments
from model import UserTreatment, SymptomEntry, TreatmentEntry, FullMoon, NewMoon
import helper
import json
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    
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
    pw_hash = bcrypt.generate_password_hash(password)
    print pw_hash

    q = db.session.query(User).filter(User.email == email).all()

    if q:
        print "user already exists"
        flash("User already exists")
        return redirect('/login')

    else:
        new_user = User(fname=fname, lname=lname, email=email, password=pw_hash)
        db.session.add(new_user)
        db.session.commit()
        print "new user has been added to the database"
        flash("Welcome to BEEtLyme!")
        return render_template('/login.html')


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

    if 'user_id' in session and q.user_id == session['user_id']:
        flash("You are already logged in")
        return redirect('profile')


    elif q and bcrypt.check_password_hash(q.password, password):
        #formerly written as q.password == password without the bcrypt
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
    flash("You have logged out.  Come back soon!")

    return redirect("/")


@app.route('/profile')
def show_profile():
    """Displays profile page of logged in user"""
    if session['user_id']:
        u = session['user_id']

        q = User.query.get(u)
        q.comments
        symptoms = q.user_symptom
        treatments = q.user_treatment
        entries = Comments.query.filter(Comments.user_id == u).order_by(Comments.created_at.desc()).all()

        print "These are the journal entries on file:", entries

        return render_template('/profile.html', user=q, symptoms=symptoms, treatments=treatments, entries=entries)

    else:
        flash("You must be logged in to access this page")
        return redirect('/login')


@app.route('/update', methods=['POST'])
def update_user_info():
    """Allows user to update user info and reset password."""
    user = User.query.get(session['user_id'])
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    current_password = request.form.get('current-password')
    new_password = request.form.get('new-password')

    if not bcrypt.check_password_hash(user.password, current_password):
        flash("Current password does not match our records.  Changes not saved.")
        return redirect('/profile')

    else:
        pw_hash = bcrypt.generate_password_hash(new_password)
        user.password = pw_hash

        if fname:
            user.fname = fname
        if lname:
            user.lname = lname
        if email:
            user.email = email

        db.session.commit()
        flash("Your profile changes have been saved.")
        return redirect('/profile')


@app.route('/set', methods=["GET"])
def show_set_symptoms():
    """Shows set symptoms and treatments page"""

    return render_template('/set.html')


@app.route('/auto_symptom', methods=['GET'])
def set_auto_complete_symp():
    """Handles autocomplete ajax request"""

    symptoms = db.session.query(Symptom.name).all()
    options = [symptom.name for symptom in symptoms]

    return jsonify(options)


@app.route('/set_symptom', methods=["POST"])
def set_new_symptom():
    """Adds a user-generated symptom to the user_symptom table.
        If not already there, also creates new Symptom and adds to symptoms table.
    """

    symptom = request.form.get("symp")
    symptom = symptom.title()
    print "Symptom captured from set-symptom form is", symptom

    user = session['user_id']
    symptoms_master_list = db.session.query(Symptom.name).all()
    user_symptoms = db.session.query(UserSymptom).filter(UserSymptom.user_id == user).all()
    user_symptom_names = [symptoms.symptom.name for symptoms in user_symptoms]

    if symptom in user_symptom_names:
        print symptom, "not added to db. Already tracking."
        return "You are already tracking that symptom."

    for symp in symptoms_master_list:
        # checking if symptom is already in master db of symptoms
        if symptom in symp:
            symptom = Symptom.query.filter_by(name=symptom).first()
            user_symptom = UserSymptom(symptom_id=symptom.symptom_id, user_id=user)
            db.session.add(user_symptom)
            print
            print "Existing Symptom: ", symptom.name, ", added to user_symptom db."
            break
    # if brand new symptom, also adding to symptom table
    else:
        symptom = Symptom(name=symptom)
        db.session.add(symptom)
        symptom_id = db.session.query(Symptom.symptom_id).filter_by(name=symptom.name)
        user_symptom = UserSymptom(symptom_id=symptom_id, user_id=user)
        db.session.add(user_symptom)
        print
        print "New Symptom: ", symptom.name, ", added to symptom and user_symptom db."

    db.session.commit()

    return "Your symptom option, {}, has been added to your profile.".format(symptom.name)



@app.route('/auto_treatment', methods=['GET'])
def set_auto_complete_treat():
    """Handles autocomplete ajax request"""

    treatments = db.session.query(Treatment.name).all()
    options = [treatment.name for treatment in treatments]

    return jsonify(options)


@app.route('/set_treatment', methods=["POST"])
def set_new_treatment():
    """Adds a user-generated treatment to the user_treatment table.
        If not already there, also creates new Treatment and adds to symptoms table.
    """

    treatment = request.form.get("treat")
    treatment = treatment.title()
    print "Treatment captured from set-treatment form is", treatment
    user = session['user_id']
    treatments_master_list = db.session.query(Treatment.name).all()
    user_treatments = db.session.query(UserTreatment).filter(UserTreatment.user_id == user).all()
    user_treatment_names = [treatments.treatment.name for treatments in user_treatments]
    print "This is the list of treatment names already being tracked:", user_treatment_names

    if treatment in user_treatment_names:
        print treatment, "not added to db. Already tracking."
        return "You are already tracking that treatment."

    for treat in treatments_master_list:
        #checks if treatment is already in db
        if treatment in treat:
            treatment = Treatment.query.filter_by(name=treatment).first()
            user_treatment = UserTreatment(treatment_id=treatment.treatment_id, user_id=user)
            db.session.add(user_treatment)
            print
            print "Existing Treatment: ", treatment.name, ", added to user_treatment db."
            break
    # if brand new treatment, adds to master treatments table
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

    return "Your treatment option, {}, has been added to your profile.".format(treatment.name)


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
    date = request.form.get("date")
    symptoms = request.form.items()
    print "This is the symp values:", symptoms
    print "This is the date captured:", date

    for key, value in symptoms:
        if key == "date":
            continue
        else:
            print key, value
            symptom_name = key
            symptom_id = db.session.query(Symptom.symptom_id).filter(
                                            Symptom.name == symptom_name).first()
            score = int(value)
            user_symp_id = db.session.query(UserSymptom.user_symp_id).filter(
                                                    UserSymptom.user_id== user,
                                                    UserSymptom.symptom_id == symptom_id).first()
            #checks if there is already an entry for that date, if so updates value:
            possible_symptom_entry = SymptomEntry.query.filter(SymptomEntry.user_symp_id == user_symp_id, SymptomEntry.created_at == date).first()
            if possible_symptom_entry:
                possible_symptom_entry.value = value
            else:
                # Insert new SE into database
                symptom_entry = SymptomEntry(user_symp_id=user_symp_id, value=score, created_at=date)
                db.session.add(symptom_entry)

    db.session.commit()
    return "Your symptom input has been logged."



@app.route('/track_treatments', methods=["POST"])
def add_treatment_entries():
    """Takes in the values given by the user for symptoms and adds entries to
        symptom_entries table.
    """

    user = session['user_id']
    date = request.form.get("date")
    treatments = request.form.items()
    print "This is from the treatment request.form: ", treatments

    for key, value in treatments:
        if key == 'date':
            continue
        else:
            print key, value
            treatment_name = key
            treatment_id = db.session.query(Treatment.treatment_id).filter(
                                            Treatment.name == treatment_name).first()
            score = int(value)
            user_treat_id = db.session.query(UserTreatment.user_treat_id).filter(
                                            UserTreatment.user_id == user,
                                            UserTreatment.treatment_id == treatment_id).first()
            #checks if there is already a treatment entry for that date, if so updates value.
            possible_treatment_entry = TreatmentEntry.query.filter(TreatmentEntry.user_treat_id == user_treat_id, TreatmentEntry.created_at == date).first()
            if possible_treatment_entry:
                possible_treatment_entry.value = value
            else:
                treatment_entry = TreatmentEntry(user_treat_id=user_treat_id, value=score, created_at=date)
                db.session.add(treatment_entry)

    db.session.commit()
    return "Your treatment input has been logged."


@app.route('/log_comment', methods=["POST"])
def lof_comment():
    """Logs user comment to database in comments table."""
    user_id = session['user_id']
    date = request.form.get("date")
    print "This is the date for the comment:", date
    comment = request.form.items()
    print "This is the form input for the comment route:", comment

    for key, value in comment:
        if key == 'date':
            continue
        else:
            print key, value
            comment = value
            possible_journal_entry = Comments.query.filter(Comments.user_id == user_id, Comments.created_at == date).first()
            if possible_journal_entry:
                possible_journal_entry.comment = comment
                print "User comment has been updated for existing date:", date
            else:
                user_comment = Comments(user_id=user_id, comment=comment, created_at=date)
                db.session.add(user_comment)
                print "following user comment has been added to database:", comment
    db.session.commit()
    return "Your journal entry has been saved."


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


@app.route('/graph_data.json', methods=['GET'])
def assemble_graph_data():
    """queries db and properly formats a json to seed graph data."""

    user_id = session['user_id']
    symptom_options = request.args.get('symptom_options')
    treatment_option = request.args.get('treatment_option')
    print "graph_options from inside graph_data route", symptom_options[0], treatment_option
    symptom_options = json.loads(symptom_options)
    treatment_option = json.loads(treatment_option)

    total_data = {'data': []}
    # create trace_data for symptoms and add to total_data
    if len(symptom_options) > 1:
        for option in symptom_options:
            trace_data = helper.plotly_helper_symp(option, user_id)
            total_data['data'].append(trace_data)
    else:
        total_data['data'].append(helper.plotly_helper_symp(symptom_options[0], user_id))
    # create trace_data for treatment and add to total_data
    total_data['data'].append(helper.plotly_helper_treat(treatment_option, user_id))

    #add full moon and new moon traces to the total_data set:
    date_range = helper.get_date_range(total_data)
    print date_range
    total_data['date_range'] = date_range
    total_data['data'].append(helper.full_moon_phase_overlay(date_range))
    total_data['data'].append(helper.new_moon_phase_overlay(date_range))

    return jsonify(total_data)


if __name__ == "__main__":  #pragma: no cover
    #app.debug = True
    #app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)  #pragma
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")  
