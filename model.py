"""Models and db for BEEtLyme Project"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class User(db.Model):
    """defines User model"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.Datetime, nullable=False)
    deleted_at = db.Column(db.Datetime, nullable=True)

    def __repr__(self):
        """Provides useful printed representation"""
        return "<User user_id=%s user name=%s %s" % (self.user_id, self.fname, self.lname)


class Symptom(db.Model):
    """defines Symptom model"""

    __tablename__ = "symptoms"

    symptom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.Datetime, nullable=False)
    deleted_at = db.Column(db.Datetime, nullable=True)

    def __repr__(self):
        """Provides useful printed representation"""
        return "<Symptom symptom_id=%s symptom name=%s" % (self.symptom_id, self.name)


class Treatment(db.Model):
    """defines Treatment model"""

    __tablename__ = "treatments"

    treatment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.Datetime, nullable=False)
    deleted_at = db.Column(db.Datetime, nullable=True)

    def __repr__(self):
        """Provides useful printed representation"""
        return "<Symptom symptom_id=%s symptom name=%s" % (self.treatment_id, self.name)


class UserSymptom(db.Model):
    """defines User-Symptom model, associating users and symptoms"""

    __tablename__ = "user-symptoms"

    user_symp_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True, )
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.symptom_id'),
                                                    nullable=False, index=True)
    created_at = db.Column(db.Datetime, nullable=False)
    deleted_at = db.Column(db.Datetime, nullable=True)

    user = db.relationship("User", backref=db.backref("user_symptom"))
    symptom = db.rlationship("Symptom", backref=db.backref("user_symptom"))

    def __repr__(self):
        """Provides useful printed representation"""
        return "<UserSymptom %s pairs user %s with symptom %s" % (
                        self.user_symp_id, self.user.fname, self.symptom.name)


class UserTreatment(db.Model):
    """defines UserTreatment model, associating users and treatments"""

    __tablename__ = "user-treatments"

    user_treat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                                                   nullable=False, index=True)
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.treatment_id'),
                                                    nullable=False, index=True)
    created_at = db.Column(db.Datetime, nullable=False)
    deleted_at = db.Column(db.Datetime, nullable=True)

    user = db.relationship("User", backref=db.backref("user_treatment"))
    treatment = db.relationship("Treatment", backref=db.backref("user_treatment"))

    def __repr__(self):
        """Provides useful printed representation"""
        return "<UserTreatment %s pairs user %s with treatment %s" % (
                        self.user_treat_id, self.user.fname, self.treatment.name)


class SymptomEntry(db.Model):
    """defines model for SymptomEntry storing user data for tracking symptom"""

    __tablename__ = "symptom-entries"

    entry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_symp_id = db.Column(db.Integer, db.ForeignKey('user-symptoms.user_symp_id'),
                                                    nullable=False, index=True)
    value = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.Datetime, nullable=False)
    updated_at = db.Column(db.Datetime, nullable=True)
    deleted_at = db.Column(db.Datetime, nullable=True)

    user_symp = db.relationship("UserSymptom", backref=db.backref("symptom_entry"))

    def __repr__(self):
        """Provides useful printed representation"""
        return "<SymptomEntry %s declared %s as value %s" % (
                        self.entry_id, self.user_symp.symptom.name, self.value)

        #can we jump through several relationships like this in the repr? ^^

class TreatmentEntry(db.Model):
    """defines model for TreatmentEntry storing user data for tracking treatment"""

    __tablename__ = "treatment-entries"

    entry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_treat_id = db.Column(db.Integer, db.ForeignKey('user-treatments.user_treat_id'),
                                                    nullable=False, index=True)
    value = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.Datetime, nullable=False)
    updated_at = db.Column(db.Datetime, nullable=True)
    deleted_at = db.Column(db.Datetime, nullable=True)

    user_treat = db.relationship("UserSymptom", backref=db.backref("treatment_entry"))

    def __repr__(self):
        """Provides useful printed representation"""
        return "<TreatmentEntry %s declared %s as value %s" % (
                        self.entry_id, self.user_treat.treatment.name, self.value)

class Comments(db.Model):
    """defines Comment model of user entry of a daily comment"""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                                                    nullable=False, index=True)
    comment = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.Datetime, nullable=False)
    updated_at = db.Column(db.Datetime, nullable=True)
    deleted_at = db.Column(db.Datetime, nullable=True)



if __name__ == "__main__":

    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
