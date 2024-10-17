from App.database import db

# Association table for students participating in competitions
competition_participants = db.Table(
    'competition_participants',
    db.Column('student_id', db.String, db.ForeignKey('student.studentID'), primary_key=True),
    db.Column('competition_id', db.String, db.ForeignKey('competitions.competitionID'), primary_key=True)
)

class Competition(db.Model):
    __tablename__ = 'competitions'
    competitionID = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String, nullable=True)
    competitionType = db.Column(db.String, nullable=False)
    adminID = db.Column(db.String, db.ForeignKey('admin.adminID'), nullable=True)  # Reference Admin ID

    # Relationship with Student model
    participants = db.relationship('Student', secondary=competition_participants, back_populates='competitions')

    def __repr__(self):
        return f'<Competition {self.competitionID}>'

    def to_dict(self):
        return {
            'competitionID': self.competitionID,
            'title': self.title,
            'date': self.date.isoformat(),
            'description': self.description,
            'competitionType': self.competitionType,
            'adminID': self.adminID,
        }