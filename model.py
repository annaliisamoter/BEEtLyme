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
    password = db.Column(db.String(16), nullable=False)
    created_at = db.Column(db.Datetime), nullable=False)
    updated_at = db.Column(db.Datetime), nullable=True)
    deleted_at = db.Column(db.Datetime), nullable=True)

    def __repr__(self):
        """Provides useful printed representation"""
        return "<User user_id=%s user name=%s %s" % (self.user_id, self.fname, self.lname)

class Symptom(db.Model):
    """defines Symptom model"""

    __tablename__ = "symptoms"

    symptom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.Datetime), nullable=False)
    updated_at = db.Column(db.Datetime), nullable=True)
    deleted_at = db.Column(db.Datetime), nullable=True)

class Treatment(db.Model):
    """defines Treatment model"""

    __tablename__ = "treatments"

    treatment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.Datetime), nullable=False)
    updated_at = db.Column(db.Datetime), nullable=True)
    deleted_at = db.Column(db.Datetime), nullable=True)






if __name__ == "__main__":

    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."