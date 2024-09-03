from app import app, db
from models import User
from sqlalchemy.exc import IntegrityError

def create_default_users():
    with app.app_context():
        try:
            # Create admin users
            admin1 = User(username='Amanuel Teklay', password='1234', role='admin')
            admin2 = User(username='G/Anenia Tsegay', password='1234', role='admin')
            admin3 = User(username='admin', password='1234', role='admin')

            # Create regular users
            user1 = User(username='Getachew Gebre', password='1234', role='user')
            user2 = User(username='user', password='1234', role='user')

            # Add users to the session
            db.session.add(admin1)
            db.session.add(admin2)
            db.session.add(admin3)
            db.session.add(user1)
            db.session.add(user2)

            # Commit the transaction
            db.session.commit()
            print("Default users created!")
        except IntegrityError as e:
            db.session.rollback()  # Roll back the transaction in case of error
            print("Error occurred:", e)

if __name__ == "__main__":
    create_default_users()