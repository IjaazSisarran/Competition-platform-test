from App.controllers.Admin import import_results_from_file
from App.models import Results

#Function to retrieve all results
def get_all_results():
    return Results.query.all()

#Function to get all results in JSON format
def get_all_results_json():
    return [result.to_dict() for result in Results.query.all()]

def to_dict(self):
    return {
        "resultID": self.resultID,
        "competitionID": self.competitionID,
        "studentID": self.studentID,
        "score": self.score,
        "completionTime": self.completionTime,
        "ranking": self.ranking
    }

#Function to retrieve results for a specific competition
def get_results_by_competition(competition_id):
    return Results.query.filter_by(competitionID=competition_id).all()

#Function to process a file and update results (if necessary)
def process_file(file_path):
    import_results_from_file(file_path)  # Reuses the import logic

#Function to get details of a specific result
def get_result_details(result_id):
    return Results.query.get(result_id)
