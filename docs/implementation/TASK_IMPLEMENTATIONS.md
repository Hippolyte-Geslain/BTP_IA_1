# 📋 TASK IMPLEMENTATIONS - PLATEFORME XP

This document provides detailed implementation solutions for all tasks from TRELLO_TASKS.md.
Generated: 2025-10-30 10:57:14

---

## 🔴 CRITIQUE (MVP - INDISPENSABLE)

### Task 1: API Backend (Flask + PostgreSQL)

**Implementation:**

#### Step 1: Install dependencies
```bash
pip install flask flask-sqlalchemy flask-jwt-extended flask-cors psycopg2-binary python-dotenv flask-bcrypt
```

#### Step 2: Create project structure
```bash
mkdir -p backend/app/routes backend/app/models backend/app/utils
cd backend
```

#### Step 3: Create Flask application (backend/app/__init__.py)
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/plateforme_xp')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.projets import projets_bp
    from app.routes.chat import chat_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(projets_bp, url_prefix='/api/projets')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    
    return app
```

#### Step 4: Create User Model (backend/app/models/user.py)
```python
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
    projets = db.relationship('Projet', backref='user', lazy=True)
    badges = db.relationship('Badge', backref='user', lazy=True)
    messages = db.relationship('Message', backref='user', lazy=True)
    
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
            'date_inscription': self.date_inscription.isoformat() if self.date_inscription else None
        }
```

#### Step 5: Create Project Model (backend/app/models/projet.py)
```python
from app import db
from datetime import datetime

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
            'technos': self.technos,
            'difficulte': self.difficulte,
            'xp_recompense': self.xp_recompense,
            'statut': self.statut,
            'user_id': self.user_id,
            'date_debut': self.date_debut.isoformat() if self.date_debut else None,
            'date_fin': self.date_fin.isoformat() if self.date_fin else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
