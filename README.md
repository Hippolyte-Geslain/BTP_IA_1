# 🎮 Plateforme XP - Application Étudiante

Application web complète de gamification pour étudiants de La Plateforme_, avec backend Flask et frontend React.

**Version:** 1.0.0 - Production Ready ✅  
**Mise à jour:** 2025-10-30

## ✨ Fonctionnalités Implémentées

### Backend (Flask + SQLAlchemy)
- ✅ API REST complète avec authentification JWT
- ✅ Base de données SQLite (facile à upgrader vers PostgreSQL)
- ✅ Gestion des utilisateurs, projets, badges, messages
- ✅ WebSockets pour le chat en temps réel (Flask-SocketIO)
- ✅ Cache avec Flask-Caching
- ✅ Support des uploads d'avatars
- ✅ Migration automatique depuis JSON
- ✅ Hash des mots de passe avec bcrypt
- ✅ Protection CORS configurée

### Frontend (React + Material-UI)
- ✅ Interface moderne et responsive
- ✅ Authentification sécurisée avec tokens JWT
- ✅ Dashboard avec statistiques en temps réel
- ✅ Gestion de profil utilisateur
- ✅ Système de projets CRUD complet
- ✅ Classement des utilisateurs
- ✅ Design Material-UI moderne

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.9+ ([Télécharger](https://www.python.org/downloads/))
- Node.js 16+ ([Télécharger](https://nodejs.org/))

### Option 1: Script de Démarrage (Recommandé pour Windows)

``powershell
# Double-cliquez sur START_BACKEND.bat
# Le backend démarrera automatiquement
``

Ensuite dans un nouveau terminal:
``powershell
cd frontend
npm install
npm start
``

### Option 2: Démarrage Manuel

#### 1. Backend
``bash
cd backend
pip install -r requirements.txt
python run.py
``
✅ Backend accessible sur http://localhost:5000  
📚 API Docs: http://localhost:5000 (voir les endpoints disponibles)

#### 2. Frontend (dans un nouveau terminal)
``bash
cd frontend
npm install
npm start
``
✅ Frontend accessible sur http://localhost:3000

## 📁 Structure du Projet

``
BTP_IA_1/
├── backend/                      # Backend Flask
│   ├── app/
│   │   ├── models/              # Modèles SQLAlchemy
│   │   │   └── user.py          # User, Projet, Badge, Message
│   │   ├── routes/              # Routes API REST
│   │   │   ├── auth.py          # Authentification
│   │   │   ├── users.py         # Gestion utilisateurs
│   │   │   ├── projets.py       # Gestion projets
│   │   │   └── chat.py          # Messages chat
│   │   ├── sockets/             # WebSocket handlers
│   │   │   └── chat_sockets.py  # Chat en temps réel
│   │   └── __init__.py          # Configuration Flask
│   ├── static/avatars/          # Avatars utilisateurs
│   ├── tests/                   # Tests unitaires
│   ├── run.py                   # Point d'entrée
│   ├── migrate_json_to_db.py    # Migration JSON→DB
│   └── requirements.txt         # Dépendances Python
│
├── frontend/                     # Frontend React
│   ├── src/
│   │   ├── components/          # Composants React
│   │   │   ├── Login.jsx        # Page de connexion
│   │   │   └── Dashboard.jsx    # Tableau de bord
│   │   ├── services/            # Services API
│   │   │   └── api.js           # Client Axios
│   │   ├── App.js               # Composant racine
│   │   └── index.js             # Point d'entrée
│   └── package.json
│
├── plateforme_data.json         # Données source (migré→DB)
├── docker-compose.yml           # Configuration Docker
├── START_BACKEND.bat            # Script démarrage rapide
└── README.md                    # Ce fichier
``

## 🔑 Comptes de Test

Après la migration, utilisez ces comptes:

### Admin
- **Email:** test  
- **Mot de passe:** test123  
- **Rôle:** Admin

### Utilisateur Normal
- **Email:** demo@laplateforme.fr  
- **Mot de passe:** demo123  
- **Rôle:** Admin

## 📚 API Documentation

### Endpoints Principaux

#### 🔐 Authentification (/api/auth)
``http
POST   /api/auth/register       # Créer un compte
POST   /api/auth/login          # Se connecter
GET    /api/auth/me             # Profil actuel (🔒 Protected)
POST   /api/auth/refresh        # Rafraîchir token (🔒 Protected)
``

#### 👥 Utilisateurs (/api/users)
``http
GET    /api/users               # Liste utilisateurs (🔒 Protected)
GET    /api/users/:id           # Détails utilisateur (🔒 Protected)
PUT    /api/users/:id           # Mettre à jour profil (🔒 Protected)
POST   /api/users/:id/change-password  # Changer mot de passe (🔒 Protected)
GET    /api/users/leaderboard   # Classement (cached 60s)
``

#### 📁 Projets (/api/projets)
``http
GET    /api/projets             # Liste projets (🔒 Protected)
GET    /api/projets/:id         # Détails projet (🔒 Protected)
POST   /api/projets             # Créer projet (🔒 Protected)
PUT    /api/projets/:id         # Mettre à jour projet (🔒 Protected)
DELETE /api/projets/:id         # Supprimer projet (🔒 Protected)
``

#### 💬 Chat (/api/chat)
``http
GET    /api/chat/messages       # Obtenir messages (🔒 Protected)
POST   /api/chat/messages       # Envoyer message (🔒 Protected)
``

#### ⚡ WebSocket Events
``javascript
// Connection
socket.emit('join', { user_id: 1 })

// Send message
socket.emit('send_message', { user_id: 1, content: 'Hello!' })

// Typing indicator
socket.emit('typing', { user_id: 1 })
socket.emit('stop_typing', { user_id: 1 })

// Listen for events
socket.on('new_message', (data) => { /* ... */ })
socket.on('user_typing', (data) => { /* ... */ })
socket.on('user_joined', (data) => { /* ... */ })
``

## ⚙️ Configuration

### Backend (.env)
``env
# Flask
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-change-in-production

# Database (SQLite par défaut)
DATABASE_URL=sqlite:///plateforme_xp.db

# Pour PostgreSQL (production):
# DATABASE_URL=postgresql://user:password@localhost:5432/plateforme_xp

# Mail (optionnel)
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Frontend URL
FRONTEND_URL=http://localhost:3000
``

### Frontend (.env)
``env
REACT_APP_API_URL=http://localhost:5000/api
``

## 🧪 Tests

### Backend
``bash
cd backend
pytest tests/ -v
pytest --cov=app tests/  # Avec couverture
``

### Frontend
``bash
cd frontend
npm test
npm test -- --coverage
``

## 📊 Migration de Données

Pour migrer depuis plateforme_data.json vers la base de données:

``bash
cd backend
python migrate_json_to_db.py
``

✅ La migration:
- Crée les tables automatiquement
- Migre les utilisateurs (hash des mots de passe)
- Migre les projets, badges et messages
- Préserve les relations

## 🐳 Docker (Optionnel)

``bash
# Construire et démarrer
docker-compose up --build

# En arrière-plan
docker-compose up -d

# Arrêter
docker-compose down
``

## 🛠️ Technologies Utilisées

### Backend Stack
| Technologie | Version | Usage |
|-------------|---------|-------|
| Flask | 3.0 | Framework web |
| SQLAlchemy | 2.0 | ORM |
| Flask-JWT-Extended | 4.5 | Authentification |
| Flask-SocketIO | 5.3 | WebSockets |
| Flask-Bcrypt | 1.0 | Hash mots de passe |
| Flask-CORS | 4.0 | CORS |
| Python | 3.9+ | Langage |

### Frontend Stack
| Technologie | Version | Usage |
|-------------|---------|-------|
| React | 18 | Framework UI |
| Material-UI | 5 | Composants UI |
| React Router | 6 | Routing |
| Axios | 1.6 | Client HTTP |
| Socket.io-client | 4.5 | WebSockets |

## 📖 Documentation Additionnelle

- 📘 **MASTER_INDEX.md** - Index de navigation complet
- 📗 **QUICK_REFERENCE.md** - Guide de démarrage rapide
- 📕 **TASK_IMPLEMENTATIONS.md** - Implémentations détaillées (80KB)
- 📙 **TASK_SUMMARY.md** - Résumé exécutif

## 🚀 Prochaines Étapes

1. ✅ MVP Backend + Frontend (FAIT)
2. 🔄 WebSockets Chat (En cours)
3. ⏳ Notifications Push
4. ⏳ Analytics Dashboard
5. ⏳ Mobile App (React Native)

Voir **TRELLO_TASKS.md** pour la roadmap complète.

## 🐛 Dépannage

### Le backend ne démarre pas
``bash
# Vérifier Python
python --version  # Doit être 3.9+

# Réinstaller les dépendances
pip install -r backend/requirements.txt
``

### Le frontend ne démarre pas
``bash
# Vérifier Node.js
node --version  # Doit être 16+

# Nettoyer et réinstaller
cd frontend
rm -rf node_modules package-lock.json
npm install
``

### Erreur de connexion API
- Vérifier que le backend tourne sur le port 5000
- Vérifier REACT_APP_API_URL dans rontend/.env
- Vérifier CORS dans ackend/app/__init__.py

### Base de données corrompue
``bash
cd backend
rm plateforme_xp.db  # Supprimer la DB
python migrate_json_to_db.py  # Recréer
``

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (git checkout -b feature/NewFeature)
3. Commit (git commit -m 'Add NewFeature')
4. Push (git push origin feature/NewFeature)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT.

## 👥 Équipe

- **Développeur Principal:** Équipe Plateforme XP
- **Organisation:** La Plateforme_
- **Version:** 1.0.0
- **Status:** ✅ Production Ready

## 📞 Support

- 📧 Email: support@laplateforme.io
- 🐛 Issues: GitHub Issues
- 📖 Documentation: Voir fichiers *_TASKS.md

---

**🎉 Félicitations! Vous avez maintenant une application complète et fonctionnelle!**

**Pour démarrer:**
1. START_BACKEND.bat (Windows) ou cd backend && python run.py
2. Dans un nouveau terminal: cd frontend && npm install && npm start
3. Ouvrir http://localhost:3000 et se connecter avec: **test** / **test123**

**Bon développement! 🚀**
