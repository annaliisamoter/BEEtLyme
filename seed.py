from sqlalchemy import func
from model import User
from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app
from datetime import datetime




def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    for row in open("seed_data/u.fake-user"):
        row = row.rstrip()
        fname, lname, email, password = row.split("|")

        user = User(fname=fname,
                    lname=lname,
                    email=email,
                    password=password)

        db.session.add(user)

    db.session.commit()



    if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    
    
