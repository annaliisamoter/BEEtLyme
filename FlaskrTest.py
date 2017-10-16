import os
import unittest
from server import app
from model import *
from flask import json, jsonify


class FlaskTests(unittest.TestCase):
    """Testing of BEEtLyme app routes, both functional and unittest."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        connect_to_db(app, "postgresql:///beetlyme_test")
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_homepage(self):
        """tests homepage"""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn('Allowing those treating', result.data)

    def test_login(self):
        """Tests login route posting, redirect to profile page."""
        result = self.client.post("/login", data={ 
                                    "email": "annabelle@gmail.com",
                                    "password": "password123",
                                    }, follow_redirects=True)
        self.assertIn("Welcome", result.data)

    def test_register(self):
        """tests render profile page"""
        result = self.client.get("/register")
        self.assertEqual(result.status_code, 200)
        self.assertIn('New User', result.data)

    def test_register_post(self):
        result = self.client.post("/register", data={
                                    'fname': 'Annabelle',
                                    'lname': 'Akkerman',
                                    'email': 'annabelle@gmail.com',
                                    'password': 'password123'},
                                    follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn('User Login', result.data)

    def test_set(self):
        """Tests the rendering of '/set'."""
        result = self.client.get("/set")
        self.assertEqual(result.status_code, 200)
        self.assertIn('Set a new', result.data)

    def test_track(self):
        """Tests the rendering of '/track'."""
        result = self.client.get("/track")
        self.assertEqual(result.status_code, 200)
        self.assertIn('Track your Symptoms', result.data)

    def test_graph_options(self):
        """Tests rending of graph_options page."""
        result = self.client.get("/graph_options")
        self.assertEqual(result.status_code, 200)
        self.assertIn('Graphing options', result.data)

    def test_auto_symptom(self):
        """tests json app route returning json of all symptom names in db."""
        result = self.client.get("/auto_symptom")
        data = json.loads(result.data)
        self.assertEqual(data[0], 'Fever')

    def test_auto_treatment(self):
        """test json app route returning json of all treatment names in db."""
        result = self.client.get("/auto_treatment")
        data = json.loads(result.data)
        self.assertEqual(data[0], 'Bee Venom')

    def test_set_symptom(self):
        """Tests setting symptom for user to track in db."""
        result = self.client.post("/set_symptom", data={
                                    "symp": "Fever",
                                    "user_id": "1"})
        self.assertIn("You are already tracking", result.data)

    def test_set_symptom(self):
        """Tests setting symptom for user to track in db."""
        result = self.client.post("/set_symptom", data={
                                "symp": "Sweats, Chills",
                                "user_id": "1"})
        self.assertIn("Your symptom option, Sweats, Chills", result.data)

    def test_set_treatment(self):
        """Tests setting treatment for user to track in db."""
        result = self.client.post("/set_treatment", data={
                                    "treat": "Bee Venom",
                                    "user_id": "1"})
        self.assertIn("You are already tracking", result.data)

    def test_set_treatment(self):
        """Tests setting treatment for user to track in db."""
        result = self.client.post("/set_treatment", data={
                                    "treat": "Vit C",
                                    "user_id": "1"})
        self.assertIn("Your treatment option, Vit C", result.data)

    def test_track_symptom(self):
        """Tests inputting user values to symptom to db."""
        result = self.client.post("/track_symptoms", data={
                                    'user': '1',
                                    'date': '2017-09-11',
                                    'symptoms': {'Fever': '8'}
                                    })
        self.assertIn("Your symptoms have been logged")


def example_data():
    """data for test db beetlyme_test"""
    created_at = '2017-09-01'
    user = User(fname='Annabelle',
                lname='Akkerman',
                email='annabelle@gmail.com',
                password='password123',
                created_at='2017-09-01')

    db.session.add(user)
    symptom = Symptom(name="Fever", created_at=created_at)
    db.session.add(symptom)
    treatment = Treatment(name='Bee Venom', created_at=created_at)
    db.session.add(treatment)
    user_symptom = UserSymptom(user_id=1, symptom_id=1, created_at=created_at)
    db.session.add(user_symptom)
    user_treatment = UserTreatment(user_id=1, treatment_id=1, created_at=created_at)
    db.session.add(user_treatment)
    symptom_entry_1 = SymptomEntry(user_symp_id=1, value=6, created_at=created_at)
    symptom_entry_2 = SymptomEntry(user_symp_id=1, value=5, created_at='2017-09-03')
    symptom_entry_3 = SymptomEntry(user_symp_id=1, value=4, created_at='2017-09-06')
    symptom_entry_4 = SymptomEntry(user_symp_id=1, value=3, created_at='2017-09-09')
    symptom_entry_5 = SymptomEntry(user_symp_id=1, value=3, created_at='2017-09-20')
    db.session.add(symptom_entry_1)
    db.session.add(symptom_entry_2)
    db.session.add(symptom_entry_3)
    db.session.add(symptom_entry_4)
    db.session.add(symptom_entry_5)

    treatment_entry_1 = TreatmentEntry(user_treat_id=1, value=10, created_at=created_at)
    treatment_entry_2 = TreatmentEntry(user_treat_id=1, value=10, created_at='2017-09-03')
    treatment_entry_3 = TreatmentEntry(user_treat_id=1, value=10, created_at='2017-09-06')
    treatment_entry_4 = TreatmentEntry(user_treat_id=1, value=10, created_at='2017-09-09')
    treatment_entry_5 = TreatmentEntry(user_treat_id=1, value=10, created_at='2017-09-20')
    db.session.add(treatment_entry_1)
    db.session.add(treatment_entry_2)
    db.session.add(treatment_entry_3)
    db.session.add(treatment_entry_4)
    db.session.add(treatment_entry_5)

    full_moon = FullMoon(full_moon_date="2017-09-06")
    db.session.add(full_moon)
    new_moon = NewMoon(new_moon_date="2017-09-20")
    db.session.add(new_moon)

    db.session.commit()


class FlaskTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        # Connect to test database
        connect_to_db(app, "postgresql:///beetlyme_test")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    # def test_some_db_thing(self):
    #     """Some database test..."


if __name__ == '__main__':
    unittest.main()
