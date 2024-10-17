from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from App.controllers import (
    create_admin, get_all_admins_json, create_competition, update_competition_details
)

admin_views = Blueprint('admin_views', __name__)

# Register an admin
@admin_views.route('/register/admin', methods=['POST'])
def register_admin():
    data = request.get_json()
    try:
        admin_id = create_admin(
            username=data['username'],
            password=data['password'],
            first_name=data['firstName'],
            last_name=data['lastName'],
            email=data['email']
        )
        return jsonify(admin_id=admin_id), 201
    except Exception as e:
        return jsonify(error=str(e)), 400

# Get all admins (Admin-only)
@admin_views.route('/admins', methods=['GET'])
@jwt_required()
def get_all_admins():
    admins = get_all_admins_json()
    return jsonify(admins), 200

# Admin creates a competition
@admin_views.route('/admin/competition', methods=['POST'])
@jwt_required()
def create_competition_view():
    data = request.get_json()
    try:
        competition_id = create_competition(
            name=data['title'],
            date_str=data['date'],
            status=data['competitionType'],
            description=data.get('description'),
            admin_id=data['adminID']
        )
        return jsonify(competition_id=competition_id), 201
    except Exception as e:
        return jsonify(error=str(e)), 400

# Admin updates a competition
@admin_views.route('/admin/competition/<competition_id>', methods=['PUT'])
@jwt_required()
def update_competition_view(competition_id):
    data = request.get_json()
    try:
        update_competition_details(
            competition_id,
            name=data.get('title'),
            date=data.get('date'),
            status=data.get('competitionType')
        )
        return jsonify(message=f"Competition {competition_id} updated successfully"), 200
    except Exception as e:
        return jsonify(error=str(e)), 400
