#!/usr/bin/env python
"""
Script to add an admin user to the database
"""
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db, bcrypt
from app.models.user import User

def add_admin():
    """Add an admin user"""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        existing = User.query.filter_by(email='admin@plateforme.com').first()
        if existing:
            print(f"Admin user already exists: {existing.email}")
            return False
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash('Admin123!').decode('utf-8')
        
        # Create admin user
        admin = User(
            nom='Admin',
            email='admin@plateforme.com',
            password=hashed_password,
            promo='2024',
            role='admin',
            xp=10000,
            niveau=10,
            bio='Administrator account',
            date_inscription=datetime.utcnow()
        )
        
        db.session.add(admin)
        
        try:
            db.session.commit()
            print("✓ Admin user created successfully!")
            print(f"  Email: admin@plateforme.com")
            print(f"  Password: Admin123!")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error creating admin user: {e}")
            return False

if __name__ == '__main__':
    success = add_admin()
    sys.exit(0 if success else 1)
