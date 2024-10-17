from App.database import db
from uuid import uuid4
from App.models import User

class Admin(User):
    __tablename__ = 'admin'
    
    adminID = db.Column(db.String, primary_key=True, nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

    def __init__(self, username, password, firstName, lastName, email, adminID):
        super().__init__(username, password, user_type="admin", firstName=firstName, lastName=lastName, email=email)
        self.adminID = adminID  

    def __repr__(self):
        return f'<Admin {self.adminID}>'

    def to_dict(self):
        return {
            'adminID': self.adminID,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email
        }

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }