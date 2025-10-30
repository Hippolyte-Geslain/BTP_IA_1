from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, bcrypt, cache
from app.models.user import User
from werkzeug.utils import secure_filename
import os

users_bp = Blueprint('users', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users"""
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user by ID"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user profile"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check authorization
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Handle JSON or form data
        data = request.get_json() if request.is_json else request.form.to_dict()
        
        # Handle file upload
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"user_{user_id}_{file.filename}")
                upload_folder = os.path.join('static', 'avatars')
                os.makedirs(upload_folder, exist_ok=True)
                file.save(os.path.join(upload_folder, filename))
                user.avatar = f'/static/avatars/{filename}'
        
        # Update fields
        if 'nom' in data:
            user.nom = data['nom']
        if 'email' in data:
            user.email = data['email']
        if 'promo' in data:
            user.promo = data['promo']
        if 'bio' in data:
            user.bio = data['bio']
        
        db.session.commit()
        cache.delete(f'user_{user_id}')
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@users_bp.route('/<int:user_id>/change-password', methods=['POST'])
@jwt_required()
def change_password(user_id):
    """Change user password"""
    try:
        current_user_id = get_jwt_identity()
        
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Verify old password
        if not bcrypt.check_password_hash(user.password, data['old_password']):
            return jsonify({'error': 'Incorrect old password'}), 400
        
        # Hash and save new password
        user.password = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@users_bp.route('/leaderboard', methods=['GET'])
@cache.cached(timeout=60)
def get_leaderboard():
    """Get leaderboard"""
    try:
        users = User.query.order_by(User.xp.desc()).limit(100).all()
        return jsonify([{
            'rank': idx + 1,
            'id': user.id,
            'nom': user.nom,
            'xp': user.xp,
            'niveau': user.niveau,
            'promo': user.promo,
            'avatar': user.avatar
        } for idx, user in enumerate(users)]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
