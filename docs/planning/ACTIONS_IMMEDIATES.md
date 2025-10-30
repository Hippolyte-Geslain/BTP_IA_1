# 🎬 ACTIONS IMMÉDIATES À FAIRE

## 📅 Cette Semaine

### ✅ Jour 1: Lire la Documentation
- [ ] Lire `EVOLUTIONS_REQUISES.md` complètement
- [ ] Lire `ROADMAP_RAPIDE.md` 
- [ ] Identifier les technologies à apprendre
- **Temps: 2 heures**

### ✅ Jour 2-3: Environnement Local
```bash
# Backend
mkdir backend && cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install flask sqlalchemy psycopg2-binary flask-jwt-extended flask-cors

# Frontend
cd ..
npx create-react-app frontend
cd frontend
npm install axios react-router-dom
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Database
# Télécharger PostgreSQL: https://www.postgresql.org/download/
# Créer base "plateforme_xp"
```

**Temps: 1-2 heures (téléchargements + installation)**

### ✅ Jour 4-5: First API Endpoint

**backend/app.py:**
```python
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "API works! 🎉"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

```bash
cd backend
python app.py
# Visite: http://localhost:5000/api/test
```

**Temps: 1 heure**

### ✅ Jour 6-7: First React Component

**frontend/src/App.jsx:**
```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [message, setMessage] = useState('Chargement...');

  useEffect(() => {
    axios.get('http://localhost:5000/api/test')
      .then(res => setMessage(res.data.message))
      .catch(err => setMessage('Erreur: ' + err.message));
  }, []);

  return (
    <div className="App">
      <h1>🎮 Plateforme XP</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;
```

```bash
cd frontend
npm start
# Visite: http://localhost:3000
```

**Temps: 1 heure**

**✅ Si tout marche: Backend parle à Frontend! 🎉**

---

## 📊 Semaine 2: Models & Authentification

### ✅ Jour 8-9: Setup PostgreSQL

**backend/config.py:**
```python
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/plateforme_xp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-secret-change-this')
```

**backend/models.py:**
```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    promo = db.Column(db.String(10), default='B2')
    xp = db.Column(db.Integer, default=0)
    niveau = db.Column(db.Integer, default=1)
    badges = db.Column(db.JSON, default=[])
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'email': self.email,
            'promo': self.promo,
            'xp': self.xp,
            'niveau': self.niveau,
            'badges': self.badges
        }
```

**backend/app.py (mise à jour):**
```python
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Temps: 2 heures**

### ✅ Jour 10-11: Routes d'Authentification

**backend/routes/auth.py:**
```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email exists"}), 400
    
    user = User(
        nom=data['nom'],
        email=data['email'],
        promo=data.get('promo', 'B2')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        "message": "Account created!",
        "user": user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    token = create_access_token(identity=user.id)
    
    return jsonify({
        "access_token": token,
        "user": user.to_dict()
    }), 200
```

**backend/app.py (enregistrer blueprint):**
```python
from routes.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/api/auth')
```

**Temps: 2 heures**

### ✅ Jour 12: Tester l'Auth avec Postman

```
1. Télécharger Postman: https://www.postman.com/downloads/
2. POST http://localhost:5000/api/auth/register
   {
     "nom": "Test User",
     "email": "test@example.com",
     "password": "password123",
     "promo": "B2"
   }
3. POST http://localhost:5000/api/auth/login
   {
     "email": "test@example.com",
     "password": "password123"
   }
   → Copier le token JWT retourné
```

**Temps: 1 heure**

---

## 🎨 Semaine 3: Frontend React

### ✅ Jour 15-16: Composant Login

**frontend/src/components/Login.jsx:**
```jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/Login.css';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(
                'http://localhost:5000/api/auth/login',
                { email, password }
            );
            
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('user', JSON.stringify(response.data.user));
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.error || 'Connection error');
        }
    };

    return (
        <div className="login-container">
            <h1>🎮 Plateforme XP</h1>
            <form onSubmit={handleLogin}>
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                {error && <p className="error">{error}</p>}
                <button type="submit">Login</button>
            </form>
        </div>
    );
}
```

