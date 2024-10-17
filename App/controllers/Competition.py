from sqlalchemy import *
from App.models import Competition
from App.models import db

#Function to generate a competition
def generate_competition_id():
    last_competition = Competition.query.order_by(Competition.competitionID.desc()).first()
    if last_competition:
        last_id = int(last_competition.competitionID[1:])
        new_id = f'C{last_id + 1:03}'
    else:
        new_id = 'C001'
    return new_id

#Function to retrieve details of a specific competition
def get_competition_details(competition_id):
    competition = Competition.query.get(competition_id)
    if competition:
        return competition.to_dict()
    return None

#Function to update competition details
def update_competition_details(competition_id, **update_details):
    competition = Competition.query.filter_by(competitionID=competition_id).first()
    
    if not competition:
        print(f"No competition found with ID {competition_id}")
        return
    
    if 'name' in update_details and update_details['name']:
        competition.title = update_details['name']
    if 'date' in update_details and update_details['date']:
        competition.date = update_details['date']
    if 'status' in update_details and update_details['status']:
        competition.competitionType = update_details['status']
    
    try:
        db.session.commit()
        print(f"Competition {competition_id} updated successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error updating competition {competition_id}: {e}")

#Function to retrieve all competitions
def get_all_competitions_json():
    competitions = Competition.query.all()
    return [competition.to_dict() for competition in competitions]

#Function to add results to a competition (assuming results are related)
def add_results(competition_id, result):
    competition = Competition.query.get(competition_id)
    if competition:
        competition.results.append(result)
        db.session.commit()
        return True
    return False
