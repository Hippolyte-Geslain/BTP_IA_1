#!/usr/bin/env python3
import sys
import os

os.chdir(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 50)
print("BACKEND STARTUP TEST")
print("=" * 50)

try:
    print("\n1. Testing imports...")
    from backend.app import create_app, db
    print("   ✓ Flask app created successfully")
    
    print("\n2. Creating app context...")
    app = create_app()
    print("   ✓ App created")
    
    print("\n3. Testing database...")
    with app.app_context():
        db.create_all()
        print("   ✓ Database initialized")
    
    print("\n4. Starting server on http://localhost:5000")
    print("   Press CTRL+C to stop\n")
    
    app.run(
        debug=False,
        host='0.0.0.0',
        port=5000,
        use_reloader=False
    )
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to close...")