**frontend/src/styles/Login.css:**
```css
.login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-container h1 {
    color: white;
    font-size: 3rem;
    margin-bottom: 2rem;
}

.login-container form {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    width: 100%;
    max-width: 400px;
}

.login-container input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
}

.login-container button {
    width: 100%;
    padding: 12px;
    margin-top: 20px;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 1rem;
    cursor: pointer;
}

.login-container button:hover {
    background: #764ba2;
}

.error {
    color: red;
    margin: 10px 0;
}
```

**Temps: 2 heures**

### ✅ Jour 17-18: Routing & Dashboard

**frontend/src/App.jsx:**
```jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import './App.css';

function PrivateRoute({ children }) {
    const token = localStorage.getItem('access_token');
    return token ? children : <Navigate to="/login" />;
}

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route 
                    path="/dashboard" 
                    element={
                        <PrivateRoute>
                            <Dashboard />
                        </PrivateRoute>
                    } 
                />
                <Route path="/" element={<Navigate to="/dashboard" />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
```

**frontend/src/components/Dashboard.jsx:**
```jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Dashboard() {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const userData = localStorage.getItem('user');
        if (userData) {
            setUser(JSON.parse(userData));
        }
    }, []);

    const logout = () => {
        localStorage.clear();
        window.location.href = '/login';
    };

    return (
        <div className="dashboard">
            <h1>Welcome, {user?.nom}! 🎮</h1>
            <p>XP: {user?.xp} | Level: {user?.niveau}</p>
            <button onClick={logout}>Logout</button>
        </div>
    );
}
```

**Temps: 2 heures**

---

## ✅ Checkpoint: Fin Semaine 3

**À ce stade, vous devez avoir:**
- [ ] API Flask complète avec Auth
- [ ] PostgreSQL configuré
- [ ] Frontend React avec Login
- [ ] Private routes fonctionnelles
- [ ] Token JWT en localStorage

**Test final:**
1. Backend: `python app.py` (port 5000)
2. Frontend: `npm start` (port 3000)
3. Aller sur http://localhost:3000/login
4. Créer un compte
5. Se connecter
6. Voir le dashboard

**Si ça marche: Vous êtes à 30% du chemin!** 🎉

---

## 📝 Prochaines Étapes (Semaine 4+)

### Semaine 4: Plus de Routes API
- [ ] GET /api/users/profile
- [ ] GET /api/projets
- [ ] POST /api/projets/{id}/completer
- [ ] GET /api/chat/messages
- [ ] POST /api/chat/messages

### Semaine 5: Plus de Composants React
- [ ] Projects page
- [ ] Chat page
- [ ] Leaderboard page
- [ ] Profile page
- [ ] Navigation menu

### Semaine 6: Styling Complet
- [ ] Tailwind CSS partout
- [ ] Animations
- [ ] Responsive design
- [ ] Dark mode

### Semaine 7: Déploiement
- [ ] Docker setup
- [ ] Heroku deployment
- [ ] Tests en production

---

## 🆘 Si Vous Êtes Bloqué

### Erreur CORS
```python
# backend/app.py
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
```

### Erreur Database Connection
```bash
# Vérifier PostgreSQL tourne
sudo service postgresql start  # Linux/Mac
# Windows: PostgreSQL service
```

### Token Non Reconnu
```python
# Vérifier JWT_SECRET_KEY est la même partout
# Mettre à jour le token dans localStorage
```

### "Module not found"
```bash
pip install -r requirements.txt    # Backend
npm install                         # Frontend
```

---

## 📞 Ressources d'Aide

- Flask docs: https://flask.palletsprojects.com/
- React docs: https://react.dev/
- PostgreSQL docs: https://www.postgresql.org/docs/
- Stack Overflow: https://stackoverflow.com/questions/tagged/flask+react
- Discord La Plateforme_: [Lien]

---

**🎯 Vous êtes prêt? Commencez aujourd'hui! 🚀**

**Revenir dans une semaine pour montrer vos résultats!**
