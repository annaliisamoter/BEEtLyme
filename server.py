from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Symptom, Treatment, UserSymptom
from model import UserTreatment, SymptomEntry, TreatmentEntry



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
    """ renders registration form """

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def register_process():
    """ checks if user is registered, if not adds new user to database """

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
    """ return login page """

    return render_template('login.html')


@app.route('/login', methods=["POST"])
def login_process():
    """ validate email & pass & stores in session """
    email = request.form.get("email")
    password = request.form.get("password")

    q = db.session.query(User).filter(User.email == email).first()

    if q and q.password == password:
        print q, q.password
        session['user_id'] = q.user_id
        session['logged_in'] = True
        flash("You are logged in!")
        print "login success"
        return redirect('/profile')

    else:
        flash("Your email or password do not match our records, please try again")
        print "login failed"
        return redirect('/login')


@app.route('/logout')
def log_out():
    """logs a user out"""
    session['user_id'] = None
    session['logged_in'] = False

    return redirect("/")


@app.route('/profile')
def show_profile():
    """displays profile page of logged in user"""

    if session['user_id']:
        u = session['user_id']
        q = User.query.filter(User.user_id == u).first()
        symptoms = q.user_symptom
        #list of symptom objects
        treatments = q.user_treatment

        return render_template('/profile.html', user=q, symptoms=symptoms, treatments=treatments)

    else:
        flash("You must be logged in to access this page")
        return redirect('/login')

@app.route('/set_symptom', methods=["GET"])
def show_set_symptoms():
    """Shows set symptoms page"""

    return render_template('/set_symptom.html')


@app.route('/set_symptom', methods=["POST"])
def set_new_symptom():
    """Adds a user-generated symptom to the user_symptom table.
        If not already there, also created new Symptom and adds to symptoms table.
    """

    symptom = request.form.get("symptom")
    symptom = symptom.capitalize()
    print "Symptom captured from form is", symptom
    user = session['user_id']
    symptoms_master_list = db.session.query(Symptom.name).all()
    print

    for symp in symptoms_master_list:
        print symp

        if symptom in symp:
            symptom = Symptom.query.filter_by(name=symptom).first()
            user_symptom = UserSymptom(symptom_id=symptom.symptom_id, user_id=user)
            db.session.add(user_symptom)
            print
            print "Existing ", symptom.name, "added to user_symptom db."
            break

    else:
        symptom = Symptom(name=symptom)
        db.session.add(symptom)
        symptom_id = db.session.query(Symptom.symptom_id).filter_by(name=symptom.name)
        user_symptom = UserSymptom(symptom_id=symptom_id, user_id=user)
        db.session.add(user_symptom)
        print
        print "New ", symptom.name, " added to user_symptom db."

    db.session.commit()

    return redirect('/profile')



if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
