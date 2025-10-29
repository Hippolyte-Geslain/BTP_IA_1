# 🎮 Plateforme XP - Application Étudiante Gamifiée

**Application Desktop 100% Fonctionnelle + Guide d'Évolution Complet**

> Prototype complet pour les étudiants de La Plateforme_ combinant apprentissage, entraide et progression gamifiée.

## 📊 STATUS ACTUEL

**Version Desktop:** ✅ 100% Fonctionnel  
**Version Web:** ❌ À développer (voir `EVOLUTIONS_REQUISES.md`)  
**Version Mobile:** ❌ À développer (voir `EVOLUTIONS_REQUISES.md`)

## 📋 Description

**Plateforme XP** est une application gamifiée qui transforme l'expérience étudiante en un jeu vidéo RPG. Les étudiants gagnent de l'XP en réalisant des projets, en aidant leurs pairs, et progressent à travers différents niveaux avec un système de badges et de récompenses.

## ✨ Fonctionnalités Implémentées (Prototype)

### 🎯 Système de Progression
- ✅ **Profil utilisateur** avec XP et niveaux
- ✅ **Système de niveaux** calculé dynamiquement (formule RPG)
- ✅ **Barre de progression** visuelle vers le prochain niveau
- ✅ **Badges débloquables** (Premier Projet, Mentor, etc.)

### 📚 Gestion de Projets
- ✅ Liste de projets avec difficulté (Easy/Medium/Hard)
- ✅ Récompenses XP variables selon la difficulté
- ✅ Suivi des projets complétés
- ✅ Attribution automatique d'XP

### 🤝 Système d'Entraide
- ✅ Gain d'XP en aidant d'autres étudiants
- ✅ Badge "Mentor" pour encourager l'entraide
- ✅ Valorisation de la collaboration

### 💬 Chat Anonyme
- ✅ Messages anonymes pour poser des questions librement
- ✅ Horodatage des messages
- ✅ Système de réponses

### 🏆 Classement
- ✅ Leaderboard des étudiants par XP
- ✅ Médailles pour le top 3
- ✅ Motivation compétitive saine

### 📅 Événements
- ✅ Liste d'événements (BDE, Workshops, Tournois)
- ✅ Système de participation
- ✅ Dates et types d'événements

### 📱 Badge Numérique
- ✅ Génération de QR Code pour accès à l'école
- ✅ Données encodées (ID, nom, niveau, validité)
- ✅ Export en image PNG

### 💾 Persistance
- ✅ Sauvegarde JSON des données
- ✅ Chargement automatique au démarrage
- ✅ Données préservées entre sessions

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le dépôt**
```bash
git clone <url_du_repo>
cd BTP_IA_1
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Lancer l'application**
```bash
python test.py
```

## 📦 Dépendances

- `qrcode` : Génération de QR Codes pour les badges
- `Pillow` : Manipulation d'images pour les QR Codes

## 🎮 Utilisation

### Première utilisation

1. **Créer un compte** (Option 1)
   - Entrez votre nom et email
   - Un ID utilisateur vous sera attribué

2. **Se connecter** (Option 2)
   - Utilisez votre ID utilisateur

3. **Explorer les fonctionnalités**
   - Consultez votre profil
   - Regardez les projets disponibles
   - Complétez des projets pour gagner de l'XP
   - Aidez d'autres étudiants
   - Participez au chat anonyme

### Exemples d'utilisation

```
Menu Principal > 1 (Créer un compte)
Nom: Noah
Email: noah@laplateforme.io
✅ Utilisateur Noah créé avec succès !

Menu Principal > 2 (Se connecter)
ID utilisateur: 1
👋 Bienvenue Noah !

