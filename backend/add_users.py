#!/usr/bin/env python
"""Quick script to add test users to database"""
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db, bcrypt
from app.models.user import User

def add_test_users():
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check existing users
        existing = User.query.count()
        if existing > 0:
            print(f"⚠️  Database already has {existing} users")
            # Delete all users to reset
            User.query.delete()
            db.session.commit()
            print("✓ Cleared existing users")
        
        # Test users
        users = [
            {
                'nom': 'test',
                'email': 'test',
                'password': 'test123',
                'promo': 'B2',
                'role': 'admin'
            },
            {
                'nom': 'demo',
                'email': 'demo@laplateforme.fr',
                'password': 'demo123',
                'promo': 'B2',
                'role': 'admin'
            }
        ]
        
        # Add users
        for user_data in users:
            hashed = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            user = User(
                nom=user_data['nom'],
                email=user_data['email'],
                password=hashed,
                promo=user_data['promo'],
                role=user_data['role'],
                xp=0,
                niveau=1,
                date_inscription=datetime.utcnow()
            )
            db.session.add(user)
            print(f"✓ Added: {user_data['email']} / {user_data['password']}")
        
        db.session.commit()
        print("\n✅ Users added successfully!")
        print("\nTest credentials:")
        print("  - Email: test, Password: test123")
        print("  - Email: demo@laplateforme.fr, Password: demo123")

if __name__ == '__main__':
    add_test_users()