```

#### Step 6: Create Auth Routes (backend/app/routes/auth.py)
```python
from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    new_user = User(
        nom=data['nom'],
        email=data['email'],
        password=hashed_password,
        promo=data['promo'],
        role=data.get('role', 'student')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully', 'user': new_user.to_dict()}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200
```

#### Step 7: Create main app file (backend/run.py)
```python
from app import create_app, db
import os

app = create_app()

@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
```

#### Step 8: Create environment file (.env)
```bash
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/plateforme_xp
```

#### Step 9: Initialize PostgreSQL database
```bash
# Create database
psql -U postgres
CREATE DATABASE plateforme_xp;
\q

# Run migrations
python run.py
```

**Testing with curl:**
```bash
# Register a user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nom":"Test User","email":"test@test.com","password":"password123","promo":"B2"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'
```

---

### Task 2: Interface Web (React)

**Implementation:**

#### Step 1: Create React application
```bash
npx create-react-app frontend
cd frontend
npm install axios react-router-dom @mui/material @emotion/react @emotion/styled
```

#### Step 2: Create API service (frontend/src/services/api.js)
```javascript
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = Bearer +token+`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  getCurrentUser: () => api.get('/auth/me'),
};

export const usersAPI = {
  getAll: () => api.get('/users'),
  getById: (id) => api.get(+"/users/"+id+),
  update: (id, data) => api.put(+"/users/"+id+, data),
  delete: (id) => api.delete(+"/users/"+id+),
};

export const projetsAPI = {
  getAll: () => api.get('/projets'),
  getById: (id) => api.get(+"/projets/"+id+),
  create: (data) => api.post('/projets', data),
  update: (id, data) => api.put(+"/projets/"+id+, data),
  delete: (id) => api.delete(+"/projets/"+id+),
};

export const chatAPI = {
  getMessages: () => api.get('/chat/messages'),
  sendMessage: (data) => api.post('/chat/messages', data),
};

export default api;
```

#### Step 3: Create Login Component (frontend/src/components/Login.jsx)
```javascript
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
import { TextField, Button, Container, Typography, Box, Alert } from '@mui/material';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await authAPI.login({ email, password });
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography component="h1" variant="h3" gutterBottom>
          🎮 Plateforme XP
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          L'application des étudiants de La Plateforme_
        </Typography>
        
        {error && <Alert severity="error" sx={{ mt: 2, width: '100%' }}>{error}</Alert>}
        
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3, width: '100%' }}>
          <TextField
            fullWidth
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Mot de passe"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            margin="normal"
            required
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Se connecter
          </Button>
          <Button
            fullWidth
            variant="outlined"
            onClick={() => navigate('/register')}
          >
            Créer un compte
          </Button>
        </Box>
      </Box>
    </Container>
  );
}

export default Login;
```

#### Step 4: Create App Router (frontend/src/App.js)
```javascript
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Projects from './components/Projects';
import Chat from './components/Chat';
import Leaderboard from './components/Leaderboard';
import Profile from './components/Profile';

function App() {
  const isAuthenticated = () => !!localStorage.getItem('token');

  const ProtectedRoute = ({ children }) => {
    return isAuthenticated() ? children : <Navigate to="/login" />;
  };

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/projects" element={<ProtectedRoute><Projects /></ProtectedRoute>} />
        <Route path="/chat" element={<ProtectedRoute><Chat /></ProtectedRoute>} />
        <Route path="/leaderboard" element={<ProtectedRoute><Leaderboard /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
        <Route path="/" element={<Navigate to="/dashboard" />} />
      </Routes>
    </Router>
  );
}

export default App;
```

#### Step 5: Run the application
```bash
# Backend
cd backend
python run.py

# Frontend (in another terminal)
cd frontend
npm start
```

---

### Task 3: Authentification JWT

**Implementation:**

The JWT authentication is already integrated in Tasks 1 and 2. Here's a summary:

#### Key Components:

1. **Password Hashing (backend):**
```python
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# On registration
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

# On login
bcrypt.check_password_hash(user.password, provided_password)
```

2. **JWT Token Generation:**
```python
from flask_jwt_extended import create_access_token
access_token = create_access_token(identity=user.id)
```

3. **Protected Routes:**
```python
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    return {'user_id': user_id}
```

4. **Token Refresh Endpoint (backend/app/routes/auth.py):**
```python
from flask_jwt_extended import create_refresh_token, jwt_required, get_jwt_identity

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_token = create_access_token(identity=user_id)
    return jsonify({'access_token': new_token}), 200
```

5. **Frontend Token Storage:**
```javascript
// Store token
localStorage.setItem('token', access_token);

// Retrieve and use token
const token = localStorage.getItem('token');
axios.defaults.headers.common['Authorization'] = +Bearer +token+`;
```

**Testing:**
```bash
# Get token
TOKEN=+"(curl -s -X POST http://localhost:5000/api/auth/login -H \"Content-Type: application/json\" -d '{\"email\":\"test@test.com\",\"password\":\"password123\"}' | jq -r '.access_token')"+

# Use token to access protected route
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer "
```

---

### Task 4: Migration de base de données depuis JSON

**Implementation:**

#### Create migration script (backend/migrate_json_to_db.py)
```python
import json
from app import create_app, db, bcrypt
from app.models.user import User
from app.models.projet import Projet
from app.models.badge import Badge
from app.models.message import Message
from datetime import datetime

def migrate_data():
    app = create_app()
    
    with app.app_context():
        # Read JSON file
        with open('../plateforme_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("Starting migration...")
        
        # Clear existing data (optional, for fresh migration)
        db.drop_all()
        db.create_all()
        
        # Migrate users
        user_map = {}
        for user_data in data.get('users', []):
            user = User(
                nom=user_data['nom'],
                email=user_data['email'],
                password=user_data['password'],  # Already hashed or will be hashed
                promo=user_data['promo'],
                role=user_data.get('role', 'student'),
                xp=user_data.get('xp', 0),
                niveau=user_data.get('niveau', 1),
                date_inscription=datetime.fromisoformat(user_data['date_inscription']) 
                    if 'date_inscription' in user_data else datetime.utcnow()
            )
            db.session.add(user)
            db.session.flush()  # Get the ID
            user_map[user_data['email']] = user.id
            print(f"Migrated user: {user.nom}")
        
        db.session.commit()
        
        # Migrate projects
        for user_data in data.get('users', []):
            user_id = user_map[user_data['email']]
            for projet_data in user_data.get('projets', []):
                projet = Projet(
                    titre=projet_data.get('titre', 'Untitled'),
                    description=projet_data.get('description', ''),
                    technos=projet_data.get('technos', []),
                    difficulte=projet_data.get('difficulte', 'medium'),
                    xp_recompense=projet_data.get('xp_recompense', 0),
                    statut=projet_data.get('statut', 'non_commence'),
                    user_id=user_id
                )
                db.session.add(projet)
                print(f"Migrated project: {projet.titre}")
        
        db.session.commit()
        
        # Migrate badges
        for user_data in data.get('users', []):
            user_id = user_map[user_data['email']]
            for badge_data in user_data.get('badges', []):
                badge = Badge(
                    nom=badge_data.get('nom', 'Unknown Badge'),
                    description=badge_data.get('description', ''),
                    icone=badge_data.get('icone', '🏆'),
                    user_id=user_id,
                    date_obtention=datetime.fromisoformat(badge_data['date_obtention'])
                        if 'date_obtention' in badge_data else datetime.utcnow()
                )
                db.session.add(badge)
                print(f"Migrated badge: {badge.nom}")
        
        db.session.commit()
        
        # Migrate chat messages if they exist
        for msg_data in data.get('messages', []):
            message = Message(
                contenu=msg_data.get('contenu', ''),
                user_id=user_map.get(msg_data.get('user_email'), 1),
                timestamp=datetime.fromisoformat(msg_data['timestamp'])
                    if 'timestamp' in msg_data else datetime.utcnow()
            )
            db.session.add(message)
        
        db.session.commit()
        
        print("Migration completed successfully!")
        print(f"Migrated {len(user_map)} users")

if __name__ == '__main__':
    migrate_data()
```

#### Run migration
```bash
cd backend
python migrate_json_to_db.py
```

#### Create backup script (backend/backup_db.py)
```python
import os
import subprocess
from datetime import datetime

def backup_database():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'backup_plateforme_xp_{timestamp}.sql'
    
    db_url = os.getenv('DATABASE_URL', 'postgresql://localhost/plateforme_xp')
    
    # Extract connection details
    # Format: postgresql://user:password@host:port/database
    
    subprocess.run([
        'pg_dump',
        '-h', 'localhost',
        '-U', 'postgres',
        '-d', 'plateforme_xp',
        '-f', backup_file
    ])
    
    print(f"Backup created: {backup_file}")

if __name__ == '__main__':
    backup_database()
```

---

### Task 5: Déploiement Cloud

**Implementation:**

#### Option 1: Heroku Deployment

**Step 1: Create Procfile (backend/Procfile)**
```
web: gunicorn run:app
```

**Step 2: Update requirements.txt**
```bash
pip install gunicorn
pip freeze > requirements.txt
```

**Step 3: Deploy to Heroku**
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create plateforme-xp-backend

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set JWT_SECRET_KEY=your-jwt-secret

# Deploy
git push heroku main

# Run migrations
heroku run python migrate_json_to_db.py
```

#### Option 2: Railway Deployment

**Step 1: Create railway.json**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn run:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Step 2: Deploy**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to project
railway link

# Deploy
railway up
```

#### Frontend Deployment (Vercel)

**Step 1: Create vercel.json (frontend/vercel.json)**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

**Step 2: Deploy to Vercel**
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Set environment variable
vercel env add REACT_APP_API_URL production
# Enter your backend URL (e.g., https://plateforme-xp-backend.herokuapp.com/api)
```

#### Frontend Deployment (Netlify)

**Step 1: Create netlify.toml (frontend/netlify.toml)**
```toml
[build]
  command = "npm run build"
  publish = "build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

**Step 2: Deploy**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd frontend
netlify deploy --prod
```

#### SSL/HTTPS Configuration
All these platforms (Heroku, Railway, Vercel, Netlify) provide automatic HTTPS with free SSL certificates. No additional configuration needed.

**Health Check Endpoint:**
Already created in run.py:
```python
@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}, 200
```

---

## 🟡 PRIORITÉ MOYENNE (AMÉLIORER L'EXPÉRIENCE UTILISATEUR)

### Task 6: WebSockets en Temps Réel pour le Chat

**Implementation:**

#### Step 1: Install dependencies
```bash
# Backend
pip install flask-socketio eventlet

# Frontend
npm install socket.io-client
```

#### Step 2: Add Socket.IO to Flask (backend/app/__init__.py)
```python
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    # ... existing configuration ...
    
    socketio.init_app(app, cors_allowed_origins="*")
    
    return app
```

#### Step 3: Create WebSocket handlers (backend/app/sockets/chat.py)
```python
from flask_socketio import emit, join_room, leave_room
from flask import request
from app import socketio, db
from app.models.message import Message
from app.models.user import User
from datetime import datetime

active_users = {}

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    user_id = active_users.pop(request.sid, None)
    if user_id:
        emit('user_left', {'user_id': user_id}, broadcast=True)

@socketio.on('join')
def handle_join(data):
    user_id = data['user_id']
    active_users[request.sid] = user_id
    emit('user_joined', {
        'user_id': user_id,
        'active_users': list(active_users.values())
    }, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    user_id = data['user_id']
    content = data['content']
    
    # Save to database
    message = Message(
        contenu=content,
        user_id=user_id,
        timestamp=datetime.utcnow()
    )
    db.session.add(message)
    db.session.commit()
    
    # Get user info
    user = User.query.get(user_id)
    
    # Broadcast to all clients
    emit('new_message', {
        'id': message.id,
        'content': content,
        'user': user.to_dict(),
        'timestamp': message.timestamp.isoformat()
    }, broadcast=True)

@socketio.on('typing')
def handle_typing(data):
    user_id = data['user_id']
    user = User.query.get(user_id)
    emit('user_typing', {
        'user_id': user_id,
        'user_name': user.nom
    }, broadcast=True, include_self=False)

@socketio.on('stop_typing')
def handle_stop_typing(data):
    user_id = data['user_id']
    emit('user_stop_typing', {'user_id': user_id}, broadcast=True, include_self=False)
```

#### Step 4: Update run.py
```python
from app import create_app, db, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
```

#### Step 5: Create React WebSocket hook (frontend/src/hooks/useSocket.js)
```javascript
import { useEffect, useState } from 'react';
import io from 'socket.io-client';

const SOCKET_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const useSocket = () => {
  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const newSocket = io(SOCKET_URL);
    
    newSocket.on('connect', () => {
      setConnected(true);
      console.log('Socket connected');
    });

    newSocket.on('disconnect', () => {
      setConnected(false);
      console.log('Socket disconnected');
    });

    setSocket(newSocket);

    return () => newSocket.close();
  }, []);

  return { socket, connected };
};
```

#### Step 6: Create Chat Component with WebSocket (frontend/src/components/Chat.jsx)
```javascript
import React, { useState, useEffect, useRef } from 'react';
import { useSocket } from '../hooks/useSocket';
import { Box, TextField, Button, Typography, Paper, List, ListItem } from '@mui/material';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [typingUsers, setTypingUsers] = useState([]);
  const [onlineUsers, setOnlineUsers] = useState([]);
  const { socket, connected } = useSocket();
  const user = JSON.parse(localStorage.getItem('user'));
  const typingTimeoutRef = useRef(null);

  useEffect(() => {
    if (!socket) return;

    // Join chat
    socket.emit('join', { user_id: user.id });

    // Listen for new messages
    socket.on('new_message', (message) => {
      setMessages((prev) => [...prev, message]);
    });

    // Listen for typing indicators
    socket.on('user_typing', (data) => {
      setTypingUsers((prev) => [...prev, data.user_name]);
    });

    socket.on('user_stop_typing', (data) => {
      setTypingUsers((prev) => prev.filter(name => name !== data.user_name));
    });

    // Listen for user joined/left
    socket.on('user_joined', (data) => {
      setOnlineUsers(data.active_users);
    });

    socket.on('user_left', (data) => {
      setOnlineUsers((prev) => prev.filter(id => id !== data.user_id));
    });

    return () => {
      socket.off('new_message');
      socket.off('user_typing');
      socket.off('user_stop_typing');
      socket.off('user_joined');
      socket.off('user_left');
    };
  }, [socket]);

  const handleSend = () => {
    if (!inputMessage.trim()) return;
    
    socket.emit('send_message', {
      user_id: user.id,
      content: inputMessage
    });
    
    setInputMessage('');
    socket.emit('stop_typing', { user_id: user.id });
  };

  const handleTyping = (e) => {
    setInputMessage(e.target.value);
    
    socket.emit('typing', { user_id: user.id });
    
    clearTimeout(typingTimeoutRef.current);
    typingTimeoutRef.current = setTimeout(() => {
      socket.emit('stop_typing', { user_id: user.id });
    }, 1000);
  };

  return (
    <Box sx={{ display: 'flex', height: '100vh', p: 2 }}>
      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <Typography variant="h4" gutterBottom>
          💬 Chat en temps réel
        </Typography>
        <Typography variant="body2" color={connected ? 'success.main' : 'error.main'}>
          {connected ? '🟢 Connecté' : '🔴 Déconnecté'}
        </Typography>
        
        <Paper sx={{ flex: 1, overflow: 'auto', p: 2, my: 2 }}>
          <List>
            {messages.map((msg, idx) => (
              <ListItem key={idx}>
                <Box>
                  <Typography variant="subtitle2" color="primary">
                    {msg.user.nom}
                  </Typography>
                  <Typography variant="body1">{msg.content}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </Typography>
                </Box>
              </ListItem>
            ))}
          </List>
          {typingUsers.length > 0 && (
            <Typography variant="caption" color="text.secondary">
              {typingUsers.join(', ')} est en train d'écrire...
            </Typography>
          )}
        </Paper>
        
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            value={inputMessage}
            onChange={handleTyping}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Écrivez un message..."
          />
          <Button variant="contained" onClick={handleSend}>
            Envoyer
          </Button>
        </Box>
      </Box>
      
      <Paper sx={{ width: 250, ml: 2, p: 2 }}>
        <Typography variant="h6" gutterBottom>
          En ligne ({onlineUsers.length})
        </Typography>
        <List>
          {onlineUsers.map((userId) => (
            <ListItem key={userId}>
              <Typography variant="body2">👤 User {userId}</Typography>
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  );
}

export default Chat;
```

---

### Task 7: Notifications Push

**Implementation:**

#### Step 1: Create notification service (frontend/src/services/notificationService.js)
```javascript
export const requestNotificationPermission = async () => {
  if (!('Notification' in window)) {
    console.log('This browser does not support notifications');
    return false;
  }

  const permission = await Notification.requestPermission();
  return permission === 'granted';
};

export const showNotification = (title, options = {}) => {
  if (Notification.permission === 'granted') {
    new Notification(title, {
      icon: '/logo192.png',
      badge: '/logo192.png',
      ...options
    });
  }
};

export const subscribeToNotifications = async () => {
  try {
    const registration = await navigator.serviceWorker.register('/sw.js');
    
    const subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: process.env.REACT_APP_VAPID_PUBLIC_KEY
    });
    
    // Send subscription to backend
    await fetch(process.env.REACT_APP_API_URL + '/notifications/subscribe', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': +Bearer +localStorage.getItem('token')+
      },
      body: JSON.stringify(subscription)
    });
    
    return subscription;
  } catch (error) {
    console.error('Failed to subscribe to notifications:', error);
    return null;
  }
};
```

#### Step 2: Create service worker (frontend/public/sw.js)
```javascript
self.addEventListener('push', function(event) {
  const data = event.data.json();
  
  const options = {
    body: data.body,
    icon: '/logo192.png',
    badge: '/logo192.png',
    data: data.data,
    actions: data.actions || []
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  
  event.waitUntil(
    clients.openWindow(event.notification.data.url || '/')
  );
});
```

#### Step 3: Backend notification handler (backend/app/routes/notifications.py)
```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pywebpush import webpush, WebPushException
import os
import json

notifications_bp = Blueprint('notifications', __name__)

# Store subscriptions (in production, use database)
subscriptions = {}

@notifications_bp.route('/subscribe', methods=['POST'])
@jwt_required()
def subscribe():
    user_id = get_jwt_identity()
    subscription = request.get_json()
    
    subscriptions[user_id] = subscription
    
    return jsonify({'message': 'Subscribed successfully'}), 200

@notifications_bp.route('/send', methods=['POST'])
def send_notification():
    data = request.get_json()
    user_id = data['user_id']
    
    if user_id not in subscriptions:
        return jsonify({'error': 'User not subscribed'}), 404
    
    notification_data = {
        'title': data['title'],
        'body': data['body'],
        'data': data.get('data', {}),
    }
    
    try:
        webpush(
            subscription_info=subscriptions[user_id],
            data=json.dumps(notification_data),
            vapid_private_key=os.getenv('VAPID_PRIVATE_KEY'),
            vapid_claims={
                "sub": "mailto:your-email@example.com"
            }
        )
        return jsonify({'message': 'Notification sent'}), 200
    except WebPushException as ex:
        return jsonify({'error': str(ex)}), 500

# Example: Send badge notification
def notify_badge_earned(user_id, badge_name):
    if user_id in subscriptions:
        send_notification({
            'user_id': user_id,
            'title': '🎉 Nouveau badge débloqué!',
            'body': f'Vous avez gagné le badge: {badge_name}',
            'data': {'url': '/profile'}
        })
```

#### Step 4: Generate VAPID keys
```bash
pip install py-vapid
vapid --gen

# Add to .env
VAPID_PRIVATE_KEY=your-private-key
VAPID_PUBLIC_KEY=your-public-key
```

---

### Task 8: Édition du Profil Utilisateur

**Implementation:**

#### Step 1: Create Profile Edit Component (frontend/src/components/ProfileEdit.jsx)
```javascript
import React, { useState, useEffect } from 'react';
import { usersAPI } from '../services/api';
import {
  Box, TextField, Button, Avatar, Typography,
  Dialog, DialogTitle, DialogContent, DialogActions,
  Alert, CircularProgress
} from '@mui/material';

function ProfileEdit({ open, onClose, onSave }) {
  const [user, setUser] = useState(null);
  const [formData, setFormData] = useState({
    nom: '',
    email: '',
    promo: '',
    bio: '',
  });
  const [passwordData, setPasswordData] = useState({
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [avatar, setAvatar] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const currentUser = JSON.parse(localStorage.getItem('user'));
    setUser(currentUser);
    setFormData({
      nom: currentUser.nom || '',
      email: currentUser.email || '',
      promo: currentUser.promo || '',
      bio: currentUser.bio || '',
    });
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handlePasswordChange = (e) => {
    setPasswordData({ ...passwordData, [e.target.name]: e.target.value });
  };

  const handleAvatarChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setAvatar(file);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const formDataToSend = new FormData();
      Object.keys(formData).forEach(key => {
        formDataToSend.append(key, formData[key]);
      });
      
      if (avatar) {
        formDataToSend.append('avatar', avatar);
      }

      const response = await usersAPI.update(user.id, formDataToSend);
      
      localStorage.setItem('user', JSON.stringify(response.data));
      setSuccess('Profil mis à jour avec succès!');
      
      setTimeout(() => {
        onSave(response.data);
        onClose();
      }, 1500);
    } catch (err) {
      setError('Erreur lors de la mise à jour du profil');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordSubmit = async () => {
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setError('Les mots de passe ne correspondent pas');
      return;
    }

    if (passwordData.newPassword.length < 8) {
      setError('Le mot de passe doit contenir au moins 8 caractères');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await usersAPI.changePassword(user.id, {
        old_password: passwordData.oldPassword,
        new_password: passwordData.newPassword
      });
      
      setSuccess('Mot de passe changé avec succès!');
      setPasswordData({ oldPassword: '', newPassword: '', confirmPassword: '' });
    } catch (err) {
      setError('Erreur lors du changement de mot de passe');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>✏️ Modifier le profil</DialogTitle>
      <DialogContent>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 3 }}>
          <Avatar
            src={avatar ? URL.createObjectURL(avatar) : user?.avatar}
            sx={{ width: 120, height: 120, mb: 2 }}
          />
          <Button variant="outlined" component="label">
            Changer l'avatar
            <input type="file" hidden accept="image/*" onChange={handleAvatarChange} />
          </Button>
        </Box>

        <Typography variant="h6" gutterBottom>Informations personnelles</Typography>
        <TextField
          fullWidth
          name="nom"
          label="Nom"
          value={formData.nom}
          onChange={handleChange}
          margin="normal"
        />
        <TextField
          fullWidth
          name="email"
          label="Email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          margin="normal"
        />
        <TextField
          fullWidth
          name="promo"
          label="Promo"
          value={formData.promo}
          onChange={handleChange}
          margin="normal"
        />
        <TextField
          fullWidth
          name="bio"
          label="Bio"
          multiline
          rows={4}
          value={formData.bio}
          onChange={handleChange}
          margin="normal"
        />

        <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
          Changer le mot de passe
        </Typography>
        <TextField
          fullWidth
          name="oldPassword"
          label="Ancien mot de passe"
          type="password"
          value={passwordData.oldPassword}
          onChange={handlePasswordChange}
          margin="normal"
        />
        <TextField
          fullWidth
          name="newPassword"
          label="Nouveau mot de passe"
          type="password"
          value={passwordData.newPassword}
          onChange={handlePasswordChange}
          margin="normal"
        />
        <TextField
          fullWidth
          name="confirmPassword"
          label="Confirmer le mot de passe"
          type="password"
          value={passwordData.confirmPassword}
          onChange={handlePasswordChange}
          margin="normal"
        />
        <Button
          variant="outlined"
          onClick={handlePasswordSubmit}
          disabled={loading || !passwordData.oldPassword}
          sx={{ mt: 1 }}
        >
          Changer le mot de passe
        </Button>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Annuler</Button>
        <Button
          variant="contained"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : 'Enregistrer'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default ProfileEdit;
```

#### Step 2: Backend profile update endpoint (backend/app/routes/users.py)
```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db, bcrypt
from app.models.user import User
import os

users_bp = Blueprint('users', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Handle file upload
    if 'avatar' in request.files:
        file = request.files['avatar']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"user_{user_id}_{file.filename}")
            upload_folder = os.path.join('static', 'avatars')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            user.avatar = f'/static/avatars/{filename}'
    
    # Update other fields
    data = request.form if request.files else request.get_json()
    
    if 'nom' in data:
        user.nom = data['nom']
    if 'email' in data:
        user.email = data['email']
    if 'promo' in data:
        user.promo = data['promo']
    if 'bio' in data:
        user.bio = data['bio']
    
    db.session.commit()
    
    return jsonify(user.to_dict()), 200

@users_bp.route('/<int:user_id>/change-password', methods=['POST'])
@jwt_required()
def change_password(user_id):
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
```

---

### Task 9: Tableau de Bord Analytique Avancé

**Implementation:**

#### Step 1: Install chart library
```bash
npm install recharts
```

#### Step 2: Create Analytics Component (frontend/src/components/Analytics.jsx)
```javascript
import React, { useState, useEffect } from 'react';
import { usersAPI } from '../services/api';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell
} from 'recharts';
import {
  Box, Typography, Paper, Grid, Select, MenuItem,
  FormControl, InputLabel, Button
} from '@mui/material';
import { jsPDF } from 'jspdf';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

function Analytics() {
  const [timeRange, setTimeRange] = useState('month');
  const [xpData, setXpData] = useState([]);
  const [projectsData, setProjectsData] = useState([]);
  const [activityData, setActivityData] = useState([]);
  const [stats, setStats] = useState({});

  useEffect(() => {
    fetchAnalytics();
  }, [timeRange]);

  const fetchAnalytics = async () => {
    try {
      const user = JSON.parse(localStorage.getItem('user'));
      const response = await usersAPI.getAnalytics(user.id, timeRange);
      
      setXpData(response.data.xp_history);
      setProjectsData(response.data.projects_by_status);
      setActivityData(response.data.activity_by_day);
      setStats(response.data.stats);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  const exportToPDF = () => {
    const doc = new jsPDF();
    
    doc.setFontSize(20);
    doc.text('Rapport d\'Analytique', 20, 20);
    
    doc.setFontSize(12);
    doc.text(Total XP: +stats.total_xp+`, 20, 40);
    doc.text(Projets complétés: +stats.completed_projects+`, 20, 50);
    doc.text(Badges gagnés: +stats.total_badges+`, 20, 60);
    doc.text(Temps sur la plateforme: +stats.time_spent+ heures, 20, 70);
    
    doc.save('analytics-report.pdf');
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">📊 Tableau de bord analytique</Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <FormControl sx={{ minWidth: 120 }}>
            <InputLabel>Période</InputLabel>
            <Select
              value={timeRange}
              label="Période"
              onChange={(e) => setTimeRange(e.target.value)}
            >
              <MenuItem value="week">Semaine</MenuItem>
              <MenuItem value="month">Mois</MenuItem>
              <MenuItem value="year">Année</MenuItem>
            </Select>
          </FormControl>
          <Button variant="contained" onClick={exportToPDF}>
            📄 Exporter PDF
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Stats Cards */}
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h4" color="primary">{stats.total_xp || 0}</Typography>
            <Typography variant="body2">Total XP</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h4" color="success.main">
              {stats.completed_projects || 0}
            </Typography>
            <Typography variant="body2">Projets complétés</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h4" color="warning.main">
              {stats.total_badges || 0}
            </Typography>
            <Typography variant="body2">Badges gagnés</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h4" color="info.main">
              {stats.time_spent || 0}h
            </Typography>
            <Typography variant="body2">Temps total</Typography>
          </Paper>
        </Grid>

        {/* XP Over Time Chart */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>XP au fil du temps</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={xpData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="xp" stroke="#8884d8" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Projects by Status */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Projets par statut</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={projectsData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {projectsData.map((entry, index) => (
                    <Cell key={+cell-+index+`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Activity by Day */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Activité par jour</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={activityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="activity" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Analytics;
```

#### Step 3: Backend analytics endpoint (backend/app/routes/users.py)
```python
@users_bp.route('/<int:user_id>/analytics', methods=['GET'])
@jwt_required()
def get_analytics(user_id):
    current_user_id = get_jwt_identity()
    
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    time_range = request.args.get('range', 'month')
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Calculate date range
    from datetime import datetime, timedelta
    
    if time_range == 'week':
        start_date = datetime.utcnow() - timedelta(days=7)
    elif time_range == 'month':
        start_date = datetime.utcnow() - timedelta(days=30)
    else:  # year
        start_date = datetime.utcnow() - timedelta(days=365)
    
    # Get XP history
    xp_history = db.session.query(
        db.func.date(XPLog.created_at).label('date'),
        db.func.sum(XPLog.amount).label('xp')
    ).filter(
        XPLog.user_id == user_id,
        XPLog.created_at >= start_date
    ).group_by('date').all()
    
    # Get projects by status
    projects_by_status = db.session.query(
        Projet.statut,
        db.func.count(Projet.id)
    ).filter(
        Projet.user_id == user_id
    ).group_by(Projet.statut).all()
    
    # Calculate stats
    total_projects = len(user.projets)
    completed_projects = len([p for p in user.projets if p.statut == 'termine'])
    
    return jsonify({
        'xp_history': [{'date': str(h[0]), 'xp': h[1]} for h in xp_history],
        'projects_by_status': [
            {'name': s[0], 'value': s[1]} for s in projects_by_status
        ],
        'stats': {
            'total_xp': user.xp,
            'completed_projects': completed_projects,
            'total_badges': len(user.badges),
            'time_spent': calculate_time_spent(user_id)
        }
    }), 200
```

---

### Task 10: Fonctionnalité de Réinitialisation de Mot de Passe

**Implementation:**

#### Step 1: Install email library
```bash
pip install flask-mail
```

#### Step 2: Configure Flask-Mail (backend/app/__init__.py)
```python
from flask_mail import Mail

mail = Mail()

def create_app():
    # ...
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    
    mail.init_app(app)
    # ...
```

#### Step 3: Create password reset endpoints (backend/app/routes/auth.py)
```python
from flask_mail import Message
from app import mail
from itsdangerous import URLSafeTimedSerializer
import os

serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'If email exists, reset link sent'}), 200
    
    # Generate reset token
    token = serializer.dumps(email, salt='password-reset-salt')
    
    # Create reset link
    reset_url = f"{os.getenv('FRONTEND_URL')}/reset-password?token={token}"
    
    # Send email
    msg = Message(
        'Réinitialisation de mot de passe',
        recipients=[email]
    )
    msg.body = f'''Bonjour {user.nom},

Vous avez demandé une réinitialisation de mot de passe.
Cliquez sur le lien ci-dessous pour réinitialiser votre mot de passe:

{reset_url}

Ce lien expirera dans 1 heure.

Si vous n'avez pas fait cette demande, ignorez cet email.
'''
    
    mail.send(msg)
    
    return jsonify({'message': 'Reset link sent to email'}), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')
    
    try:
        # Verify token (expires after 1 hour)
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        return jsonify({'error': 'Invalid or expired token'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Update password
    user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()
    
    # Send confirmation email
    msg = Message(
        'Mot de passe modifié',
        recipients=[email]
    )
    msg.body = f'''Bonjour {user.nom},

Votre mot de passe a été modifié avec succès.

Si vous n'avez pas effectué cette action, contactez-nous immédiatement.
'''
    mail.send(msg)
    
    return jsonify({'message': 'Password reset successfully'}), 200
```

#### Step 4: Create Forgot Password Component (frontend/src/components/ForgotPassword.jsx)
```javascript
import React, { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { authAPI } from '../services/api';
import {
  Container, Box, Typography, TextField, Button, Alert
} from '@mui/material';

function ForgotPassword() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRequestReset = async (e) => {
    e.preventDefault();
    try {
      await authAPI.forgotPassword({ email });
      setMessage('Un lien de réinitialisation a été envoyé à votre email');
      setError('');
    } catch (err) {
      setError('Erreur lors de l\'envoi du lien');
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      setError('Les mots de passe ne correspondent pas');
      return;
    }

    try {
      await authAPI.resetPassword({ token, password });
      setMessage('Mot de passe réinitialisé avec succès');
      setError('');
      
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError('Le lien est invalide ou expiré');
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8 }}>
        <Typography variant="h4" gutterBottom>
          {token ? 'Nouveau mot de passe' : 'Mot de passe oublié'}
        </Typography>
        
        {message && <Alert severity="success" sx={{ mb: 2 }}>{message}</Alert>}
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        {!token ? (
          <Box component="form" onSubmit={handleRequestReset} sx={{ mt: 3 }}>
            <TextField
              fullWidth
              label="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              margin="normal"
              required
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3 }}
            >
              Envoyer le lien
            </Button>
          </Box>
        ) : (
          <Box component="form" onSubmit={handleResetPassword} sx={{ mt: 3 }}>
            <TextField
              fullWidth
              label="Nouveau mot de passe"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Confirmer le mot de passe"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              margin="normal"
              required
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3 }}
            >
              Réinitialiser
            </Button>
          </Box>
        )}
      </Box>
    </Container>
  );
}

export default ForgotPassword;
```

---

## 🔵 AMÉLIORATIONS FUTURES (AGRÉABLE À AVOIR)

### Task 11: Application Mobile (React Native)

**Implementation:**

#### Step 1: Initialize React Native project
```bash
npx react-native init PlateformeXPMobile
cd PlateformeXPMobile
npm install @react-navigation/native @react-navigation/native-stack
npm install react-native-screens react-native-safe-area-context
npm install axios react-native-async-storage
npm install react-native-biometrics react-native-camera
```

#### Step 2: Create API service (src/services/api.js)
```javascript
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = 'https://your-api.herokuapp.com/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem('token');
  if (token) {
    config.headers.Authorization = +Bearer +token+`;
  }
  return config;
});

export default api;
```

#### Step 3: Implement biometric authentication (src/services/biometric.js)
```javascript
import ReactNativeBiometrics from 'react-native-biometrics';

export const authenticateWithBiometrics = async () => {
  try {
    const { available, biometryType } = await ReactNativeBiometrics.isSensorAvailable();
    
    if (!available) {
      return { success: false, error: 'Biometrics not available' };
    }

    const { success } = await ReactNativeBiometrics.simplePrompt({
      promptMessage: 'Authentification',
      cancelButtonText: 'Annuler'
    });

    return { success };
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

#### Step 4: Create Login Screen with biometrics (src/screens/LoginScreen.js)
```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { authenticateWithBiometrics } from '../services/biometric';
import api from '../services/api';

const LoginScreen = ({ navigation }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [biometricAvailable, setBiometricAvailable] = useState(false);

  useEffect(() => {
    checkBiometrics();
  }, []);

  const checkBiometrics = async () => {
    const hasBiometric = await AsyncStorage.getItem('biometric_enabled');
    setBiometricAvailable(!!hasBiometric);
  };

  const handleLogin = async () => {
    try {
      const response = await api.post('/auth/login', { email, password });
      await AsyncStorage.setItem('token', response.data.access_token);
      await AsyncStorage.setItem('user', JSON.stringify(response.data.user));
      navigation.navigate('Dashboard');
    } catch (error) {
      alert('Identifiants invalides');
    }
  };

  const handleBiometricLogin = async () => {
    const result = await authenticateWithBiometrics();
    if (result.success) {
      navigation.navigate('Dashboard');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>🎮 Plateforme XP</Text>
      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
      />
      <TextInput
        style={styles.input}
        placeholder="Mot de passe"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <TouchableOpacity style={styles.button} onPress={handleLogin}>
        <Text style={styles.buttonText}>Se connecter</Text>
      </TouchableOpacity>
      {biometricAvailable && (
        <TouchableOpacity style={styles.biometricButton} onPress={handleBiometricLogin}>
          <Text style={styles.buttonText}>👆 Connexion biométrique</Text>
        </TouchableOpacity>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 40,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 15,
    marginBottom: 15,
    fontSize: 16,
  },
  button: {
    backgroundColor: '#48bb78',
    padding: 15,
    borderRadius: 8,
    marginTop: 10,
  },
  biometricButton: {
    backgroundColor: '#4a9eff',
    padding: 15,
    borderRadius: 8,
    marginTop: 10,
  },
  buttonText: {
    color: '#fff',
    textAlign: 'center',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default LoginScreen;
```

---

### Task 12: Réservation de Sessions de Tutorat

**Implementation:**

#### Backend Model (backend/app/models/tutoring.py)
```python
from app import db
from datetime import datetime

class TutorProfile(db.Model):
    __tablename__ = 'tutor_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    competences = db.Column(db.JSON)
    disponibilite = db.Column(db.JSON)
    tarif_horaire = db.Column(db.Float)
    rating = db.Column(db.Float, default=0.0)
    total_sessions = db.Column(db.Integer, default=0)
    
    sessions = db.relationship('TutoringSession', backref='tutor', lazy=True)

class TutoringSession(db.Model):
    __tablename__ = 'tutoring_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor_profiles.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(100))
    scheduled_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, default=60)  # minutes
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    meeting_link = db.Column(db.String(255))
    rating = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

#### Backend Routes (backend/app/routes/tutoring.py)
```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.tutoring import TutorProfile, TutoringSession
from app.models.user import User
from datetime import datetime, timedelta

tutoring_bp = Blueprint('tutoring', __name__)

@tutoring_bp.route('/tutors', methods=['GET'])
@jwt_required()
def get_tutors():
    subject = request.args.get('subject')
    
    query = TutorProfile.query
    
    if subject:
        query = query.filter(TutorProfile.competences.contains([subject]))
    
    tutors = query.all()
    
    result = []
    for tutor in tutors:
        user = User.query.get(tutor.user_id)
        result.append({
            'id': tutor.id,
            'user': user.to_dict(),
            'competences': tutor.competences,
            'rating': tutor.rating,
            'total_sessions': tutor.total_sessions
        })
    
    return jsonify(result), 200

@tutoring_bp.route('/sessions/book', methods=['POST'])
@jwt_required()
def book_session():
    student_id = get_jwt_identity()
    data = request.get_json()
    
    session = TutoringSession(
        tutor_id=data['tutor_id'],
        student_id=student_id,
        subject=data['subject'],
        scheduled_time=datetime.fromisoformat(data['scheduled_time']),
        duration=data.get('duration', 60)
    )
    
    db.session.add(session)
    db.session.commit()
    
    # Send email notifications
    # ... email logic ...
    
    return jsonify({
        'message': 'Session booked successfully',
        'session_id': session.id
    }), 201

@tutoring_bp.route('/sessions/<int:session_id>/rate', methods=['POST'])
@jwt_required()
def rate_session(session_id):
    data = request.get_json()
    
    session = TutoringSession.query.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    
    session.rating = data['rating']
    session.feedback = data.get('feedback', '')
    session.status = 'completed'
    
    # Update tutor rating
    tutor = TutorProfile.query.get(session.tutor_id)
    total_ratings = tutor.total_sessions * tutor.rating
    tutor.total_sessions += 1
    tutor.rating = (total_ratings + data['rating']) / tutor.total_sessions
    
    db.session.commit()
    
    return jsonify({'message': 'Session rated successfully'}), 200
```

#### Frontend Component (frontend/src/components/Tutoring.jsx)
```javascript
import React, { useState, useEffect } from 'react';
import { tutoringAPI } from '../services/api';
import {
  Box, Grid, Card, CardContent, Typography, Button,
  Dialog, DialogTitle, DialogContent, TextField,
  Rating, Avatar, Chip
} from '@mui/material';
import { DateTimePicker } from '@mui/x-date-pickers';

function Tutoring() {
  const [tutors, setTutors] = useState([]);
  const [selectedTutor, setSelectedTutor] = useState(null);
  const [bookingOpen, setBookingOpen] = useState(false);
  const [bookingData, setBookingData] = useState({
    subject: '',
    scheduledTime: new Date(),
    duration: 60
  });

  useEffect(() => {
    fetchTutors();
  }, []);

  const fetchTutors = async () => {
    try {
      const response = await tutoringAPI.getTutors();
      setTutors(response.data);
    } catch (error) {
      console.error('Error fetching tutors:', error);
    }
  };

  const handleBookSession = async () => {
    try {
      await tutoringAPI.bookSession({
        tutor_id: selectedTutor.id,
        ...bookingData
      });
      alert('Session réservée avec succès!');
      setBookingOpen(false);
    } catch (error) {
      alert('Erreur lors de la réservation');
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        👨‍🏫 Réservation de Sessions de Tutorat
      </Typography>

      <Grid container spacing={3}>
        {tutors.map((tutor) => (
          <Grid item xs={12} md={4} key={tutor.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar src={tutor.user.avatar} sx={{ mr: 2 }} />
                  <Box>
                    <Typography variant="h6">{tutor.user.nom}</Typography>
                    <Rating value={tutor.rating} readOnly size="small" />
                  </Box>
                </Box>
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {tutor.total_sessions} sessions complétées
                </Typography>
                
                <Box sx={{ mt: 2, mb: 2 }}>
                  {tutor.competences.map((comp, idx) => (
                    <Chip key={idx} label={comp} size="small" sx={{ mr: 1, mb: 1 }} />
                  ))}
                </Box>
                
                <Button
                  variant="contained"
                  fullWidth
                  onClick={() => {
                    setSelectedTutor(tutor);
                    setBookingOpen(true);
                  }}
                >
                  Réserver
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={bookingOpen} onClose={() => setBookingOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Réserver une session</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Sujet"
            value={bookingData.subject}
            onChange={(e) => setBookingData({...bookingData, subject: e.target.value})}
            margin="normal"
          />
          <DateTimePicker
            label="Date et heure"
            value={bookingData.scheduledTime}
            onChange={(newValue) => setBookingData({...bookingData, scheduledTime: newValue})}
            renderInput={(params) => <TextField {...params} fullWidth margin="normal" />}
          />
          <TextField
            fullWidth
            label="Durée (minutes)"
            type="number"
            value={bookingData.duration}
            onChange={(e) => setBookingData({...bookingData, duration: parseInt(e.target.value)})}
            margin="normal"
          />
          <Button
            variant="contained"
            fullWidth
            onClick={handleBookSession}
            sx={{ mt: 2 }}
          >
            Confirmer la réservation
          </Button>
        </DialogContent>
      </Dialog>
    </Box>
  );
}

export default Tutoring;
```

---

### Task 13: Création/Gestion de Tournois

**Implementation:**

#### Backend Model (backend/app/models/tournament.py)
```python
from app import db
from datetime import datetime

class Tournament(db.Model):
    __tablename__ = 'tournaments'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    format = db.Column(db.String(20))  # solo, team
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime, nullable=False)
    max_participants = db.Column(db.Integer)
    prize_xp = db.Column(db.Integer)
    status = db.Column(db.String(20), default='upcoming')  # upcoming, active, completed
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    participants = db.relationship('TournamentParticipant', backref='tournament', lazy=True)
    problems = db.relationship('TournamentProblem', backref='tournament', lazy=True)

class TournamentParticipant(db.Model):
    __tablename__ = 'tournament_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    rank = db.Column(db.Integer)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

class TournamentProblem(db.Model):
    __tablename__ = 'tournament_problems'
    
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    points = db.Column(db.Integer, default=100)
    difficulty = db.Column(db.String(20))
```

#### Backend Routes (backend/app/routes/tournaments.py)
```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.tournament import Tournament, TournamentParticipant, TournamentProblem
from datetime import datetime

tournaments_bp = Blueprint('tournaments', __name__)

@tournaments_bp.route('/', methods=['GET'])
def get_tournaments():
    status = request.args.get('status', 'active')
    
    tournaments = Tournament.query.filter_by(status=status).all()
    
    return jsonify([{
        'id': t.id,
        'nom': t.nom,
        'description': t.description,
        'format': t.format,
        'date_debut': t.date_debut.isoformat(),
        'date_fin': t.date_fin.isoformat(),
        'participants_count': len(t.participants),
        'max_participants': t.max_participants
    } for t in tournaments]), 200

@tournaments_bp.route('/', methods=['POST'])
@jwt_required()
def create_tournament():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    tournament = Tournament(
        nom=data['nom'],
        description=data.get('description', ''),
        format=data.get('format', 'solo'),
        date_debut=datetime.fromisoformat(data['date_debut']),
        date_fin=datetime.fromisoformat(data['date_fin']),
        max_participants=data.get('max_participants'),
        prize_xp=data.get('prize_xp', 0),
        created_by=user_id
    )
    
    db.session.add(tournament)
    db.session.commit()
    
    return jsonify({
        'message': 'Tournament created successfully',
        'tournament_id': tournament.id
    }), 201

@tournaments_bp.route('/<int:tournament_id>/join', methods=['POST'])
@jwt_required()
def join_tournament(tournament_id):
    user_id = get_jwt_identity()
    
    tournament = Tournament.query.get(tournament_id)
    if not tournament:
        return jsonify({'error': 'Tournament not found'}), 404
    
    # Check if already joined
    existing = TournamentParticipant.query.filter_by(
        tournament_id=tournament_id,
        user_id=user_id
    ).first()
    
    if existing:
        return jsonify({'error': 'Already joined'}), 400
    
    # Check max participants
    if tournament.max_participants and len(tournament.participants) >= tournament.max_participants:
        return jsonify({'error': 'Tournament is full'}), 400
    
    participant = TournamentParticipant(
        tournament_id=tournament_id,
        user_id=user_id
    )
    
    db.session.add(participant)
    db.session.commit()
    
    return jsonify({'message': 'Joined tournament successfully'}), 200

@tournaments_bp.route('/<int:tournament_id>/leaderboard', methods=['GET'])
def get_leaderboard(tournament_id):
    participants = TournamentParticipant.query.filter_by(
        tournament_id=tournament_id
    ).order_by(TournamentParticipant.score.desc()).all()
    
    return jsonify([{
        'rank': idx + 1,
        'user_id': p.user_id,
        'score': p.score
    } for idx, p in enumerate(participants)]), 200
```

---

### Task 14: Coach de Carrière IA

**Implementation:**

#### Step 1: Install OpenAI SDK
```bash
pip install openai
```

#### Step 2: Create AI Coach service (backend/app/services/ai_coach.py)
```python
import openai
import os
from app.models.user import User
from app.models.projet import Projet

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_career_advice(user_id, question):
    user = User.query.get(user_id)
    projects = Projet.query.filter_by(user_id=user_id).all()
    
    # Build context
    context = f"""
    User Profile:
    - Name: {user.nom}
    - XP Level: {user.xp}
    - Niveau: {user.niveau}
    - Promo: {user.promo}
    
    Completed Projects:
    """
    
    for project in projects:
        if project.statut == 'termine':
            context += f"- {project.titre} ({', '.join(project.technos or [])})\n"
    
    context += f"\nUser Question: {question}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a career coach for tech students. Provide personalized advice based on their completed projects and skill level."
                },
                {
                    "role": "user",
                    "content": context
                }
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_skill_gaps(user_id):
    user = User.query.get(user_id)
    projects = Projet.query.filter_by(user_id=user_id).all()
    
    # Extract user skills
    user_skills = set()
    for project in projects:
        if project.technos:
            user_skills.update(project.technos)
    
    # Define market trends (could be fetched from API)
    trending_skills = {
        'Python', 'JavaScript', 'React', 'Node.js', 'Docker',
        'Kubernetes', 'AWS', 'Machine Learning', 'TypeScript'
    }
    
    missing_skills = trending_skills - user_skills
    
    return {
        'current_skills': list(user_skills),
        'missing_skills': list(missing_skills),
        'recommendations': [
            f"Learn {skill} to stay competitive" for skill in list(missing_skills)[:3]
        ]
    }
```

#### Step 3: Create AI Coach endpoints (backend/app/routes/ai_coach.py)
```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.ai_coach import get_career_advice, analyze_skill_gaps

ai_coach_bp = Blueprint('ai_coach', __name__)

@ai_coach_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    user_id = get_jwt_identity()
    data = request.get_json()
    question = data.get('question', '')
    
    response = get_career_advice(user_id, question)
    
    return jsonify({'response': response}), 200

@ai_coach_bp.route('/skill-analysis', methods=['GET'])
@jwt_required()
def skill_analysis():
    user_id = get_jwt_identity()
    
    analysis = analyze_skill_gaps(user_id)
    
    return jsonify(analysis), 200
```

#### Step 4: Frontend AI Coach Component (frontend/src/components/AICoach.jsx)
```javascript
import React, { useState } from 'react';
import { aiCoachAPI } from '../services/api';
import {
  Box, TextField, Button, Paper, Typography,
  List, ListItem, CircularProgress, Chip
} from '@mui/material';

function AICoach() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [skillAnalysis, setSkillAnalysis] = useState(null);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMessage = { role: 'user', content: input };
    setMessages([...messages, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await aiCoachAPI.chat({ question: input });
      const aiMessage = { role: 'assistant', content: response.data.response };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSkillAnalysis = async () => {
    setLoading(true);
    try {
      const response = await aiCoachAPI.getSkillAnalysis();
      setSkillAnalysis(response.data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        🤖 Coach de Carrière IA
      </Typography>

      <Button
        variant="outlined"
        onClick={handleSkillAnalysis}
        disabled={loading}
        sx={{ mb: 3 }}
      >
        Analyser mes compétences
      </Button>

      {skillAnalysis && (
        <Paper sx={{ p: 2, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Analyse de compétences
          </Typography>
          <Typography variant="subtitle2" gutterBottom>
            Compétences actuelles:
          </Typography>
          <Box sx={{ mb: 2 }}>
            {skillAnalysis.current_skills.map((skill, idx) => (
              <Chip key={idx} label={skill} color="success" sx={{ mr: 1, mb: 1 }} />
            ))}
          </Box>
          <Typography variant="subtitle2" gutterBottom>
            Compétences recommandées:
          </Typography>
          <Box>
            {skillAnalysis.missing_skills.map((skill, idx) => (
              <Chip key={idx} label={skill} color="warning" sx={{ mr: 1, mb: 1 }} />
            ))}
          </Box>
        </Paper>
      )}

      <Paper sx={{ p: 2, height: 400, overflow: 'auto', mb: 2 }}>
        <List>
          {messages.map((msg, idx) => (
            <ListItem
              key={idx}
              sx={{
                justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start'
              }}
            >
              <Paper
                sx={{
                  p: 2,
                  maxWidth: '70%',
                  bgcolor: msg.role === 'user' ? 'primary.main' : 'grey.200',
                  color: msg.role === 'user' ? 'white' : 'text.primary'
                }}
              >
                <Typography variant="body1">{msg.content}</Typography>
              </Paper>
            </ListItem>
          ))}
          {loading && (
            <ListItem>
              <CircularProgress size={24} />
            </ListItem>
          )}
        </List>
      </Paper>

      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Posez une question sur votre carrière..."
        />
        <Button variant="contained" onClick={handleSend} disabled={loading}>
          Envoyer
        </Button>
      </Box>
    </Box>
  );
}

export default AICoach;
```

---

