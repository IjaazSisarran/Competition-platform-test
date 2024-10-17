from App.database import db

class Results(db.Model):
    __tablename__ = 'results'
    
    resultID = db.Column(db.String, primary_key=True)
    competitionID = db.Column(db.String, db.ForeignKey('competitions.competitionID'), nullable=False)  # Reference Competitions
    studentID = db.Column(db.String, db.ForeignKey('student.studentID'), nullable=False)  # Reference Student
    score = db.Column(db.Integer, nullable=False)
    completionTime = db.Column(db.String, nullable=True)
    ranking = db.Column(db.Integer, nullable=False)

    # Optionally, you can define relationships to get the competition and student directly
    competition = db.relationship('Competition', backref='results')
    student = db.relationship('Student', backref='results')

    def to_dict(self):
        return {
            "resultID": self.resultID,
            "competitionID": self.competitionID,
            "studentID": self.studentID,
            "score": self.score,
            "completionTime": self.completionTime,
            "ranking": self.ranking
        }

    def __repr__(self):
        return f'<Results {self.resultID}>'