Menu Principal > 5 (Compléter un projet)
ID du projet: 1
✨ +50 XP (Projet: Site Web Portfolio)
🏆 Badge débloqué: Premier Projet !
```

## 📊 Architecture du Code

```
test.py
├── Modèles de Données
│   ├── User (utilisateurs)
│   ├── Project (projets)
│   ├── ChatMessage (messages)
│   └── Event (événements)
│
├── Système de Gestion
│   └── PlateformeXP (logique métier)
│       ├── Gestion utilisateurs
│       ├── Gestion projets
│       ├── Système XP/Niveaux
│       ├── Chat anonyme
│       ├── Événements
│       ├── Classement
│       └── Persistance données
│
└── Interface CLI
    ├── Banner
    └── Menu interactif
```

## 🎯 Fonctionnalités à Développer (Roadmap)

### Phase 2 - Interface Graphique
- [ ] Interface web avec Flask/Django
- [ ] Dashboard étudiant personnalisé
- [ ] Visualisations de progression

### Phase 3 - Fonctionnalités Avancées
- [ ] **Tutorat** : Réservation de sessions
- [ ] **Carte des bons plans** : Géolocalisation
- [ ] **Tournois** : Création et gestion
- [ ] **Coach carrière** : Conseils IA
- [ ] **Compagnon de compétences** : Analyse CV
- [ ] **Partage de ressources** : Bibliothèque collaborative

### Phase 4 - Mobile & Cloud
- [ ] Application mobile (React Native)
- [ ] Synchronisation cloud
- [ ] Notifications push
- [ ] Authentification OAuth

### Phase 5 - Social & Gamification+
- [ ] Système d'amis
- [ ] Guildes/Équipes
- [ ] Achievements complexes
- [ ] Skins/Avatars personnalisables

## ⚠️ LIMITATIONS ACTUELLES (Important!)

### ❌ Version Desktop Uniquement
- Pas d'accès web/URL
- Application locale sur un seul ordinateur
- Pas d'accès distant

### ❌ Pas de Vraie Base de Données
- Données stockées en JSON (risque de perte)
- Pas de scalabilité
- Limite quelques utilisateurs locaux

### ❌ Pas de Sécurité d'Authentification
- Pas de mot de passe hashé
- Pas de JWT/OAuth2
- Pas de chiffrement

### ❌ Pas de Real-Time
- Pas de WebSockets
- Pas de notifications push
- Chat pas synchronisé entre clients

### ❌ Pas de Mobile
- Interface Desktop seulement
- Pas de version React Native

---

## 📈 POUR PASSER EN PRODUCTION

### Vous avez besoin de:
1. **Backend Web:** Flask + PostgreSQL + JWT
2. **Frontend Web:** React + TypeScript + Tailwind
3. **Mobile:** React Native (optionnel)
4. **DevOps:** Docker + GitHub Actions + Heroku/AWS
5. **Real-Time:** WebSockets (Socket.io)

**→ Voir le fichier `EVOLUTIONS_REQUISES.md` pour le guide complet!**

---

## 🏗️ Structure de Données

### Utilisateur
```json
{
  "user_id": 1,
  "name": "Noah",
  "email": "noah@laplateforme.io",
  "xp": 180,
  "level": 2,
  "badges": ["🏆 Premier Projet", "🎓 Mentor"],
  "projects_completed": [1, 2]
}
```

### Projet
```json
{
  "project_id": 1,
  "title": "Site Web Portfolio",
  "difficulty": "Easy",
  "xp_reward": 50,
  "skills": ["HTML", "CSS", "JavaScript"]
}
```

## 🔐 Sécurité

- Les mots de passe ne sont pas implémentés dans ce prototype
- Les messages anonymes sont vraiment anonymes
- Les données sont stockées localement en JSON

## 🤝 Contribution

Ce projet est un prototype pédagogique pour La Plateforme_. Les contributions sont bienvenues !

### Comment contribuer ?
1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Projet éducatif - La Plateforme_ © 2024

## 👨‍💻 Auteur

**Noah** - Étudiant B2 à La Plateforme_

## 🙏 Remerciements

- La Plateforme_ pour l'inspiration
- La communauté étudiante
- Les formateurs et mentors

---

**🎮 Transformez votre apprentissage en aventure !**