#!/usr/bin/env python
"""Quick script to add test users directly"""
import os
import sys
import json
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

def add_users():
    # Use SQLite directly to avoid import conflicts
    db_path = 'backend/instance/plateforme_xp.db'
    
    # Create db directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom VARCHAR(100) NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            promo VARCHAR(10) NOT NULL,
            role VARCHAR(20) DEFAULT 'student',
            xp INTEGER DEFAULT 0,
            niveau INTEGER DEFAULT 1,
            bio TEXT,
            avatar VARCHAR(255),
            date_inscription DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Load data from JSON
    with open('plateforme_data.json', 'r') as f:
        data = json.load(f)
    
    # Clear existing users
    cursor.execute('DELETE FROM users')
    conn.commit()
    print("✓ Cleared existing users")
    
    # Add test users
    for user_data in data['users']:
        hashed_password = generate_password_hash(user_data['password'])
        
        try:
            cursor.execute('''
                INSERT INTO users (nom, email, password, promo, role, xp, niveau, date_inscription)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_data['nom'],
                user_data['email'],
                hashed_password,
                user_data['promo'],
                user_data.get('role', 'student'),
                user_data.get('xp', 0),
                user_data.get('niveau', 1),
                user_data['date_inscription']
            ))
            print(f"✓ Adding user: {user_data['email']} / {user_data['password']}")
        except Exception as e:
            print(f"⚠ Error adding user {user_data['email']}: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Database seeded successfully!")
    print("\nTest accounts:")
    for user_data in data['users']:
        print(f"  Email: {user_data['email']}")
        print(f"  Password: {user_data['password']}\n")

if __name__ == '__main__':
    try:
        add_users()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
