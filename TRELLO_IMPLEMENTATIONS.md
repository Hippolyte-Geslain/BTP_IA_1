# 🚀 IMPLEMENTATIONS DES TÂCHES TRELLO

**Date:** 2025-10-30  
**Status:** En cours  
**Documentation:** Solutions détaillées pour chaque tâche

---

## 📋 TABLE DES MATIÈRES

- [Tâches Critiques](#-critique-mvp)
- [Tâches Moyennes](#-priorité-moyenne)
- [Améliorations Futures](#-améliorations-futures)
- [DevOps & Production](#-devops--production)

---

## 🔴 CRITIQUE (MVP)

### ✅ TÂCHE 1: API Backend (Flask + PostgreSQL)

**Status:** ✅ Implémenté

#### Solution Complète

**Fichier:** `backend/run.py`
```python
from app import create_app, db
from dotenv import load_dotenv
import socket

load_dotenv()
app = create_app()

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if __name__ == '__main__':
    # Auto-detect available port
    port = 5001 if is_port_in_use(5000) else 5000
    
    with app.app_context():
        db.create_all()
        print("✅ Database tables created")
    
    print(f"🚀 Starting Plateforme XP Backend on port {port}...")
    app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)
```

**Fichier:** `backend/app/__init__.py`
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
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///plateforme_xp.db')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)
    
    # Register blueprints
    with app.app_context():
        from app.routes import auth, users, projets, chat
        app.register_blueprint(auth.auth_bp, url_prefix='/api/auth')
        app.register_blueprint(users.users_bp, url_prefix='/api/users')
        app.register_blueprint(projets.projets_bp, url_prefix='/api/projets')
        app.register_blueprint(chat.chat_bp, url_prefix='/api/chat')
    
    return app
```

**Commande d'installation:**
```bash
cd backend
pip install flask flask-sqlalchemy flask-jwt-extended flask-cors flask-bcrypt python-dotenv
python run.py
```

**Test avec curl:**
```bash
# Health check
curl http://localhost:5000/health

# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nom":"Test User","email":"test@test.com","password":"test123"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```

---

### ✅ TÂCHE 2: Interface Web (React)

**Status:** ✅ Implémenté

#### Solution Complète

**Fichier:** `frontend/src/App.js`
```javascript
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

// Import components
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import Projects from './components/Projects';
import Chat from './components/Chat';
import Leaderboard from './components/Leaderboard';
import Profile from './components/Profile';
import Calendar from './components/Calendar';
import Badges from './components/Badges';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#2b6cb0' },
    secondary: { main: '#48bb78' },
  },
});

function App() {
  const isAuthenticated = () => !!localStorage.getItem('token');
  
  const ProtectedRoute = ({ children }) => {
    return isAuthenticated() ? children : <Navigate to="/login" />;
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/projects" element={<ProtectedRoute><Projects /></ProtectedRoute>} />
          <Route path="/chat" element={<ProtectedRoute><Chat /></ProtectedRoute>} />
          <Route path="/leaderboard" element={<ProtectedRoute><Leaderboard /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          <Route path="/badges" element={<ProtectedRoute><Badges /></ProtectedRoute>} />
          <Route path="/calendar" element={<ProtectedRoute><Calendar /></ProtectedRoute>} />
          <Route path="/" element={<Navigate to="/dashboard" />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
```

**Fichier:** `frontend/src/services/api.js`
```javascript
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' }
});

// Add token to requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
};

export const usersAPI = {
  getProfile: () => api.get('/users/profile'),
  updateProfile: (data) => api.put('/users/profile', data),
  getLeaderboard: () => api.get('/users/leaderboard'),
};

export const projetsAPI = {
  getAll: () => api.get('/projets'),
  complete: (id) => api.post(`/projets/${id}/complete`),
};

export const chatAPI = {
  getMessages: () => api.get('/chat/messages'),
  sendMessage: (message) => api.post('/chat/messages', { message }),
};

export default api;
```

**Commandes d'installation:**
```bash
cd frontend
npm install react react-dom react-router-dom @mui/material @emotion/react @emotion/styled axios
npm start
```

---

### ✅ TÂCHE 3: Authentification JWT

**Status:** ✅ Implémenté

#### Solution Complète

**Fichier:** `backend/app/routes/auth.py`
```python
from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models.user import User
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validation
    if not all(k in data for k in ['nom', 'email', 'password']):
        return jsonify({'error': 'Missing fields'}), 400
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Hash password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    # Create user
    user = User(
        nom=data['nom'],
        email=data['email'],
        password=hashed_password,
        promotion=data.get('promotion', 'B2')
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Generate token
    token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(hours=1)
    )
    
    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validation
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'error': 'Missing credentials'}), 400
    
    # Find user
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Generate token
    token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(hours=1)
    )
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    }), 200
```

**Fichier:** `backend/app/middleware/auth.py`
```python
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User

def jwt_required_custom():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                user = User.query.get(current_user_id)
                if not user:
                    return jsonify({'error': 'User not found'}), 404
                return f(current_user=user, *args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'Invalid or expired token'}), 401
        return wrapper
    return decorator
```

**Test:**
```bash
# Login and save token
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}' \
  | jq -r '.token')

# Use token
curl http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer $TOKEN"
```

---

### ⚠️ TÂCHE 4: Migration depuis JSON

**Status:** ⚠️ Partiellement implémenté

#### Solution

**Fichier:** `backend/migrate_json_to_db.py`
```python
import json
from app import create_app, db
from app.models.user import User
from app.models.projet import Projet
from app.models.message import Message

def migrate_json_to_db():
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Load JSON data
        with open('../plateforme_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Migrate users
        print("Migrating users...")
        for email, user_data in data.get('utilisateurs', {}).items():
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(
                    nom=user_data['nom'],
                    email=email,
                    password='hashed_password_placeholder',
                    promotion=user_data.get('promotion', 'B2'),
                    xp=user_data.get('xp', 0),
                    niveau=user_data.get('niveau', 1)
                )
                db.session.add(user)
        
        db.session.commit()
        print(f"✅ Migrated {User.query.count()} users")
        
        # Migrate chat messages
        print("Migrating chat messages...")
        for msg_data in data.get('messages_chat', []):
            message = Message(
                message=msg_data['message'],
                timestamp=msg_data['timestamp'],
                user_id=1  # Default user for now
            )
            db.session.add(message)
        
        db.session.commit()
        print(f"✅ Migrated {Message.query.count()} messages")
        
        print("✅ Migration complete!")

if __name__ == '__main__':
    migrate_json_to_db()
```

**Commande:**
```bash
cd backend
python migrate_json_to_db.py
```

---

### ⚠️ TÂCHE 5: Déploiement Cloud

**Status:** ⚠️ Prêt pour déploiement

#### Solution - Heroku

**Fichier:** `backend/Procfile`
```
web: python run.py
```

**Fichier:** `backend/runtime.txt`
```
python-3.10.0
```

**Commandes:**
```bash
# Install Heroku CLI
# heroku.com/install

# Login
heroku login

# Create app
heroku create plateforme-xp-backend

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set env vars
heroku config:set SECRET_KEY=your-secret-key
heroku config:set JWT_SECRET_KEY=your-jwt-key

# Deploy
git push heroku main

# Check logs
heroku logs --tail
```

#### Solution - Vercel (Frontend)

**Fichier:** `frontend/vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": { "distDir": "build" }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "env": {
    "REACT_APP_API_URL": "https://plateforme-xp-backend.herokuapp.com/api"
  }
}
```

**Commandes:**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

---

## 🟡 PRIORITÉ MOYENNE

### ⚠️ TÂCHE 6: WebSockets en Temps Réel

**Status:** ⚠️ À améliorer (actuellement polling)

#### Solution avec Socket.IO

**Backend:** `backend/app/sockets/__init__.py`
```python
from flask_socketio import SocketIO, emit, join_room, leave_room
from app.models.message import Message
from app import db

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connected', {'message': 'Connected to server'})

@socketio.on('join_chat')
def handle_join(data):
    user_id = data.get('user_id')
    join_room('chat_room')
    emit('user_joined', {'user_id': user_id}, room='chat_room')

@socketio.on('send_message')
def handle_message(data):
    message = Message(
        message=data['message'],
        user_id=data['user_id']
    )
    db.session.add(message)
    db.session.commit()
    
    emit('new_message', {
        'id': message.id,
        'message': message.message,
        'user_id': message.user_id,
        'timestamp': message.timestamp.isoformat()
    }, room='chat_room')

@socketio.on('typing')
def handle_typing(data):
    emit('user_typing', data, room='chat_room', include_self=False)
```

**Modifier:** `backend/run.py`
```python
from app.sockets import socketio

app = create_app()
socketio.init_app(app)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```

**Frontend:** `frontend/src/services/socket.js`
```javascript
import io from 'socket.io-client';

const SOCKET_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class SocketService {
  constructor() {
    this.socket = null;
  }

  connect() {
    this.socket = io(SOCKET_URL);
    
    this.socket.on('connect', () => {
      console.log('✅ Connected to WebSocket');
    });
    
    return this.socket;
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
    }
  }

  onNewMessage(callback) {
    this.socket.on('new_message', callback);
  }

  sendMessage(message, userId) {
    this.socket.emit('send_message', { message, user_id: userId });
  }

  joinChat(userId) {
    this.socket.emit('join_chat', { user_id: userId });
  }

  onTyping(callback) {
    this.socket.on('user_typing', callback);
  }

  emitTyping(userId) {
    this.socket.emit('typing', { user_id: userId });
  }
}

export default new SocketService();
```

**Installation:**
```bash
# Backend
pip install flask-socketio python-socketio eventlet

# Frontend
npm install socket.io-client
```

---

### ❌ TÂCHE 7: Notifications Push

**Status:** ❌ Non implémenté

#### Solution avec Web Push API

**Backend:** `backend/app/services/notification.py`
```python
from pywebpush import webpush, WebPushException
import json

class NotificationService:
    def __init__(self):
        self.VAPID_PRIVATE_KEY = os.getenv('VAPID_PRIVATE_KEY')
        self.VAPID_PUBLIC_KEY = os.getenv('VAPID_PUBLIC_KEY')
        self.VAPID_CLAIMS = {
            "sub": "mailto:admin@plateformexp.com"
        }
    
    def send_notification(self, subscription, title, body):
        try:
            webpush(
                subscription_info=subscription,
                data=json.dumps({
                    "title": title,
                    "body": body,
                    "icon": "/logo192.png"
                }),
                vapid_private_key=self.VAPID_PRIVATE_KEY,
                vapid_claims=self.VAPID_CLAIMS
            )
            return True
        except WebPushException as e:
            print(f"Error sending notification: {e}")
            return False
    
    def notify_badge_earned(self, user, badge):
        self.send_notification(
            user.push_subscription,
            "🎖️ Nouveau Badge!",
            f"Vous avez gagné le badge: {badge.nom}"
        )
```

**Frontend:** `frontend/src/services/notifications.js`
```javascript
const PUBLIC_VAPID_KEY = process.env.REACT_APP_VAPID_PUBLIC_KEY;

export const requestNotificationPermission = async () => {
  if (!('Notification' in window)) {
    console.log('Notifications not supported');
    return false;
  }

  const permission = await Notification.requestPermission();
  
  if (permission === 'granted') {
    const registration = await navigator.serviceWorker.ready;
    const subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(PUBLIC_VAPID_KEY)
    });
    
    // Send subscription to backend
    await api.post('/users/push-subscription', subscription);
    return true;
  }
  
  return false;
};

function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\\-/g, '+')
    .replace(/_/g, '/');
  
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}
```

**Installation:**
```bash
pip install pywebpush
npm install web-push
```

---

### ⚠️ TÂCHE 8: Édition du Profil

**Status:** ⚠️ Partiellement implémenté

#### Solution Complète

**Backend:** `backend/app/routes/users.py`
```python
@users_bp.route('/profile', methods=['PUT'])
@jwt_required_custom()
def update_profile(current_user):
    data = request.get_json()
    
    # Update fields
    if 'nom' in data:
        current_user.nom = data['nom']
    if 'promotion' in data:
        current_user.promotion = data['promotion']
    if 'bio' in data:
        current_user.bio = data['bio']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': current_user.to_dict()
    }), 200

@users_bp.route('/change-password', methods=['POST'])
@jwt_required_custom()
def change_password(current_user):
    data = request.get_json()
    
    # Verify old password
    if not bcrypt.check_password_hash(current_user.password, data['old_password']):
        return jsonify({'error': 'Invalid old password'}), 401
    
    # Update password
    hashed_password = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')
    current_user.password = hashed_password
    
    db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'}), 200
```

**Frontend:** `frontend/src/components/Profile.jsx`
```javascript
const [editMode, setEditMode] = useState(false);
const [formData, setFormData] = useState({
  nom: user.nom,
  promotion: user.promotion,
  bio: user.bio
});

const handleSave = async () => {
  try {
    const response = await usersAPI.updateProfile(formData);
    setUser(response.data.user);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    setEditMode(false);
    alert('Profile updated!');
  } catch (error) {
    alert('Error updating profile');
  }
};

return (
  <Box>
    {editMode ? (
      <Box component="form">
        <TextField
          label="Nom"
          value={formData.nom}
          onChange={(e) => setFormData({...formData, nom: e.target.value})}
          fullWidth
          margin="normal"
        />
        <TextField
          label="Promotion"
          value={formData.promotion}
          onChange={(e) => setFormData({...formData, promotion: e.target.value})}
          fullWidth
          margin="normal"
        />
        <TextField
          label="Bio"
          value={formData.bio}
          onChange={(e) => setFormData({...formData, bio: e.target.value})}
          fullWidth
          multiline
          rows={4}
          margin="normal"
        />
        <Button onClick={handleSave} variant="contained">Save</Button>
        <Button onClick={() => setEditMode(false)}>Cancel</Button>
      </Box>
    ) : (
      <Box>
        <Typography>{user.nom}</Typography>
        <Typography>{user.promotion}</Typography>
        <Typography>{user.bio}</Typography>
        <Button onClick={() => setEditMode(true)} startIcon={<EditIcon />}>
          Edit Profile
        </Button>
      </Box>
    )}
  </Box>
);
```

---

## 📊 RÉSUMÉ DES IMPLÉMENTATIONS

| Tâche | Status | Fichiers | Commandes |
|-------|--------|----------|-----------|
| 1. API Backend | ✅ | backend/run.py, app/__init__.py | `python run.py` |
| 2. Interface Web | ✅ | frontend/src/App.js | `npm start` |
| 3. Auth JWT | ✅ | backend/app/routes/auth.py | Auto avec backend |
| 4. Migration JSON | ⚠️ | backend/migrate_json_to_db.py | `python migrate_json_to_db.py` |
| 5. Déploiement | ⚠️ | Procfile, vercel.json | `git push heroku main` |
| 6. WebSockets | ⚠️ | app/sockets/__init__.py | `pip install flask-socketio` |
| 7. Notifications | ❌ | app/services/notification.py | `pip install pywebpush` |
| 8. Édition Profil | ⚠️ | components/Profile.jsx | Intégré |

---

**Dernière mise à jour:** 2025-10-30  
**Documentation maintenue par:** Plateforme XP Team
