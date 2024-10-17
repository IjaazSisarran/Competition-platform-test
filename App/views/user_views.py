from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from App.controllers import (
    create_user, get_user_by_username, get_user, update_user
)

user_views = Blueprint('user_views', __name__)

# Register a user
@user_views.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    try:
        user = create_user(
            username=data['username'],
            password=data['password'],
            firstName=data['firstName'],
            lastName=data['lastName'],
            email=data['email']
        )
        return jsonify(user=user.get_json()), 201
    except Exception as e:
        return jsonify(error=str(e)), 400

# Login route
@user_views.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = get_user_by_username(data['username'])

    if user and user.check_password(data['password']):
        access_token = create_access_token(identity={'id': user.id, 'username': user.username})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid credentials"), 401

# Get details of the current logged-in user
@user_views.route('/user', methods=['GET'])
@jwt_required()
def get_current_user():
    identity = get_jwt_identity()
    user = get_user(identity['id'])
    if user:
        return jsonify(user=user.get_json()), 200
    return jsonify(message="User not found"), 404

# Update the current user's username
@user_views.route('/user', methods=['PUT'])
@jwt_required()
def update_user_view():
    identity = get_jwt_identity()
    data = request.get_json()
    try:
        update_user(identity['id'], data['username'])
        return jsonify(message="User updated successfully"), 200
    except Exception as e:
        return jsonify(error=str(e)), 400
