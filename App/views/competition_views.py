from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from App.controllers import (
    Competition,
    generate_competition_id,
    get_competition_details,
    get_all_competitions_json,
    update_competition_details,
)
from App.database import db

competition_views = Blueprint('competition_views', __name__)

# Admin creates a competition
@competition_views.route('/admin/competition', methods=['POST'])
@jwt_required()
def create_competition():
    data = request.get_json()
    competition_id = generate_competition_id()
    
    new_competition = Competition(
        competitionID=competition_id,
        title=data['title'],
        date=data['date'],
        description=data.get('description'),
        competitionType=data['competitionType'],
        adminID=data['adminID']  # Make sure admin ID is provided
    )
    
    try:
        db.session.add(new_competition)
        db.session.commit()
        return jsonify({'message': 'Competition created', 'competitionID': competition_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Get details of a specific competition
@competition_views.route('/competitions/<competition_id>', methods=['GET'])
def get_competition(competition_id):
    competition = get_competition_details(competition_id)
    if competition:
        return jsonify(competition), 200
    return jsonify({'error': 'Competition not found'}), 404

# Get all competitions
@competition_views.route('/competitions', methods=['GET'])
def get_all_competitions():
    competitions = get_all_competitions_json()
    return jsonify(competitions), 200

# Admin updates a competition
@competition_views.route('/admin/competition/<competition_id>', methods=['PUT'])
@jwt_required()
def update_competition(competition_id):
    data = request.get_json()
    try:
        update_competition_details(
            competition_id,
            name=data.get('title'),
            date=data.get('date'),
            status=data.get('competitionType')
        )
        return jsonify({'message': f'Competition {competition_id} updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
