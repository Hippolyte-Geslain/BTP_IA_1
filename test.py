#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plateforme XP - Application Étudiante Gamifiée
Prototype pour La Plateforme_
"""

import json
import os
import qrcode
from datetime import datetime
from typing import List, Dict, Optional
import random


# ==================== MODÈLES DE DONNÉES ====================

class User:
    """Modèle représentant un étudiant"""
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.xp = 0
        self.level = 1
        self.badges = []
        self.projects_completed = []
        
    def add_xp(self, amount: int, reason: str = ""):
        """Ajoute de l'XP et met à jour le niveau"""
        self.xp += amount
        old_level = self.level
        self.level = self.calculate_level()
        
        if self.level > old_level:
            print(f"🎉 {self.name} a atteint le niveau {self.level} !")
        
        print(f"✨ +{amount} XP {'(' + reason + ')' if reason else ''}")
        
    def calculate_level(self) -> int:
        """Calcule le niveau basé sur l'XP (système RPG)"""
        return int((self.xp / 100) ** 0.5) + 1
    
    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'xp': self.xp,
            'level': self.level,
            'badges': self.badges,
            'projects_completed': self.projects_completed
        }


class Project:
    """Modèle représentant un projet"""
    def __init__(self, project_id: int, title: str, difficulty: str, xp_reward: int):
        self.project_id = project_id
        self.title = title
        self.difficulty = difficulty  # Easy, Medium, Hard
        self.xp_reward = xp_reward
        self.skills = []
        
    def to_dict(self) -> dict:
        return {
            'project_id': self.project_id,
            'title': self.title,
            'difficulty': self.difficulty,
            'xp_reward': self.xp_reward,
            'skills': self.skills
        }


class ChatMessage:
    """Modèle pour les messages du chat anonyme"""
    def __init__(self, message_id: int, content: str, author_id: Optional[int] = None):
        self.message_id = message_id
        self.content = content
        self.author_id = author_id  # None si anonyme
        self.timestamp = datetime.now()
        self.replies = []
        self.is_anonymous = author_id is None
        
    def to_dict(self) -> dict:
        return {
            'message_id': self.message_id,
            'content': self.content,
            'author_id': "Anonyme" if self.is_anonymous else self.author_id,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'replies': len(self.replies)
        }


class Event:
    """Modèle pour les événements (BDE, école, tournois)"""
    def __init__(self, event_id: int, title: str, event_type: str, date: str):
        self.event_id = event_id
        self.title = title
        self.event_type = event_type  # BDE, Workshop, Tournament
        self.date = date
        self.participants = []
        
    def to_dict(self) -> dict:
        return {
            'event_id': self.event_id,
            'title': self.title,
            'type': self.event_type,
            'date': self.date,
            'participants': len(self.participants)
        }


# ==================== SYSTÈME DE GESTION ====================

