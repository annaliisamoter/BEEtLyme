from sqlalchemy import func
from model import User, Treatment, Symptom, connect_to_db, db
from model import UserTreatment, UserSymptom, SymptomEntry, TreatmentEntry, FullMoon, NewMoon
from server import app
from datetime import datetime


def load_users():
    """Load users from u.user into database."""

    print "Users"

    User.query.delete()

    for row in open("seed_data/u.fake-users.txt"):
        row = row.rstrip()
        fname, lname, email, password, created_at = row.split("|")

        user = User(fname=fname,
                    lname=lname,
                    email=email,
                    password=password,
                    created_at=created_at)

        db.session.add(user)

    db.session.commit()


def load_symptoms():
    """Load symptoms from u.symptoms into database."""

    print "Symptoms"

    Symptom.query.delete()

    for row in open("seed_data/u.symptoms"):
        row = row.rstrip().split("|")
        name = row[0]
        created_at = row[1]

        symptom = Symptom(name=name, created_at=created_at)
        db.session.add(symptom)

    db.session.commit()


def load_treatments():
    """Load treatments from u.treatments into database."""

    print "Treatments"

    Treatment.query.delete()

    for row in open("seed_data/u.treatments"):
        row = row.rstrip()
        name, created_at = row.split("|")

        treatment = Treatment(name=name, created_at=created_at)
        db.session.add(treatment)

    db.session.commit()

def load_user_symptoms():
    """Load fake user-symptoms from u.fake_user_symptoms into db."""

    print "User-Symptoms"

    UserSymptom.query.delete()

    for row in open("seed_data/u.fake_user_symptoms"):
        row = row.rstrip()
        user_id, symptom_id, created_at = row.split("|")

        user_symptom = UserSymptom(user_id=user_id, symptom_id=symptom_id,
                                                        created_at=created_at)
        db.session.add(user_symptom)

    db.session.commit()

def load_user_treatments():
    """load fake user-treatments from u.fake_user_treatments into db."""

    print "User-Treatments"

    UserTreatment.query.delete()

    for row in open("seed_data/u.fake_user_treatments"):
        row = row.rstrip()
        user_id, treatment_id, created_at = row.split("|")

        user_treatment = UserTreatment(user_id=user_id, treatment_id=treatment_id,
                                                        created_at=created_at)
        db.session.add(user_treatment)

    db.session.commit()

def load_fake_symptom_entries():
    """Load fake user treatment entries into db"""

    print "SymptomEntries"

    SymptomEntry.query.delete()

    for row in open("seed_data/u.fake_symptom_entries"):
        row = row.rstrip()
        user_symp_id, value, created_at = row.split("|")
        symptom_entry = SymptomEntry(user_symp_id=user_symp_id, value=value,
                                        created_at=created_at)
        db.session.add(symptom_entry)

    db.session.commit()


def load_fake_treatment_entries():

    print "TreatmentEntries"

    TreatmentEntry.query.delete()

    for row in open("seed_data/u.fake_treatment_entries"):
        row = row.rstrip()
        user_treat_id, value, created_at = row.split("|")
        treatment_entry = TreatmentEntry(user_treat_id=user_treat_id, value=value,
                                            created_at=created_at)
        db.session.add(treatment_entry)

    db.session.commit()


def load_full_moons():
    """Seeds FullMoon table in db"""
    print "FullMoon"

    #FullMoon.query.delete()

    for row in open("seed_data/moon_phases.txt"):
        row = row.rstrip()
        full_moon_date, new_moon = row.split("|")
        full_moon_date = datetime.strptime(full_moon_date, '%b %d, %Y')
        full_moon = FullMoon(full_moon_date=full_moon_date)
        db.session.add(full_moon)

    db.session.commit()


def load_new_moons():
    """Seeds NewMoon table in db"""
    print "NewMoon"

    #NewMoon.query.delete()

    for row in open("seed_data/moon_phases.txt"):
        row = row.rstrip()
        full_moon_date, new_moon = row.split("|")
        new_moon_date = datetime.strptime(new_moon, '%b %d, %Y')
        new_moon = NewMoon(new_moon_date=new_moon_date)
        db.session.add(new_moon)

    db.session.commit()




if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    #Import different types of data
    load_users()
    load_symptoms()
    load_treatments()
    load_user_symptoms()
    load_user_treatments()
    load_fake_symptom_entries()
    load_fake_treatment_entries()
    load_full_moons()
    load_new_moons()
