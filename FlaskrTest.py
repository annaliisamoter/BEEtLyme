import os
import unittest
from server import app
from model import *
from flask import json, jsonify
import helper


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


    def test_login_new(self):
        """Tests login route posting, redirect to profile page if user already logged in."""
        result = self.client.post("/login", data={
                                    "email": "bernadette@gmail.com",
                                    "password": "password456",
                                    }, follow_redirects=True)
        self.assertIn("Welcome", result.data)
        self.assertIn("Bernadette", result.data)

    def test_login_already(self):
        """Tests login route posting, redirect to profile page if user already logged in."""
        result = self.client.post("/login", data={
                                    "email": "annabelle@gmail.com",
                                    "password": "password123",
                                    }, follow_redirects=True)
        self.assertIn("Welcome", result.data)
        self.assertIn("Annabelle", result.data)
        self.assertIn("already logged in", result.data)

    def test_register(self):
        """tests render profile page"""
        result = self.client.get("/register")
        self.assertEqual(result.status_code, 200)
        self.assertIn('New User', result.data)

    def test_register_post_new_user(self):
        """tests register route for new user."""
        result = self.client.post("/register", data={
                                    'fname': 'Jane',
                                    'lname': 'Doe',
                                    'email': 'janedoe@gmail.com',
                                    'password': 'password123'})
        self.assertEqual(result.status_code, 200)
        self.assertIn('User Login', result.data)
        self.assertIn('Welcome!', result.data)

    def test_register_post_existing_user(self):
        """tests register route if user is already registered."""
        result = self.client.post("/register", data={
                                    'fname': 'Annabelle',
                                    'lname': 'Akkerman',
                                    'email': 'annabelle@gmail.com',
                                    'password': 'password123'},
                                    follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn('User Login', result.data)
        self.assertIn('User already exists', result.data)

    def test_logout(self):
        """Tests logout route"""
        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn("Goodbye", result.data)

    def test_profile_logged_in(self):
        """Tests rendering of profile page for logged in user."""
        result = self.client.get("/profile")
        self.assertIn("Journal Entries", result.data)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Fever", result.data)

    def test_profile_not_logged_in(self):
        """Tests the redirect if a user who is not logged in tries to access profile page."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = None
        result = self.client.get("/profile",
                                    follow_redirects=True)
        self.assertIn("You must be logged in", result.data)

    def test_set_render(self):
        """Tests the rendering of '/set'."""
        result = self.client.get("/set")
        self.assertEqual(result.status_code, 200)
        self.assertIn('Set a new', result.data)

    def test_track_render(self):
        """Tests the rendering of '/track'."""
        result = self.client.get("/track")
        self.assertEqual(result.status_code, 200)
        self.assertIn('Track your Symptoms', result.data)

    def test_graph_options_render(self):
        """Tests rending of graph_options page."""
        result = self.client.get("/graph_options")
        self.assertEqual(result.status_code, 200)
        self.assertIn('Graphing options', result.data)
        self.assertIn('Fever', result.data)
        self.assertIn('Bee Venom', result.data)

    def test_auto_symptom(self):
        """tests json app route returning json of all symptom names in db."""
        result = self.client.get("/auto_symptom")
        data = json.loads(result.data)
        self.assertIn(data[0], 'Fever')

    def test_auto_treatment(self):
        """test json app route returning json of all treatment names in db."""
        result = self.client.get("/auto_treatment")
        data = json.loads(result.data)
        self.assertIn(data[0], 'Bee Venom')

    def test_set_symptom_existing(self):
        """Tests that when user tries to track same symptom twice, it doesn't get re-added."""
        result = self.client.post("/set_symptom", data={
                                    "symp": "Fever"})
        self.assertIn("You are already tracking", result.data)

    def test_set_symptom_new_to_user(self):
        """Tests setting new symptom for user to track in db, and
        adding it to Symptom table as well."""
        result = self.client.post("/set_symptom", data={
                                "symp": "Muscle Pain"})
        test_query = db.session.query(Symptom).filter(Symptom.name == "Muscle Pain").first()
        self.assertIn("Muscle Pain", test_query.name)

    def test_set_symptom_new_to_db(self):
        """Tests setting new symptom for user to track in db."""
        result = self.client.post("/set_symptom", data={
                                    "symp": "Headaches"})
        self.assertIn("Your symptom option, Headaches", result.data)

    def test_set_treatment_existing(self):
        """Tests treatment can't be duplicated for user to track in db."""
        result = self.client.post("/set_treatment", data={
                                    "treat": "Bee Venom"})
        self.assertIn("You are already tracking", result.data)

    def test_set_treatment_new_to_user(self):
        """Tests setting treatment for user to track in db."""
        result = self.client.post("/set_treatment", data={
                                    "treat": "Vit D"})
        self.assertIn("Your treatment option, Vit D", result.data)

    def test_set_treatment_nwe_to_db(self):
        """Tests that new treatments are added to master treatments table."""
        result = self.client.post("/set_treatment", data={
                                    "treat": "Vit D"})
        test_query = db.session.query(Treatment).filter(Treatment.name == "Vit D").first()
        self.assertIn("Vit D", test_query.name)

    def test_log_comment(self):
        """Tests adding user comment (journal entry) to db."""
        result = self.client.post("/log_comment", data={
                                    'date': '2017-09-11',
                                    'comment': 'this is a test'})
        self.assertIn("Your journal entry has been saved.", result.data)

    def test_track_symptom(self):
        """Tests adding user values to symptom to db."""
        result = self.client.post("/track_symptoms", data={
                                    'date': '2017-09-11',
                                    'Fever': 3
                                    })
        self.assertIn("Your symptoms have been logged", result.data)

    def test_track_treatment(self):
        """Tests adding user values to track treatment to db."""
        result = self.client.post("/track_treatments", data={
                                    'date': '2017-09-11',
                                    'Bee Venom': 10
                                    })
        self.assertIn("Your treatments have been logged", result.data)

    def test_graph_json(self):
        """Tests app route that packages user data for graphing in plotly."""

        result = self.client.get('/graph_data.json', query_string={
                                    'symptom_options':'["Fever"]',
                                    'treatment_option':'"Bee Venom"'})
        data = json.loads(result.data)
        self.assertIn("data", data)
        self.assertIn("date_range", data)


def example_data():
    """data for test db beetlyme_test"""
    created_at = '2017-09-01'
    user_1 = User(fname='Annabelle',
                lname='Akkerman',
                email='annabelle@gmail.com',
                password='password123',
                created_at='2017-09-01')
    user_2 = User(fname='Bernadette',
                lname='Bush',
                email='bernadette@gmail.com',
                password='password456',
                created_at='2017-09-01')

    db.session.add_all([user_1, user_2])
    symptom_1 = Symptom(name="Fever", created_at=created_at)
    symptom_2 = Symptom(name="Sweats, Chills", created_at=created_at)
    db.session.add_all([symptom_1, symptom_2])
    treatment_1 = Treatment(name='Bee Venom', created_at=created_at)
    treatment_2 = Treatment(name='Vitamin C', created_at=created_at)
    db.session.add_all([treatment_1, treatment_2])

    user_symptom_1 = UserSymptom(user_id=1, symptom_id=1, created_at=created_at)
    user_symptom_2 = UserSymptom(user_id=1, symptom_id=2, created_at=created_at)
    user_symptom_3 = UserSymptom(user_id=2, symptom_id=1, created_at=created_at)
    user_symptom_4 = UserSymptom(user_id=2, symptom_id=2, created_at=created_at)
    db.session.add_all([user_symptom_1, user_symptom_2, user_symptom_3, user_symptom_4])

    user_treatment_1 = UserTreatment(user_id=1, treatment_id=1, created_at=created_at)
    user_treatment_2 = UserTreatment(user_id=1, treatment_id=2, created_at=created_at)
    user_treatment_3 = UserTreatment(user_id=2, treatment_id=1, created_at=created_at)
    user_treatment_4 = UserTreatment(user_id=2, treatment_id=2, created_at=created_at)
    db.session.add_all([user_treatment_1, user_treatment_4, user_treatment_2, user_treatment_3])

    symptom_entry_1 = SymptomEntry(user_symp_id=1, value=6, created_at=created_at)
    symptom_entry_2 = SymptomEntry(user_symp_id=1, value=5, created_at='2017-09-03')
    symptom_entry_3 = SymptomEntry(user_symp_id=1, value=4, created_at='2017-09-06')
    symptom_entry_4 = SymptomEntry(user_symp_id=1, value=3, created_at='2017-09-09')
    symptom_entry_5 = SymptomEntry(user_symp_id=1, value=3, created_at='2017-09-20')
    se_1 = SymptomEntry(user_symp_id=2, value=6, created_at=created_at)
    se_2 = SymptomEntry(user_symp_id=2, value=5, created_at='2017-09-03')
    se_3 = SymptomEntry(user_symp_id=2, value=6, created_at='2017-09-06')
    se_4 = SymptomEntry(user_symp_id=2, value=5, created_at='2017-09-09')
    se_5 = SymptomEntry(user_symp_id=2, value=8, created_at='2017-09-20')
    se_6 = SymptomEntry(user_symp_id=3, value=6, created_at=created_at)
    se_7 = SymptomEntry(user_symp_id=3, value=5, created_at='2017-09-03')
    se_8 = SymptomEntry(user_symp_id=3, value=3, created_at='2017-09-06')
    se_9 = SymptomEntry(user_symp_id=3, value=5, created_at='2017-09-09')
    se_10 = SymptomEntry(user_symp_id=3, value=5, created_at='2017-09-20')
    se_11 = SymptomEntry(user_symp_id=4, value=6, created_at=created_at)
    se_12 = SymptomEntry(user_symp_id=4, value=5, created_at='2017-09-03')
    se_13 = SymptomEntry(user_symp_id=4, value=6, created_at='2017-09-06')
    se_14 = SymptomEntry(user_symp_id=1, value=5, created_at='2017-09-20')
    db.session.add_all([symptom_entry_1, se_1, se_2, se_3, se_4])
    db.session.add_all([symptom_entry_2, se_5, se_6, se_7, se_8])
    db.session.add_all([symptom_entry_3, se_9, se_10, se_11])
    db.session.add_all([symptom_entry_4, se_12, se_13, se_14])
    db.session.add(symptom_entry_5)

    treatment_entry_1 = TreatmentEntry(user_treat_id=1, value=10, created_at=created_at)
    treatment_entry_2 = TreatmentEntry(user_treat_id=1, value=10, created_at='2017-09-03')
    treatment_entry_3 = TreatmentEntry(user_treat_id=1, value=10, created_at='2017-09-06')
    treatment_entry_4 = TreatmentEntry(user_treat_id=1, value=10, created_at='2017-09-09')
    treatment_entry_5 = TreatmentEntry(user_treat_id=1, value=10, created_at='2017-09-20')
    te_1 = TreatmentEntry(user_treat_id=2, value=3000, created_at=created_at)
    te_2 = TreatmentEntry(user_treat_id=2, value=3000, created_at='2017-09-03')
    te_3 = TreatmentEntry(user_treat_id=2, value=3000, created_at='2017-09-20')
    te_4 = TreatmentEntry(user_treat_id=2, value=3000, created_at='2017-09-06')
    te_5 = TreatmentEntry(user_treat_id=2, value=3000, created_at='2017-09-09')
    te_6 = TreatmentEntry(user_treat_id=3, value=10, created_at='2017-09-20')
    te_7 = TreatmentEntry(user_treat_id=3, value=10, created_at='2017-09-03')
    te_8 = TreatmentEntry(user_treat_id=3, value=10, created_at='2017-09-06')
    te_9 = TreatmentEntry(user_treat_id=3, value=10, created_at='2017-09-09')
    te_10 = TreatmentEntry(user_treat_id=3, value=10, created_at='2017-09-01')
    te_11 = TreatmentEntry(user_treat_id=4, value=3000, created_at='2017-09-03')
    te_12 = TreatmentEntry(user_treat_id=4, value=3000, created_at='2017-09-06')
    te_13 = TreatmentEntry(user_treat_id=4, value=3000, created_at='2017-09-09')
    te_14 = TreatmentEntry(user_treat_id=4, value=3000, created_at='2017-09-20')

    db.session.add_all([treatment_entry_1, te_1, te_2, te_3, te_4])
    db.session.add_all([treatment_entry_2, te_5, te_6, te_7, te_8])
    db.session.add_all([treatment_entry_3, te_9, te_10, te_11])
    db.session.add_all([treatment_entry_4, te_12, te_13, te_14])
    db.session.add(treatment_entry_5)

    full_moon = FullMoon(full_moon_date="2017-09-06")
    db.session.add(full_moon)
    new_moon = NewMoon(new_moon_date="2017-09-20")
    db.session.add(new_moon)

    db.session.commit()


    
# class FlaskTestsDatabase(unittest.TestCase):
#     """Flask tests that use the database."""

#     def setUp(self):
#         """Stuff to do before every test."""
#         self.client = app.test_client()
#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'key'
#         # Connect to test database
#         connect_to_db(app, "postgresql:///beetlyme_test")

#         # Create tables and add sample data
#         db.create_all()
#         example_data()

#     def tearDown(self):
#         """Do at end of every test."""

#         db.session.close()
#         db.drop_all()

#     # def test_some_db_thing(self):
#     #     """Some database test..."


if __name__ == '__main__':
    unittest.main()
