from flask import Blueprint, request, jsonify

taxi_driver_bp = Blueprint('taxi_driver', __name__)

@taxi_driver_bp.route('/taxi_driver', methods=['POST'])
def driver():
    data = request.get_json()


    