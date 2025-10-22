#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLATEFORME XP - Interface Graphique Moderne
Application étudiante gamifiée pour La Plateforme_
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import json
import os
import qrcode
from PIL import Image, ImageTk
import math

# ==================== CLASSES DU MODÈLE ====================

class Utilisateur:
    def __init__(self, nom, email, promotion="B2"):
        self.nom = nom
        self.email = email
        self.promotion = promotion
        self.xp = 0
        self.niveau = 1
        self.projets_completes = []
        self.badges = []
        self.aides_donnees = 0
        self.aides_recues = 0
        
    def calculer_niveau(self):
        self.niveau = int(math.sqrt(self.xp / 100)) + 1
        return self.niveau
    
    def xp_prochain_niveau(self):
        return (self.niveau ** 2) * 100
    
    def gagner_xp(self, points, raison=""):
        self.xp += points
        ancien_niveau = self.niveau
        self.calculer_niveau()
        return self.niveau > ancien_niveau
    
    def to_dict(self):
        return {
            'nom': self.nom,
            'email': self.email,
            'promotion': self.promotion,
            'xp': self.xp,
            'niveau': self.niveau,
            'projets_completes': self.projets_completes,
            'badges': self.badges,
            'aides_donnees': self.aides_donnees,
            'aides_recues': self.aides_recues
        }
    
    @staticmethod
    def from_dict(data):
        user = Utilisateur(data['nom'], data['email'], data.get('promotion', 'B2'))
        user.xp = data.get('xp', 0)
        user.niveau = data.get('niveau', 1)
        user.projets_completes = data.get('projets_completes', [])
        user.badges = data.get('badges', [])
        user.aides_donnees = data.get('aides_donnees', 0)
        user.aides_recues = data.get('aides_recues', 0)
        return user

class Projet:
    def __init__(self, id, titre, difficulte, xp_reward, description=""):
        self.id = id
        self.titre = titre
        self.difficulte = difficulte
        self.xp_reward = xp_reward
        self.description = description

