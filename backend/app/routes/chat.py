from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Chat, Message, db

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/create_chat', methods=['POST'])
@jwt_required()
def create_chat():
    data = request.get_json()
    username = get_jwt_identity()
    title = data.get('title')

    if not title:
        return jsonify({"message": "Title is required"}), 400

    new_chat = Chat(username=username, title=title)
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({"message": "Chat created successfully"}), 201

@chat_bp.route('/get_chats', methods=['GET'])
@jwt_required()
def get_chats():
    username = get_jwt_identity()
    chats = Chat.query.filter_by(username=username).all()
    chat_list = [{"id": chat.id, "title": chat.title, "created_at": chat.created_at} for chat in chats]

    return jsonify(chat_list), 200

@chat_bp.route('/<int:chat_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(chat_id):
    messages = Message.query.filter_by(chat_id=chat_id).all()
    message_list = [{"id": message.id, "sender": message.sender, "content": message.content, "timestamp": message.timestamp} for message in messages]
    
    return jsonify(message_list), 200
@chat_bp.route('/add_message', methods=['POST'])
@jwt_required()
def add_message():
    data = request.json
    chat_id = data.get('chat_id')
    sender = data.get('sender')
    content = data.get('content')

    if not chat_id or not sender or not content:
        return jsonify({'message': 'Missing data'}), 400

    new_message = Message(chat_id=chat_id, sender=sender, content=content)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({'message': 'Message added successfully'}), 201