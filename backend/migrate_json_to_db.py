import json
import sys
from app import create_app, db, bcrypt
from app.models.user import User, Projet, Badge, Message
from datetime import datetime

def migrate_data():
    """Migrate data from JSON file to database"""
    app = create_app()
    
    with app.app_context():
        print("🚀 Starting data migration...")
        print("=" * 50)
        
        # Read JSON file
        json_path = '../plateforme_data.json'
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: {json_path} not found")
            return False
        
        # Create tables
        db.create_all()
        print("✅ Database tables created")
        
        # Migrate users
        user_map = {}
        users_data = data.get('users', [])
        
        for user_data in users_data:
            # Check if user already exists
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user:
                print(f"⚠️  User {user_data['nom']} already exists, skipping...")
                user_map[user_data['email']] = existing_user.id
                continue
            
            # Create new user
            # Check if password is already hashed (starts with $2b$)
            if user_data['password'].startswith('$2b$') or user_data['password'].startswith('$2a$'):
                password = user_data['password']
            else:
                password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            
            user = User(
                nom=user_data['nom'],
                email=user_data['email'],
                password=password,
                promo=user_data['promo'],
                role=user_data.get('role', 'student'),
                xp=user_data.get('xp', 0),
                niveau=user_data.get('niveau', 1)
            )
            
            # Parse date if exists
            if 'date_inscription' in user_data:
                try:
                    user.date_inscription = datetime.fromisoformat(user_data['date_inscription'])
                except:
                    user.date_inscription = datetime.utcnow()
            
            db.session.add(user)
            db.session.flush()
            user_map[user_data['email']] = user.id
            print(f"✅ Migrated user: {user.nom} (ID: {user.id})")
        
        db.session.commit()
        print(f"\n📊 Total users migrated: {len(user_map)}")
        
        # Migrate projects
        project_count = 0
        for user_data in users_data:
            user_id = user_map.get(user_data['email'])
            if not user_id:
                continue
            
            for projet_data in user_data.get('projets', []):
                projet = Projet(
                    titre=projet_data.get('titre', 'Untitled Project'),
                    description=projet_data.get('description', ''),
                    technos=projet_data.get('technos', []),
                    difficulte=projet_data.get('difficulte', 'medium'),
                    xp_recompense=projet_data.get('xp_recompense', 0),
                    statut=projet_data.get('statut', 'non_commence'),
                    user_id=user_id
                )
                db.session.add(projet)
                project_count += 1
        
        db.session.commit()
        print(f"✅ Total projects migrated: {project_count}")
        
        # Migrate badges
        badge_count = 0
        for user_data in users_data:
            user_id = user_map.get(user_data['email'])
            if not user_id:
                continue
            
            for badge_data in user_data.get('badges', []):
                badge = Badge(
                    nom=badge_data.get('nom', 'Unknown Badge'),
                    description=badge_data.get('description', ''),
                    icone=badge_data.get('icone', '🏆'),
                    user_id=user_id
                )
                if 'date_obtention' in badge_data:
                    try:
                        badge.date_obtention = datetime.fromisoformat(badge_data['date_obtention'])
                    except:
                        badge.date_obtention = datetime.utcnow()
                
                db.session.add(badge)
                badge_count += 1
        
        db.session.commit()
        print(f"✅ Total badges migrated: {badge_count}")
        
        print("\n" + "=" * 50)
        print("🎉 Migration completed successfully!")
        print("=" * 50)
        
        return True


if __name__ == '__main__':
    success = migrate_data()
    sys.exit(0 if success else 1)
