from app import create_app, db
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = create_app()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': 'Plateforme XP API is running'}, 200


@app.route('/', methods=['GET'])
def index():
    """API root endpoint"""
    return {
        'message': 'Welcome to Plateforme XP API',
        'version': '1.0',
        'endpoints': {
            'auth': '/api/auth',
            'users': '/api/users',
            'projets': '/api/projets',
            'chat': '/api/chat',
            'health': '/health'
        }
    }, 200


if __name__ == '__main__':
    import socket
    
    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    # Check if port is in use
    if is_port_in_use(5000):
        print("⚠️  Port 5000 is already in use!")
        print("💡 Please run KILL_PORTS.bat to free the port, or use a different port.")
        print("🔄 Trying alternative port 5001...")
        port = 5001
    else:
        port = 5000
    
    with app.app_context():
        # Create all database tables
        db.create_all()
        print("✅ Database tables created")
    
    # Run the application
    print("🚀 Starting Plateforme XP Backend...")
    print(f"📡 Server running on http://localhost:{port}")
    print("🔥 Press CTRL+C to stop")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=port,
        use_reloader=False  # Avoid double startup
    )
