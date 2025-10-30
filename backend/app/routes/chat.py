from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import Message, User

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/messages', methods=['GET'])
@jwt_required()
def get_messages():
    """Get chat messages"""
    try:
        limit = request.args.get('limit', 50, type=int)
        messages = Message.query.order_by(Message.timestamp.desc()).limit(limit).all()
        return jsonify([msg.to_dict() for msg in reversed(messages)]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/messages', methods=['POST'])
@jwt_required()
def send_message():
    """Send a chat message"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        message = Message(
            contenu=data['contenu'],
            user_id=user_id
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify(message.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