class PlateformeXP:
    """Classe principale gérant l'application"""
    
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.projects: Dict[int, Project] = {}
        self.chat_messages: List[ChatMessage] = []
        self.events: List[Event] = []
        self.current_user: Optional[User] = None
        self.data_file = "plateforme_data.json"
        
        self.load_data()
        self._initialize_demo_data()
        
    def _initialize_demo_data(self):
        """Initialise des données de démonstration"""
        if not self.projects:
            # Créer quelques projets d'exemple
            projects_data = [
                (1, "Site Web Portfolio", "Easy", 50),
                (2, "API REST avec Flask", "Medium", 100),
                (3, "Application Mobile React Native", "Hard", 200),
                (4, "Machine Learning - Prédiction", "Hard", 250),
                (5, "Bot Discord avec Python", "Medium", 120)
            ]
            
            for pid, title, diff, xp in projects_data:
                self.projects[pid] = Project(pid, title, diff, xp)
        
        if not self.events:
            # Créer quelques événements
            self.events.append(Event(1, "Soirée Gaming BDE", "BDE", "2024-11-15"))
            self.events.append(Event(2, "Workshop IA & Machine Learning", "Workshop", "2024-11-20"))
            self.events.append(Event(3, "Hackathon 48h", "Tournament", "2024-12-01"))
    
    def register_user(self, name: str, email: str) -> User:
        """Inscrit un nouvel utilisateur"""
        user_id = len(self.users) + 1
        user = User(user_id, name, email)
        self.users[user_id] = user
        print(f"✅ Utilisateur {name} créé avec succès !")
        return user
    
    def login(self, user_id: int) -> bool:
        """Connecte un utilisateur"""
        if user_id in self.users:
            self.current_user = self.users[user_id]
            print(f"👋 Bienvenue {self.current_user.name} !")
            return True
        print("❌ Utilisateur introuvable")
        return False
    
    def complete_project(self, project_id: int):
        """Marque un projet comme complété et attribue l'XP"""
        if not self.current_user:
            print("❌ Vous devez être connecté")
            return
            
        if project_id not in self.projects:
            print("❌ Projet introuvable")
            return
            
        project = self.projects[project_id]
        
        if project_id in self.current_user.projects_completed:
            print("⚠️ Projet déjà complété")
            return
        
        self.current_user.projects_completed.append(project_id)
        self.current_user.add_xp(project.xp_reward, f"Projet: {project.title}")
        
        # Badge pour premier projet
        if len(self.current_user.projects_completed) == 1:
            self.current_user.badges.append("🏆 Premier Projet")
            print("🏆 Badge débloqué: Premier Projet !")
    
    def help_student(self, helped_user_id: int):
        """Système d'entraide - donner de l'aide à un étudiant"""
        if not self.current_user:
            print("❌ Vous devez être connecté")
            return
        
        self.current_user.add_xp(30, "Aide apportée à un étudiant")
        
        # Badge mentor
        if "🎓 Mentor" not in self.current_user.badges:
            self.current_user.badges.append("🎓 Mentor")
            print("🎓 Badge débloqué: Mentor !")
    
    def post_anonymous_message(self, content: str):
        """Poste un message anonyme sur le chat"""
        msg_id = len(self.chat_messages) + 1
        message = ChatMessage(msg_id, content)
        self.chat_messages.append(message)
        print("💬 Message anonyme posté avec succès")
    
    def view_chat(self, limit: int = 10):
        """Affiche les derniers messages du chat"""
        print("\n" + "="*50)
        print("💬 CHAT ANONYME D'ENTRAIDE")
        print("="*50)
        
        for msg in self.chat_messages[-limit:]:
            print(f"\n[{msg.timestamp.strftime('%H:%M')}] {'👤 Anonyme' if msg.is_anonymous else f'User #{msg.author_id}'}")
            print(f"  {msg.content}")
            print(f"  💬 {len(msg.replies)} réponse(s)")
    
    def generate_qr_badge(self):
        """Génère un badge QR Code pour l'accès à l'école"""
        if not self.current_user:
            print("❌ Vous devez être connecté")
            return
        
        # Données du badge
        badge_data = {
            'user_id': self.current_user.user_id,
            'name': self.current_user.name,
            'level': self.current_user.level,
            'valid_until': '2025-12-31'
        }
        
        # Générer QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(json.dumps(badge_data))
        qr.make(fit=True)
        
        filename = f"badge_{self.current_user.user_id}.png"
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        
        print(f"✅ Badge QR Code généré: {filename}")
        print(f"📱 Scannez ce badge pour accéder à l'école")
    
    def view_leaderboard(self, limit: int = 10):
        """Affiche le classement des étudiants"""
        print("\n" + "="*50)
        print("🏆 CLASSEMENT XP")
        print("="*50)
        
        sorted_users = sorted(self.users.values(), key=lambda u: u.xp, reverse=True)
        
        for i, user in enumerate(sorted_users[:limit], 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            print(f"{medal} {user.name} - Niveau {user.level} ({user.xp} XP)")
    
    def view_profile(self):
        """Affiche le profil de l'utilisateur connecté"""
        if not self.current_user:
            print("❌ Vous devez être connecté")
            return
        
        u = self.current_user
        print("\n" + "="*50)
        print(f"👤 PROFIL: {u.name}")
        print("="*50)
        print(f"📧 Email: {u.email}")
        print(f"⭐ Niveau: {u.level}")
        print(f"✨ XP: {u.xp}")
        print(f"📚 Projets complétés: {len(u.projects_completed)}")
        print(f"🏆 Badges: {', '.join(u.badges) if u.badges else 'Aucun'}")
        
        # Barre de progression XP
        next_level_xp = ((u.level) ** 2) * 100
        current_level_xp = ((u.level - 1) ** 2) * 100
        progress = ((u.xp - current_level_xp) / (next_level_xp - current_level_xp)) * 100
        bar_length = 20
        filled = int((progress / 100) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"\n📊 Progression: [{bar}] {progress:.1f}%")
        print(f"   Prochain niveau: {next_level_xp - u.xp} XP restants")
    
    def list_projects(self):
        """Liste tous les projets disponibles"""
        print("\n" + "="*50)
        print("📚 PROJETS DISPONIBLES")
        print("="*50)
        
        for project in self.projects.values():
            status = "✅" if project.project_id in (self.current_user.projects_completed if self.current_user else []) else "⭕"
            difficulty_icon = "🟢" if project.difficulty == "Easy" else "🟡" if project.difficulty == "Medium" else "🔴"
            print(f"{status} [{project.project_id}] {project.title}")
            print(f"    {difficulty_icon} {project.difficulty} | 🎁 {project.xp_reward} XP")
    
    def list_events(self):
        """Liste tous les événements"""
        print("\n" + "="*50)
        print("📅 ÉVÉNEMENTS")
        print("="*50)
        
        for event in self.events:
            icon = "🎉" if event.event_type == "BDE" else "💻" if event.event_type == "Workshop" else "🏆"
            print(f"{icon} [{event.event_id}] {event.title}")
            print(f"    📅 {event.date} | 👥 {len(event.participants)} participants")
    
    def save_data(self):
        """Sauvegarde les données dans un fichier JSON"""
        data = {
            'users': {uid: u.to_dict() for uid, u in self.users.items()},
            'projects': {pid: p.to_dict() for pid, p in self.projects.items()},
            'messages': [m.to_dict() for m in self.chat_messages],
            'events': [e.to_dict() for e in self.events]
        }
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print("💾 Données sauvegardées")
    
    def load_data(self):
        """Charge les données depuis le fichier JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Charger les utilisateurs
                for uid, udata in data.get('users', {}).items():
                    user = User(udata['user_id'], udata['name'], udata['email'])
                    user.xp = udata['xp']
                    user.level = udata['level']
                    user.badges = udata['badges']
                    user.projects_completed = udata['projects_completed']
                    self.users[int(uid)] = user
                
                print("✅ Données chargées")
            except Exception as e:
                print(f"⚠️ Erreur de chargement: {e}")


# ==================== INTERFACE CLI ====================

def print_banner():
    """Affiche la bannière de l'application"""
    print("\n" + "="*60)
    print("""
    ██████╗ ██╗      █████╗ ████████╗███████╗███████╗ ██████╗ ██████╗ ███╗   ███╗███████╗
    ██╔══██╗██║     ██╔══██╗╚══██╔══╝██╔════╝██╔════╝██╔═══██╗██╔══██╗████╗ ████║██╔════╝
    ██████╔╝██║     ███████║   ██║   █████╗  █████╗  ██║   ██║██████╔╝██╔████╔██║█████╗  
    ██╔═══╝ ██║     ██╔══██║   ██║   ██╔══╝  ██╔══╝  ██║   ██║██╔══██╗██║╚██╔╝██║██╔══╝  
    ██║     ███████╗██║  ██║   ██║   ███████╗██║     ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
    ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
                                    🎮 XP - Édition Gamifiée 🎮
    """)
    print("="*60 + "\n")


def main_menu():
    """Menu principal de l'application"""
    app = PlateformeXP()
    
    print_banner()
    
    while True:
        print("\n" + "="*50)
        print("🏠 MENU PRINCIPAL")
        print("="*50)
        print("1. 👤 Créer un compte")
        print("2. 🔐 Se connecter")
        print("3. 📊 Voir mon profil")
        print("4. 📚 Projets disponibles")
        print("5. ✅ Compléter un projet")
        print("6. 🤝 Aider un étudiant")
        print("7. 💬 Chat anonyme")
        print("8. 📅 Événements")
        print("9. 🏆 Classement")
        print("10. 📱 Générer badge QR")
        print("11. 💾 Sauvegarder")
        print("0. ❌ Quitter")
        print("="*50)
        
        choice = input("➤ Votre choix: ").strip()
        
        if choice == "1":
            name = input("📝 Nom: ").strip()
            email = input("📧 Email: ").strip()
            app.register_user(name, email)
            
        elif choice == "2":
            try:
                user_id = int(input("🔢 Votre ID utilisateur: ").strip())
                app.login(user_id)
            except ValueError:
                print("❌ ID invalide")
                
        elif choice == "3":
            app.view_profile()
            
        elif choice == "4":
            app.list_projects()
            
        elif choice == "5":
            app.list_projects()
            try:
                project_id = int(input("\n🔢 ID du projet à compléter: ").strip())
                app.complete_project(project_id)
            except ValueError:
                print("❌ ID invalide")
                
        elif choice == "6":
            try:
                helped_id = int(input("🔢 ID de l'étudiant aidé: ").strip())
                app.help_student(helped_id)
            except ValueError:
                print("❌ ID invalide")
                
        elif choice == "7":
            print("\n1. 📖 Lire les messages")
            print("2. ✍️ Poster un message anonyme")
            sub_choice = input("➤ Choix: ").strip()
            
            if sub_choice == "1":
                app.view_chat()
            elif sub_choice == "2":
                msg = input("💬 Votre message: ").strip()
                app.post_anonymous_message(msg)
                
        elif choice == "8":
            app.list_events()
            
        elif choice == "9":
            app.view_leaderboard()
            
        elif choice == "10":
            app.generate_qr_badge()
            
        elif choice == "11":
            app.save_data()
            
        elif choice == "0":
            app.save_data()
            print("\n👋 À bientôt sur Plateforme XP !")
            break
            
        else:
            print("❌ Choix invalide")


# ==================== POINT D'ENTRÉE ====================

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Application fermée")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()