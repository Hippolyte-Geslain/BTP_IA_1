from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    promo = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(20), default='student')
    xp = db.Column(db.Integer, default=0)
    niveau = db.Column(db.Integer, default=1)
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(255))
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    projets = db.relationship('Projet', backref='user', lazy=True, cascade='all, delete-orphan')
    badges = db.relationship('Badge', backref='user', lazy=True, cascade='all, delete-orphan')
    messages = db.relationship('Message', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'email': self.email,
            'promo': self.promo,
            'role': self.role,
            'xp': self.xp,
            'niveau': self.niveau,
            'bio': self.bio,
            'avatar': self.avatar,
            'date_inscription': self.date_inscription.isoformat() if self.date_inscription else None,
            'projets_count': len(self.projets),
            'badges_count': len(self.badges)
        }


class Projet(db.Model):
    __tablename__ = 'projets'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    technos = db.Column(db.JSON)
    difficulte = db.Column(db.String(20))
    xp_recompense = db.Column(db.Integer, default=0)
    statut = db.Column(db.String(20), default='non_commence')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_debut = db.Column(db.DateTime)
    date_fin = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'description': self.description,
            'technos': self.technos or [],
            'difficulte': self.difficulte,
            'xp_recompense': self.xp_recompense,
            'statut': self.statut,
            'user_id': self.user_id,
            'date_debut': self.date_debut.isoformat() if self.date_debut else None,
            'date_fin': self.date_fin.isoformat() if self.date_fin else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Badge(db.Model):
    __tablename__ = 'badges'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icone = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_obtention = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'icone': self.icone,
            'user_id': self.user_id,
            'date_obtention': self.date_obtention.isoformat() if self.date_obtention else None
        }


class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'contenu': self.contenu,
            'user_id': self.user_id,
            'user': self.user.to_dict() if self.user else None,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
