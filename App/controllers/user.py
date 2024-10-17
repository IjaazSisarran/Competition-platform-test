from App.models import User
from App.database import db
from werkzeug.security import generate_password_hash

def create_user(username, password, firstName, lastName, email):
    hashed_password = generate_password_hash(password)  # Hash the password
    new_user = User(
        username=username,
        password=hashed_password,  # Use the hashed password
        user_type='user',  # Set the default user type
        firstName=firstName,  # Pass the first name
        lastName=lastName,  # Pass the last name
        email=email  # Pass the email
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    