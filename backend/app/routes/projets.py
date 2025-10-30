from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import Projet, User
from datetime import datetime

projets_bp = Blueprint('projets', __name__)


@projets_bp.route('/', methods=['GET'])
@jwt_required()
def get_projets():
    """Get all projects"""
    try:
        user_id = request.args.get('user_id')
        
        if user_id:
            projets = Projet.query.filter_by(user_id=user_id).all()
        else:
            projets = Projet.query.all()
        
        return jsonify([projet.to_dict() for projet in projets]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@projets_bp.route('/<int:projet_id>', methods=['GET'])
@jwt_required()
def get_projet(projet_id):
    """Get project by ID"""
    try:
        projet = Projet.query.get(projet_id)
        if not projet:
            return jsonify({'error': 'Project not found'}), 404
        return jsonify(projet.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@projets_bp.route('/', methods=['POST'])
@jwt_required()
def create_projet():
    """Create new project"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        projet = Projet(
            titre=data['titre'],
            description=data.get('description', ''),
            technos=data.get('technos', []),
            difficulte=data.get('difficulte', 'medium'),
            xp_recompense=data.get('xp_recompense', 0),
            statut='non_commence',
            user_id=user_id
        )
        
        db.session.add(projet)
        db.session.commit()
        
        return jsonify({
            'message': 'Project created successfully',
            'projet': projet.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@projets_bp.route('/<int:projet_id>', methods=['PUT'])
@jwt_required()
def update_projet(projet_id):
    """Update project"""
    try:
        user_id = get_jwt_identity()
        projet = Projet.query.get(projet_id)
        
        if not projet:
            return jsonify({'error': 'Project not found'}), 404
        
        if projet.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        if 'titre' in data:
            projet.titre = data['titre']
        if 'description' in data:
            projet.description = data['description']
        if 'technos' in data:
            projet.technos = data['technos']
        if 'difficulte' in data:
            projet.difficulte = data['difficulte']
        if 'statut' in data:
            projet.statut = data['statut']
            
            # Award XP if project completed
            if data['statut'] == 'termine' and projet.statut != 'termine':
                user = User.query.get(user_id)
                user.xp += projet.xp_recompense
                projet.date_fin = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(projet.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@projets_bp.route('/<int:projet_id>', methods=['DELETE'])
@jwt_required()
def delete_projet(projet_id):
    """Delete project"""
    try:
        user_id = get_jwt_identity()
        projet = Projet.query.get(projet_id)
        
        if not projet:
            return jsonify({'error': 'Project not found'}), 404
        
        if projet.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(projet)
        db.session.commit()
        
        return jsonify({'message': 'Project deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
