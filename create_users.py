from app import app, db
from models import User
from sqlalchemy.exc import IntegrityError

def create_default_users():
    with app.app_context():
        try:
            admin = User(username='admin', password='1234', role='admin')
            user = User(username='user', password='1234', role='user')

            # Add users to the session
            db.session.add(admin)
            db.session.add(user)

            # Commit the transaction
            db.session.commit()
            print("Default users created!")
        except IntegrityError as e:
            db.session.rollback()  # Roll back the transaction in case of error
            print("Error occurred:", e)

if __name__ == "__main__":
    create_default_users()
