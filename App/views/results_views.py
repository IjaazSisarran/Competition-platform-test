from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from App.controllers import (
    get_all_results_json,
    get_results_by_competition,
    get_result_details,
)

results_views = Blueprint('results_views', __name__)

# Get all results
@results_views.route('/results', methods=['GET'])
def get_all_results():
    results = get_all_results_json()
    return jsonify(results), 200

# Get results for a specific competition
@results_views.route('/competitions/<competition_id>/results', methods=['GET'])
def get_competition_results(competition_id):
    results = get_results_by_competition(competition_id)
    if results:
        return jsonify([result.to_dict() for result in results]), 200
    return jsonify({'error': 'No results found for this competition'}), 404

# Get details of a specific result
@results_views.route('/results/<result_id>', methods=['GET'])
def get_result(result_id):
    result = get_result_details(result_id)
    if result:
        return jsonify(result.to_dict()), 200
    return jsonify({'error': 'Result not found'}), 404
