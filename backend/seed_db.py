#!/usr/bin/env python
"""
Script to seed the database with test accounts from plateforme_data.json
"""
import json
import os
import sys
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db, bcrypt
from app.models.user import User

def load_data_from_json(json_file):
    """Load data from JSON file"""
    try:
        with open(json_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file} not found")
        return None

def seed_database():
    """Seed the database with test accounts"""
    app = create_app()
    
    with app.app_context():
        # Load data
        json_file = os.path.join(os.path.dirname(__file__), '..', 'plateforme_data.json')
        data = load_data_from_json(json_file)
        
        if not data:
            print("Failed to load data")
            return False
        
        # Check if users table is empty
        existing_users = User.query.count()
        if existing_users > 0:
            print(f"Database already contains {existing_users} user(s)")
            response = input("Do you want to clear existing users? (yes/no): ").lower()
            if response == 'yes':
                User.query.delete()
                db.session.commit()
                print("Cleared existing users")
            else:
                print("Aborted seeding")
                return False
        
        # Insert users
        users_data = data.get('users', [])
        if not users_data:
            print("No users found in data")
            return False
        
        print(f"\nSeeding {len(users_data)} user(s)...")
        
        for user_data in users_data:
            # Check if user already exists
            existing = User.query.filter_by(email=user_data['email']).first()
            if existing:
                print(f"User {user_data['email']} already exists, skipping...")
                continue
            
            # Hash the password
            hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            
            # Create user
            user = User(
                nom=user_data['nom'],
                email=user_data['email'],
                password=hashed_password,
                promo=user_data['promo'],
                role=user_data.get('role', 'student'),
                xp=user_data.get('xp', 0),
                niveau=user_data.get('niveau', 1),
                date_inscription=datetime.fromisoformat(user_data['date_inscription']) if isinstance(user_data.get('date_inscription'), str) else datetime.utcnow()
            )
            
            db.session.add(user)
            print(f"✓ Added user: {user_data['email']} ({user_data['nom']})")
        
        try:
            db.session.commit()
            print("\n✓ Database seeded successfully!")
            print("\nTest accounts created:")
            for user_data in users_data:
                print(f"  - Email: {user_data['email']}, Password: {user_data['password']}")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ Error seeding database: {e}")
            return False

if __name__ == '__main__':
    success = seed_database()
    sys.exit(0 if success else 1)
