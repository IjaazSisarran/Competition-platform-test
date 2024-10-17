from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(20))
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    def __init__(self, username, password, user_type, firstName, lastName, email):
        self.username = username
        self.password = password
        self.user_type = user_type
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": user_type,  # Updated reference to "user_type"
    }