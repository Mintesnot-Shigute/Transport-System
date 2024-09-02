from app import app, db

def reset_database():
    with app.app_context():
        # Drop all tables in the database
        db.drop_all()
        
        # Create all tables based on the current models
        db.create_all()
        
        print("Database has been reset and tables have been recreated!")

if __name__ == "__main__":
    reset_database()