class PlateformeXP:
    def __init__(self):
        self.utilisateurs = {}
        self.projets = self._initialiser_projets()
        self.messages_chat = []
        self.evenements = self._initialiser_evenements()
        self.charger_donnees()
    
    def _initialiser_projets(self):
        return [
            Projet("P1", "Landing Page HTML/CSS", "Facile", 100, "Créer une page d'atterrissage"),
            Projet("P2", "To-Do List JavaScript", "Facile", 150, "Application de gestion de tâches"),
            Projet("P3", "API REST avec Flask", "Moyen", 300, "Développer une API REST"),
            Projet("P4", "Application React", "Difficile", 500, "Application web moderne en React"),
            Projet("P5", "Projet Full-Stack", "Expert", 800, "Application complète frontend + backend"),
        ]
    
    def _initialiser_evenements(self):
        return [
            {"titre": "🎉 Soirée BDE", "date": "2024-02-15", "type": "BDE"},
            {"titre": "💻 Workshop React", "date": "2024-02-20", "type": "Workshop"},
            {"titre": "🏆 Tournoi Code", "date": "2024-03-01", "type": "Tournoi"},
        ]
    
    def creer_utilisateur(self, nom, email, promotion="B2"):
        if email in self.utilisateurs:
            return None
        user = Utilisateur(nom, email, promotion)
        self.utilisateurs[email] = user
        self.sauvegarder_donnees()
        return user
    
    def obtenir_utilisateur(self, email):
        return self.utilisateurs.get(email)
    
    def completer_projet(self, email, projet_id):
        user = self.utilisateurs.get(email)
        if not user:
            return False
        
        projet = next((p for p in self.projets if p.id == projet_id), None)
        if not projet or projet_id in user.projets_completes:
            return False
        
        user.projets_completes.append(projet_id)
        level_up = user.gagner_xp(projet.xp_reward, f"Projet {projet.titre}")
        self.sauvegarder_donnees()
        return level_up
    
    def ajouter_message_chat(self, message):
        self.messages_chat.append({
            'message': message,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.sauvegarder_donnees()
    
    def obtenir_classement(self, limite=10):
        users_tries = sorted(self.utilisateurs.values(), key=lambda u: u.xp, reverse=True)
        return users_tries[:limite]
    
    def sauvegarder_donnees(self):
        data = {
            'utilisateurs': {email: user.to_dict() for email, user in self.utilisateurs.items()},
            'messages_chat': self.messages_chat
        }
        with open('plateforme_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def charger_donnees(self):
        if os.path.exists('plateforme_data.json'):
            try:
                with open('plateforme_data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.utilisateurs = {
                        email: Utilisateur.from_dict(user_data)
                        for email, user_data in data.get('utilisateurs', {}).items()
                    }
                    self.messages_chat = data.get('messages_chat', [])
            except:
                pass

# ==================== INTERFACE GRAPHIQUE ====================

class PlateformeXPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Plateforme XP 🎮")
        
        # Centrer la fenêtre et la rendre plus grande
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 1400
        window_height = 950
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg="#0a0e27")
        self.root.state('zoomed')  # Maximiser la fenêtre
        
        self.plateforme = PlateformeXP()
        self.utilisateur_actuel = None
        
        # Couleurs du thème
        self.colors = {
            'bg_dark': '#0a0e27',
            'bg_medium': '#1a1f3a',
            'bg_light': '#2a2f4a',
            'accent': '#00d4ff',
            'accent2': '#ff00ff',
            'success': '#00ff88',
            'warning': '#ffaa00',
            'danger': '#ff0055',
            'text': '#ffffff',
            'text_secondary': '#a0a0a0'
        }
        
        self.afficher_ecran_connexion()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # ==================== ÉCRAN DE CONNEXION ====================
    
    def afficher_ecran_connexion(self):
        self.clear_window()
        
        # Frame principale
        main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_frame.pack(fill='both', expand=True)
        
        # Canvas pour le background avec dégradé
        canvas = tk.Canvas(main_frame, bg=self.colors['bg_dark'], highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # Mettre à jour pour obtenir les dimensions réelles
        self.root.update_idletasks()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        # Conteneur central
        center_frame = tk.Frame(canvas, bg=self.colors['bg_medium'], bd=0)
        
        # Centrer dynamiquement selon la taille de l'écran
        x_center = canvas_width // 2 if canvas_width > 1 else 700
        y_center = canvas_height // 2 if canvas_height > 1 else 450
        
        center_window = canvas.create_window(x_center, y_center, window=center_frame, width=600, height=850)
        
        # Logo/Titre
        title_label = tk.Label(
            center_frame,
            text="🎮 PLATEFORME XP",
            font=("Helvetica", 42, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['accent']
        )
        title_label.pack(pady=40)
        
        subtitle_label = tk.Label(
            center_frame,
            text="Level Up Your Skills",
            font=("Helvetica", 16),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Formulaire
        form_frame = tk.Frame(center_frame, bg=self.colors['bg_medium'])
        form_frame.pack(pady=20)
        
        # Email
        tk.Label(
            form_frame,
            text="📧 Email",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['text']
        ).grid(row=0, column=0, sticky='w', padx=20, pady=(0, 5))
        
        email_entry = tk.Entry(
            form_frame,
            font=("Helvetica", 14),
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            insertbackground=self.colors['accent'],
            relief='flat',
            width=30
        )
        email_entry.grid(row=1, column=0, padx=20, pady=(0, 20), ipady=10)
        
        # Nom
        tk.Label(
            form_frame,
            text="👤 Nom",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['text']
        ).grid(row=2, column=0, sticky='w', padx=20, pady=(0, 5))
        
        nom_entry = tk.Entry(
            form_frame,
            font=("Helvetica", 14),
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            insertbackground=self.colors['accent'],
            relief='flat',
            width=30
        )
        nom_entry.grid(row=3, column=0, padx=20, pady=(0, 20), ipady=10)
        
        # Promotion
        tk.Label(
            form_frame,
            text="🎓 Promotion",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['text']
        ).grid(row=4, column=0, sticky='w', padx=20, pady=(0, 5))
        
        promo_var = tk.StringVar(value="B2")
        promo_combo = ttk.Combobox(
            form_frame,
            textvariable=promo_var,
            values=["B1", "B2", "B3", "M1", "M2"],
            font=("Helvetica", 14),
            state='readonly',
            width=28
        )
        promo_combo.grid(row=5, column=0, padx=20, pady=(0, 30), ipady=8)
        
        # Boutons
        btn_frame = tk.Frame(center_frame, bg=self.colors['bg_medium'])
        btn_frame.pack(pady=20)
        
        def creer_compte():
            email = email_entry.get().strip()
            nom = nom_entry.get().strip()
            promo = promo_var.get()
            
            if not email or not nom:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
                return
            
            # Vérifier si l'utilisateur existe déjà
            user = self.plateforme.obtenir_utilisateur(email)
            if user:
                messagebox.showwarning("Attention", f"Un compte existe déjà pour {email}")
                return
            
            # Créer le nouveau compte
            user = self.plateforme.creer_utilisateur(nom, email, promo)
            if user:
                messagebox.showinfo("✅ Compte créé", f"Bienvenue {nom} ! Votre aventure commence maintenant ! 🎮")
                self.utilisateur_actuel = user
                self.afficher_tableau_bord()
        
        def se_connecter():
            email = email_entry.get().strip()
            nom = nom_entry.get().strip()
            
            if not nom and not email:
                messagebox.showerror("Erreur", "Veuillez entrer votre nom ou email")
                return
            
            # Chercher par email ou par nom
            user = None
            if email:
                user = self.plateforme.obtenir_utilisateur(email)
            else:
                # Chercher par nom
                for u in self.plateforme.utilisateurs.values():
                    if u.nom.lower() == nom.lower():
                        user = u
                        break
            
            if not user:
                messagebox.showerror("Erreur", f"Aucun compte trouvé. Créez un compte d'abord !")
                return
            
            messagebox.showinfo("✅ Connexion", f"Content de vous revoir {user.nom} ! 🎮")
            self.utilisateur_actuel = user
            self.afficher_tableau_bord()
        
        # Bouton Créer un compte
        btn_creer = tk.Button(
            btn_frame,
            text="✨ Créer un compte",
            font=("Helvetica", 14, "bold"),
            bg=self.colors['accent'],
            fg=self.colors['bg_dark'],
            activebackground=self.colors['accent2'],
            activeforeground=self.colors['text'],
            relief='flat',
            cursor='hand2',
            width=20,
            command=creer_compte
        )
        btn_creer.pack(pady=10, ipady=12)
        
        # Bouton Se connecter
        btn_connexion = tk.Button(
            btn_frame,
            text="🔑 Se connecter",
            font=("Helvetica", 13),
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            activebackground=self.colors['accent2'],
            activeforeground=self.colors['text'],
            relief='flat',
            cursor='hand2',
            width=20,
            command=se_connecter
        )
        btn_connexion.pack(pady=5, ipady=10)
        
        # Stats générales
        stats_frame = tk.Frame(center_frame, bg=self.colors['bg_dark'])
        stats_frame.pack(side='bottom', fill='x', pady=20)
        
        nb_users = len(self.plateforme.utilisateurs)
        
        tk.Label(
            stats_frame,
            text=f"👥 {nb_users} étudiants inscrits",
            font=("Helvetica", 11),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_secondary']
        ).pack()
    
    # ==================== TABLEAU DE BORD ====================
    
    def afficher_tableau_bord(self):
        self.clear_window()
        
        # Frame principale
        main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_frame.pack(fill='both', expand=True)
        
        # Header
        self.creer_header(main_frame)
        
        # Container avec sidebar + content
        container = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sidebar
        sidebar = tk.Frame(container, bg=self.colors['bg_medium'], width=250)
        sidebar.pack(side='left', fill='y', padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Profil dans sidebar
        self.creer_profil_sidebar(sidebar)
        
        # Menu navigation
        self.creer_menu_navigation(sidebar)
        
        # Contenu principal
        self.content_frame = tk.Frame(container, bg=self.colors['bg_dark'])
        self.content_frame.pack(side='left', fill='both', expand=True)
        
        # Afficher accueil par défaut
        self.afficher_accueil()
    
    def creer_header(self, parent):
        header = tk.Frame(parent, bg=self.colors['bg_medium'], height=80)
        header.pack(fill='x', padx=10, pady=(10, 0))
        header.pack_propagate(False)
        
        # Logo
        tk.Label(
            header,
            text="🎮 PLATEFORME XP",
            font=("Helvetica", 24, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['accent']
        ).pack(side='left', padx=20)
        
        # Info utilisateur
        if self.utilisateur_actuel:
            user_frame = tk.Frame(header, bg=self.colors['bg_medium'])
            user_frame.pack(side='right', padx=20)
            
            tk.Label(
                user_frame,
                text=f"👤 {self.utilisateur_actuel.nom}",
                font=("Helvetica", 14, "bold"),
                bg=self.colors['bg_medium'],
                fg=self.colors['text']
            ).pack(anchor='e')
            
            tk.Label(
                user_frame,
                text=f"Niveau {self.utilisateur_actuel.niveau} • {self.utilisateur_actuel.xp} XP",
                font=("Helvetica", 11),
                bg=self.colors['bg_medium'],
                fg=self.colors['accent']
            ).pack(anchor='e')
    
    def creer_profil_sidebar(self, parent):
        profil_frame = tk.Frame(parent, bg=self.colors['bg_light'])
        profil_frame.pack(fill='x', padx=10, pady=10)
        
        user = self.utilisateur_actuel
        
        # Avatar
        tk.Label(
            profil_frame,
            text="👤",
            font=("Helvetica", 48),
            bg=self.colors['bg_light'],
            fg=self.colors['accent']
        ).pack(pady=(20, 10))
        
        # Nom
        tk.Label(
            profil_frame,
            text=user.nom,
            font=("Helvetica", 16, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['text']
        ).pack()
        
        # Niveau
        tk.Label(
            profil_frame,
            text=f"⭐ Niveau {user.niveau}",
            font=("Helvetica", 14),
            bg=self.colors['bg_light'],
            fg=self.colors['accent']
        ).pack(pady=5)
        
        # Barre XP
        xp_frame = tk.Frame(profil_frame, bg=self.colors['bg_light'])
        xp_frame.pack(fill='x', padx=20, pady=10)
        
        xp_actuel = user.xp
        xp_niveau_actuel = (user.niveau - 1) ** 2 * 100
        xp_prochain = user.xp_prochain_niveau()
        xp_dans_niveau = xp_actuel - xp_niveau_actuel
        xp_requis_niveau = xp_prochain - xp_niveau_actuel
        
        progress = (xp_dans_niveau / xp_requis_niveau) * 100 if xp_requis_niveau > 0 else 0
        
        tk.Label(
            xp_frame,
            text=f"{int(xp_dans_niveau)} / {int(xp_requis_niveau)} XP",
            font=("Helvetica", 10),
            bg=self.colors['bg_light'],
            fg=self.colors['text_secondary']
        ).pack()
        
        # Barre de progression
        progress_bg = tk.Frame(xp_frame, bg=self.colors['bg_dark'], height=20)
        progress_bg.pack(fill='x', pady=5)
        
        progress_fill = tk.Frame(progress_bg, bg=self.colors['accent'], height=20)
        progress_fill.place(x=0, y=0, relwidth=progress/100, relheight=1)
        
        # Stats
        stats_frame = tk.Frame(profil_frame, bg=self.colors['bg_light'])
        stats_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        self.creer_stat_item(stats_frame, "🎯", "Projets", len(user.projets_completes))
        self.creer_stat_item(stats_frame, "🏆", "Badges", len(user.badges))
        self.creer_stat_item(stats_frame, "💡", "Aides", user.aides_donnees)
    
    def creer_stat_item(self, parent, icon, label, value):
        frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        frame.pack(fill='x', pady=2)
        
        tk.Label(
            frame,
            text=f"{icon} {label}:",
            font=("Helvetica", 10),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_secondary']
        ).pack(side='left', padx=10)
        
        tk.Label(
            frame,
            text=str(value),
            font=("Helvetica", 10, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['accent']
        ).pack(side='right', padx=10)
    
    def creer_menu_navigation(self, parent):
        menu_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        menu_frame.pack(fill='both', expand=True, pady=20)
        
        menus = [
            ("🏠", "Accueil", self.afficher_accueil),
            ("🎯", "Projets", self.afficher_projets),
            ("💬", "Chat", self.afficher_chat),
            ("🏆", "Classement", self.afficher_classement),
            ("📅", "Événements", self.afficher_evenements),
            ("🎫", "Mon Badge", self.afficher_badge),
        ]
        
        for icon, text, command in menus:
            btn = tk.Button(
                menu_frame,
                text=f"{icon}  {text}",
                font=("Helvetica", 12, "bold"),
                bg=self.colors['bg_medium'],
                fg=self.colors['text'],
                activebackground=self.colors['bg_light'],
                activeforeground=self.colors['accent'],
                relief='flat',
                cursor='hand2',
                anchor='w',
                padx=20,
                command=command
            )
            btn.pack(fill='x', pady=2)
        
        # Bouton déconnexion
        tk.Button(
            menu_frame,
            text="🚪  Déconnexion",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['danger'],
            fg=self.colors['text'],
            activebackground='#cc0044',
            activeforeground=self.colors['text'],
            relief='flat',
            cursor='hand2',
            anchor='w',
            padx=20,
            command=self.afficher_ecran_connexion
        ).pack(side='bottom', fill='x', pady=10)
    
    # ==================== PAGE ACCUEIL ====================
    
    def afficher_accueil(self):
        self.clear_content()
        
        # Titre
        tk.Label(
            self.content_frame,
            text="🏠 Tableau de Bord",
            font=("Helvetica", 28, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 20))
        
        # Stats cards
        stats_container = tk.Frame(self.content_frame, bg=self.colors['bg_dark'])
        stats_container.pack(fill='x', pady=(0, 20))
        
        user = self.utilisateur_actuel
        
        stats = [
            ("⭐", "Niveau", str(user.niveau), self.colors['accent']),
            ("💎", "XP Total", str(user.xp), self.colors['accent2']),
            ("🎯", "Projets", str(len(user.projets_completes)), self.colors['success']),
            ("🏆", "Badges", str(len(user.badges)), self.colors['warning']),
        ]
        
        for icon, label, value, color in stats:
            self.creer_stat_card(stats_container, icon, label, value, color)
        
        # Contenu en 2 colonnes
        content_container = tk.Frame(self.content_frame, bg=self.colors['bg_dark'])
        content_container.pack(fill='both', expand=True)
        
        # Colonne gauche
        left_col = tk.Frame(content_container, bg=self.colors['bg_dark'])
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Derniers projets
        self.creer_section_projets_recents(left_col)
        
        # Colonne droite
        right_col = tk.Frame(content_container, bg=self.colors['bg_dark'])
        right_col.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Prochains événements
        self.creer_section_evenements_recents(right_col)
        
        # Messages récents
        self.creer_section_messages_recents(right_col)
    
    def creer_stat_card(self, parent, icon, label, value, color):
        card = tk.Frame(parent, bg=self.colors['bg_medium'])
        card.pack(side='left', fill='both', expand=True, padx=5)
        
        tk.Label(
            card,
            text=icon,
            font=("Helvetica", 32),
            bg=self.colors['bg_medium'],
            fg=color
        ).pack(pady=(20, 5))
        
        tk.Label(
            card,
            text=value,
            font=("Helvetica", 28, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['text']
        ).pack()
        
        tk.Label(
            card,
            text=label,
            font=("Helvetica", 12),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_secondary']
        ).pack(pady=(0, 20))
    
    def creer_section_projets_recents(self, parent):
        frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        frame.pack(fill='both', expand=True, pady=(0, 10))
        
        tk.Label(
            frame,
            text="🎯 Projets Disponibles",
            font=("Helvetica", 18, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['text']
        ).pack(anchor='w', padx=20, pady=(20, 10))
        
        projets_restants = [p for p in self.plateforme.projets if p.id not in self.utilisateur_actuel.projets_completes]
        
        if projets_restants:
            for projet in projets_restants[:3]:
                self.creer_projet_card_mini(frame, projet)
        else:
            tk.Label(
                frame,
                text="🎉 Tous les projets complétés !",
                font=("Helvetica", 12),
                bg=self.colors['bg_medium'],
                fg=self.colors['success']
            ).pack(pady=20)
    
    def creer_projet_card_mini(self, parent, projet):
        card = tk.Frame(parent, bg=self.colors['bg_light'])
        card.pack(fill='x', padx=20, pady=5)
        
        info_frame = tk.Frame(card, bg=self.colors['bg_light'])
        info_frame.pack(side='left', fill='x', expand=True, padx=15, pady=10)
        
        tk.Label(
            info_frame,
            text=projet.titre,
            font=("Helvetica", 12, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['text']
        ).pack(anchor='w')
        
        tk.Label(
            info_frame,
            text=f"💎 {projet.xp_reward} XP • {projet.difficulte}",
            font=("Helvetica", 10),
            bg=self.colors['bg_light'],
            fg=self.colors['text_secondary']
        ).pack(anchor='w')
    
    def creer_section_evenements_recents(self, parent):
        frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            frame,
            text="📅 Événements à venir",
            font=("Helvetica", 18, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['text']
        ).pack(anchor='w', padx=20, pady=(20, 10))
        
        for evt in self.plateforme.evenements[:2]:
            self.creer_evenement_card_mini(frame, evt)
    
    def creer_evenement_card_mini(self, parent, evt):
        card = tk.Frame(parent, bg=self.colors['bg_light'])
        card.pack(fill='x', padx=20, pady=5)
        
        tk.Label(
            card,
            text=evt['titre'],
            font=("Helvetica", 11, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['text']
        ).pack(anchor='w', padx=15, pady=(10, 2))
        
        tk.Label(
            card,
            text=f"📅 {evt['date']}",
            font=("Helvetica", 9),
            bg=self.colors['bg_light'],
            fg=self.colors['text_secondary']
        ).pack(anchor='w', padx=15, pady=(0, 10))
    
    def creer_section_messages_recents(self, parent):
        frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        frame.pack(fill='both', expand=True)
        
        tk.Label(
            frame,
            text="💬 Chat Récent",
            font=("Helvetica", 18, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['text']
        ).pack(anchor='w', padx=20, pady=(20, 10))
        
        messages_recents = self.plateforme.messages_chat[-3:]
        
        if messages_recents:
            for msg in messages_recents:
                self.creer_message_card_mini(frame, msg)
        else:
            tk.Label(
                frame,
                text="Aucun message pour le moment",
                font=("Helvetica", 10),
                bg=self.colors['bg_medium'],
                fg=self.colors['text_secondary']
            ).pack(pady=20)
    
    def creer_message_card_mini(self, parent, msg):
        card = tk.Frame(parent, bg=self.colors['bg_light'])
        card.pack(fill='x', padx=20, pady=5)
        
        tk.Label(
            card,
            text=f"💬 {msg['message'][:50]}...",
            font=("Helvetica", 10),
            bg=self.colors['bg_light'],
            fg=self.colors['text']
        ).pack(anchor='w', padx=15, pady=(10, 2))
        
        tk.Label(
            card,
            text=msg['timestamp'],
            font=("Helvetica", 8),
            bg=self.colors['bg_light'],
            fg=self.colors['text_secondary']
        ).pack(anchor='w', padx=15, pady=(0, 10))
    
    # ==================== PAGE PROJETS ====================
    
    def afficher_projets(self):
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="🎯 Projets",
            font=("Helvetica", 28, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 20))
        
        # Scrollable frame
        canvas = tk.Canvas(self.content_frame, bg=self.colors['bg_dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_dark'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        for projet in self.plateforme.projets:
            self.creer_projet_card(scrollable_frame, projet)
    
    def creer_projet_card(self, parent, projet):
        est_complete = projet.id in self.utilisateur_actuel.projets_completes
        
        card = tk.Frame(
            parent,
            bg=self.colors['success'] if est_complete else self.colors['bg_medium']
        )
        card.pack(fill='x', pady=10, padx=10)
        
        # En-tête
        header = tk.Frame(card, bg=card['bg'])
        header.pack(fill='x', padx=20, pady=(20, 10))
        
        tk.Label(
            header,
            text="✅ " + projet.titre if est_complete else projet.titre,
            font=("Helvetica", 18, "bold"),
            bg=card['bg'],
            fg=self.colors['text']
        ).pack(side='left')
        
        badge_color = {
            'Facile': self.colors['success'],
            'Moyen': self.colors['warning'],
            'Difficile': self.colors['danger'],
            'Expert': self.colors['accent2']
        }.get(projet.difficulte, self.colors['text_secondary'])
        
        tk.Label(
            header,
            text=projet.difficulte,
            font=("Helvetica", 10, "bold"),
            bg=badge_color,
            fg=self.colors['text'],
            padx=10,
            pady=5
        ).pack(side='right')
        
        # Description
        tk.Label(
            card,
            text=projet.description,
            font=("Helvetica", 11),
            bg=card['bg'],
            fg=self.colors['text_secondary'],
            wraplength=700,
            justify='left'
        ).pack(anchor='w', padx=20, pady=(0, 10))
        
        # Footer
        footer = tk.Frame(card, bg=card['bg'])
        footer.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Label(
            footer,
            text=f"💎 Récompense: {projet.xp_reward} XP",
            font=("Helvetica", 12, "bold"),
            bg=card['bg'],
            fg=self.colors['accent']
        ).pack(side='left')
        
        if not est_complete:
            btn = tk.Button(
                footer,
                text="✓ Marquer comme terminé",
                font=("Helvetica", 11, "bold"),
                bg=self.colors['accent'],
                fg=self.colors['bg_dark'],
                activebackground=self.colors['accent2'],
                relief='flat',
                cursor='hand2',
                padx=20,
                pady=8,
                command=lambda p=projet: self.completer_projet(p)
            )
            btn.pack(side='right')
    
    def completer_projet(self, projet):
        level_up = self.plateforme.completer_projet(self.utilisateur_actuel.email, projet.id)
        
        if level_up:
            messagebox.showinfo(
                "🎉 LEVEL UP!",
                f"Félicitations! Vous êtes maintenant niveau {self.utilisateur_actuel.niveau}!\n+{projet.xp_reward} XP"
            )
        else:
            messagebox.showinfo(
                "✅ Projet terminé",
                f"Bravo! +{projet.xp_reward} XP"
            )
        
        self.afficher_projets()
    
    # ==================== PAGE CHAT ====================
    
    def afficher_chat(self):
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="💬 Chat Anonyme",
            font=("Helvetica", 28, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 20))
        
        chat_frame = tk.Frame(self.content_frame, bg=self.colors['bg_medium'])
        chat_frame.pack(fill='both', expand=True)
        
        # Messages
        messages_frame = tk.Frame(chat_frame, bg=self.colors['bg_medium'])
        messages_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        canvas = tk.Canvas(messages_frame, bg=self.colors['bg_medium'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(messages_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_medium'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        for msg in self.plateforme.messages_chat:
            self.creer_message_bubble(scrollable_frame, msg)
        
        if not self.plateforme.messages_chat:
            tk.Label(
                scrollable_frame,
                text="💬 Aucun message. Soyez le premier à poser une question!",
                font=("Helvetica", 12),
                bg=self.colors['bg_medium'],
                fg=self.colors['text_secondary']
            ).pack(pady=50)
        
        # Input
        input_frame = tk.Frame(chat_frame, bg=self.colors['bg_light'])
        input_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        message_entry = tk.Text(
            input_frame,
            font=("Helvetica", 11),
            bg=self.colors['bg_dark'],
            fg=self.colors['text'],
            insertbackground=self.colors['accent'],
            relief='flat',
            height=3,
            wrap='word'
        )
        message_entry.pack(side='left', fill='both', expand=True, padx=(10, 5), pady=10)
        
        def envoyer_message():
            msg = message_entry.get("1.0", "end-1c").strip()
            if msg:
                self.plateforme.ajouter_message_chat(msg)
                message_entry.delete("1.0", "end")
                self.afficher_chat()
                messagebox.showinfo("✅", "Message envoyé!")
        
        btn_envoyer = tk.Button(
            input_frame,
            text="📤\nEnvoyer",
            font=("Helvetica", 10, "bold"),
            bg=self.colors['accent'],
            fg=self.colors['bg_dark'],
            activebackground=self.colors['accent2'],
            relief='flat',
            cursor='hand2',
            width=10,
            command=envoyer_message
        )
        btn_envoyer.pack(side='right', padx=(5, 10), pady=10, fill='y')
    
    def creer_message_bubble(self, parent, msg):
        bubble = tk.Frame(parent, bg=self.colors['bg_light'])
        bubble.pack(fill='x', pady=5, padx=10)
        
        tk.Label(
            bubble,
            text=f"👤 Anonyme",
            font=("Helvetica", 9, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['accent']
        ).pack(anchor='w', padx=15, pady=(10, 2))
        
        tk.Label(
            bubble,
            text=msg['message'],
            font=("Helvetica", 11),
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            wraplength=600,
            justify='left'
        ).pack(anchor='w', padx=15, pady=(0, 5))
        
        tk.Label(
            bubble,
            text=msg['timestamp'],
            font=("Helvetica", 8),
            bg=self.colors['bg_light'],
            fg=self.colors['text_secondary']
        ).pack(anchor='e', padx=15, pady=(0, 10))
    
    # ==================== PAGE CLASSEMENT ====================
    
    def afficher_classement(self):
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="🏆 Classement",
            font=("Helvetica", 28, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 20))
        
        classement_frame = tk.Frame(self.content_frame, bg=self.colors['bg_medium'])
        classement_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        top_users = self.plateforme.obtenir_classement(20)
        
        for i, user in enumerate(top_users, 1):
            self.creer_classement_row(classement_frame, i, user)
    
    def creer_classement_row(self, parent, position, user):
        est_actuel = user.email == self.utilisateur_actuel.email
        
        row = tk.Frame(
            parent,
            bg=self.colors['accent'] if est_actuel else self.colors['bg_light']
        )
        row.pack(fill='x', padx=20, pady=5)
        
        # Position
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(position, f"#{position}")
        tk.Label(
            row,
            text=medal,
            font=("Helvetica", 18, "bold"),
            bg=row['bg'],
            fg=self.colors['text'],
            width=5
        ).pack(side='left', padx=(15, 10), pady=10)
        
        # Info user
        info_frame = tk.Frame(row, bg=row['bg'])
        info_frame.pack(side='left', fill='x', expand=True, pady=10)
        
        name_text = f"{user.nom} (Vous)" if est_actuel else user.nom
        tk.Label(
            info_frame,
            text=name_text,
            font=("Helvetica", 14, "bold"),
            bg=row['bg'],
            fg=self.colors['text']
        ).pack(anchor='w')
        
        tk.Label(
            info_frame,
            text=f"Niveau {user.niveau} • {len(user.projets_completes)} projets",
            font=("Helvetica", 10),
            bg=row['bg'],
            fg=self.colors['text_secondary']
        ).pack(anchor='w')
        
        # XP
        tk.Label(
            row,
            text=f"{user.xp} XP",
            font=("Helvetica", 16, "bold"),
            bg=row['bg'],
            fg=self.colors['accent'] if not est_actuel else self.colors['bg_dark']
        ).pack(side='right', padx=15)
    
    # ==================== PAGE ÉVÉNEMENTS ====================
    
    def afficher_evenements(self):
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="📅 Événements",
            font=("Helvetica", 28, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 20))
        
        for evt in self.plateforme.evenements:
            self.creer_evenement_card(self.content_frame, evt)
    
    def creer_evenement_card(self, parent, evt):
        card = tk.Frame(parent, bg=self.colors['bg_medium'])
        card.pack(fill='x', pady=10, padx=10)
        
        icon_map = {
            'BDE': '🎉',
            'Workshop': '💻',
            'Tournoi': '🏆'
        }
        icon = icon_map.get(evt['type'], '📅')
        
        tk.Label(
            card,
            text=f"{icon} {evt['titre']}",
            font=("Helvetica", 18, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['text']
        ).pack(anchor='w', padx=20, pady=(20, 5))
        
        tk.Label(
            card,
            text=f"📅 {evt['date']} • Type: {evt['type']}",
            font=("Helvetica", 12),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_secondary']
        ).pack(anchor='w', padx=20, pady=(0, 20))
    
    # ==================== PAGE BADGE ====================
    
    def afficher_badge(self):
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="🎫 Mon Badge Numérique",
            font=("Helvetica", 28, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 20))
        
        badge_frame = tk.Frame(self.content_frame, bg=self.colors['bg_medium'])
        badge_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        user = self.utilisateur_actuel
        
        # Infos du badge
        info_frame = tk.Frame(badge_frame, bg=self.colors['bg_medium'])
        info_frame.pack(pady=30)
        
        tk.Label(
            info_frame,
            text="👤",
            font=("Helvetica", 64),
            bg=self.colors['bg_medium'],
            fg=self.colors['accent']
        ).pack(pady=20)
        
        tk.Label(
            info_frame,
            text=user.nom,
            font=("Helvetica", 24, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['text']
        ).pack(pady=5)
        
        tk.Label(
            info_frame,
            text=f"⭐ Niveau {user.niveau} • {user.xp} XP",
            font=("Helvetica", 16),
            bg=self.colors['bg_medium'],
            fg=self.colors['accent']
        ).pack(pady=5)
        
        tk.Label(
            info_frame,
            text=f"🎓 {user.promotion}",
            font=("Helvetica", 14),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_secondary']
        ).pack(pady=5)
        
        # Bouton générer QR
        def generer_qr():
            try:
                data = f"Plateforme XP - {user.nom} - Niveau {user.niveau} - {user.xp} XP"
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                filename = f"badge_{user.email.replace('@', '_').replace('.', '_')}.png"
                img.save(filename)
                messagebox.showinfo("✅ Badge généré", f"Badge QR code sauvegardé:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de générer le QR code:\n{e}")
        
        tk.Button(
            info_frame,
            text="📱 Générer QR Code",
            font=("Helvetica", 14, "bold"),
            bg=self.colors['accent'],
            fg=self.colors['bg_dark'],
            activebackground=self.colors['accent2'],
            relief='flat',
            cursor='hand2',
            padx=30,
            pady=15,
            command=generer_qr
        ).pack(pady=30)
    
    # ==================== UTILS ====================
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

# ==================== MAIN ====================

def main():
    root = tk.Tk()
    app = PlateformeXPGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
