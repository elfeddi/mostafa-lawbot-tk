from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import embed_document
import os

file_bp = Blueprint('file', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

@file_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    current_user = get_jwt_identity()
    filename = file.filename
    user_upload_dir = os.path.join(UPLOAD_FOLDER, current_user)
    os.makedirs(user_upload_dir, exist_ok=True)
    file_path = os.path.join(user_upload_dir, filename)
    file.save(file_path)

    embed_document(file_path, current_user)
    return jsonify({"message": "File uploaded and processed successfully"}), 201
