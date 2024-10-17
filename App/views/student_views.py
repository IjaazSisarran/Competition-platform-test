from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from App.controllers import (
    create_student, get_all_students_json, view_competitions,
    view_results, register_for_competition
)

student_views = Blueprint('student_views', __name__)

# Register a student
@student_views.route('/register/student', methods=['POST'])
def register_student():
    data = request.get_json()
    try:
        student_id = create_student(
            username=data['username'],
            password=data['password'],
            first_name=data['firstName'],
            last_name=data['lastName'],
            email=data['email']
        )
        return jsonify(student_id=student_id), 201
    except Exception as e:
        return jsonify(error=str(e)), 400

# Get all students (Admin only)
@student_views.route('/students', methods=['GET'])
@jwt_required()
def get_all_students():
    students = get_all_students_json()
    return jsonify(students), 200

# View competitions a student can join
@student_views.route('/student/<student_id>/competitions', methods=['GET'])
@jwt_required()
def student_view_competitions(student_id):
    competitions = view_competitions(student_id)
    return jsonify([competition.to_dict() for competition in competitions]), 200

# View results for a specific student
@student_views.route('/student/<student_id>/results', methods=['GET'])
@jwt_required()
def student_view_results(student_id):
    results = view_results(student_id)
    return jsonify([result.to_dict() for result in results]), 200

# Register a student for a competition
@student_views.route('/student/<student_id>/competition/<competition_id>', methods=['POST'])
@jwt_required()
def register_student_for_competition(student_id, competition_id):
    try:
        register_for_competition(student_id, competition_id)
        return jsonify(message=f"Student {student_id} registered for competition {competition_id}"), 201
    except Exception as e:
        return jsonify(error=str(e)), 400
