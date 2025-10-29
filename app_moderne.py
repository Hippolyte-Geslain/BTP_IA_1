import customtkinter as ctk
from tkinter import messagebox, Canvas
import json
from datetime import datetime
import random
import calendar

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PlateformeXPApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Plateforme XP - Application Étudiante")
        self.geometry("1200x800")
        self.resizable(True, True)
        
        self.current_user = None
        self.create_login_screen()
    
    def create_login_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        login_frame = ctk.CTkFrame(main_frame, corner_radius=20, fg_color=("#f0f0f0", "#1a1a1a"))
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = ctk.CTkLabel(
            login_frame,
            text="🎮 Plateforme XP",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color=("#2b6cb0", "#4a9eff")
        )
        title.pack(pady=(40, 10))
        
        subtitle = ctk.CTkLabel(
            login_frame,
            text="L'application des étudiants de La Plateforme_",
            font=ctk.CTkFont(size=16),
            text_color=("gray50", "gray70")
        )
        subtitle.pack(pady=(0, 40))
        
        self.login_email = ctk.CTkEntry(
            login_frame,
            placeholder_text="📧 Email",
            width=400,
            height=50,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        self.login_email.pack(pady=10, padx=50)
        
        self.login_password = ctk.CTkEntry(
            login_frame,
            placeholder_text="🔐 Mot de passe",
            width=400,
            height=50,
            font=ctk.CTkFont(size=14),
            corner_radius=10,
            show="•"
        )
        self.login_password.pack(pady=10, padx=50)
        
        button_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        button_frame.pack(pady=30, padx=50)
        
        login_btn = ctk.CTkButton(
            button_frame,
            text="🔓 Se connecter",
            command=self.login,
            width=180,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            fg_color=("#48bb78", "#48bb78"),
            hover_color=("#38a169", "#38a169")
        )
        login_btn.pack(side="left", padx=10)
    
    def login(self):
        email = self.login_email.get().strip()
        password = self.login_password.get().strip()
        
        if not email or not password:
            messagebox.showwarning("Attention", "Veuillez entrer votre email et mot de passe !")
            return
        
        try:
            with open("plateforme_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict) or "users" not in data:
                    data = {"users": []}
            
            for user in data.get("users", []):
                if isinstance(user, dict) and user.get("email") == email:
                    # Vérifier le mot de passe
                    if user.get("password") == password:
                        self.current_user = user
                        messagebox.showinfo("Succès", f"Bienvenue {user['nom']} !")
                        self.create_main_app()
                        return
                    else:
                        messagebox.showerror("Erreur", "Mot de passe incorrect !")
                        return
            
            messagebox.showerror("Erreur", "Aucun compte trouvé avec cet email !")
        except:
            messagebox.showerror("Erreur", "Aucun utilisateur enregistré !")
    
    def create_main_app(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=("#e0e0e0", "#0f0f0f"))
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        logo = ctk.CTkLabel(
            self.sidebar,
            text="🎮 Plateforme XP",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#2b6cb0", "#4a9eff")
        )
        logo.pack(pady=(30, 10))
        
        user_label = ctk.CTkLabel(
            self.sidebar,
            text=f"👤 {self.current_user['nom']}",
            font=ctk.CTkFont(size=14),
            text_color=("gray30", "gray70")
        )
        user_label.pack(pady=(0, 30))
        
        buttons = [
            ("📊 Tableau de bord", self.show_dashboard),
            ("🏆 Mes Projets", self.show_projects),
            ("⭐ Mes Badges", self.show_badges),
            ("💬 Chat", self.show_chat),
            ("📅 Calendrier", self.show_calendar),
            ("🎯 Tournois", self.show_tournaments),
            ("📚 Partage de cours", self.show_courses),
            ("👥 Tutorat", self.show_tutoring),
            ("🗺️ Bons plans", self.show_deals),
            ("💼 Coach carrière", self.show_career),
        ]
        
        for text, command in buttons:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                width=230,
                height=45,
                font=ctk.CTkFont(size=14),
                corner_radius=10,
                fg_color="transparent",
                hover_color=("#d0d0d0", "#2a2a2a"),
                anchor="w",
                text_color=("gray20", "gray80")
            )
            btn.pack(pady=5, padx=10)
        
        logout_btn = ctk.CTkButton(
            self.sidebar,
            text="🚪 Déconnexion",
            command=self.create_login_screen,
            width=230,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10,
            fg_color=("#e53e3e", "#e53e3e"),
            hover_color=("#c53030", "#c53030")
        )
        logout_btn.pack(side="bottom", pady=20, padx=10)
        
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.show_dashboard()
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        self.clear_content()
        
        title = ctk.CTkLabel(
            self.content_frame,
            text="📊 Tableau de bord",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        title.pack(pady=(0, 30), anchor="w")
        
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=20)
        
        stats = [
            ("🎯 XP Total", str(self.current_user['xp']), "#4a9eff"),
            ("📈 Niveau", str(self.current_user['niveau']), "#48bb78"),
            ("🏆 Badges", str(len(self.current_user.get('badges', []))), "#f6ad55"),
            ("📚 Projets", str(len(self.current_user.get('projets', []))), "#9f7aea"),
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = ctk.CTkFrame(stats_frame, corner_radius=15, fg_color=color)
            card.grid(row=0, column=i, padx=10, sticky="ew")
            stats_frame.grid_columnconfigure(i, weight=1)
            
            ctk.CTkLabel(
                card,
                text=label,
                font=ctk.CTkFont(size=14),
                text_color="white"
            ).pack(pady=(20, 5))
            
            ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(size=48, weight="bold"),
                text_color="white"
            ).pack(pady=(0, 20))
        
        welcome = ctk.CTkFrame(self.content_frame, corner_radius=15)
        welcome.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(
            welcome,
            text=f"👋 Bienvenue {self.current_user['nom']} !",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=30)
        
        ctk.CTkLabel(
            welcome,
            text="🎮 Continuez à accumuler de l'XP en complétant vos projets !",
            font=ctk.CTkFont(size=16),
            text_color=("gray50", "gray70")
        ).pack(pady=10)
    
    def show_projects(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="🏆 Mes Projets", font=ctk.CTkFont(size=36, weight="bold"))
        title.pack(pady=(0, 20), anchor="w")
        
        add_btn = ctk.CTkButton(
            self.content_frame,
            text="➕ Ajouter un projet",
            command=self.add_project,
            width=200,
            height=40,
            fg_color="#48bb78",
            hover_color="#38a169"
        )
        add_btn.pack(pady=10, anchor="w")
        
        scrollable = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, pady=10)
        
        projects = self.current_user.get('projets', [])
        if not projects:
            ctk.CTkLabel(
                scrollable,
                text="📝 Aucun projet pour le moment. Ajoutez votre premier projet !",
                font=ctk.CTkFont(size=16),
                text_color=("gray50", "gray70")
            ).pack(pady=50)
        else:
            for project in projects:
                self.create_project_card(scrollable, project)
    
    def create_project_card(self, parent, project):
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color=("#f0f0f0", "#1a1a1a"))
        card.pack(fill="x", pady=10, padx=5)
        
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            header,
            text=project['nom'],
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")
        
        status_colors = {"En cours": "#f6ad55", "Terminé": "#48bb78", "À faire": "#4a9eff"}
        status_badge = ctk.CTkLabel(
            header,
            text=project['statut'],
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=status_colors.get(project['statut'], "#gray"),
            corner_radius=8,
            text_color="white"
        )
        status_badge.pack(side="right", padx=5, pady=5)
        
        ctk.CTkLabel(
            card,
            text=f"📝 {project['description']}",
            font=ctk.CTkFont(size=14),
            text_color=("gray40", "gray70")
        ).pack(anchor="w", padx=20, pady=5)
        
        ctk.CTkLabel(
            card,
            text=f"⭐ XP: {project['xp']} | 📅 Deadline: {project['deadline']}",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60")
        ).pack(anchor="w", padx=20, pady=(5, 15))
    
    def add_project(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Ajouter un projet")
        dialog.geometry("500x600")
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="➕ Nouveau Projet", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        name_entry = ctk.CTkEntry(dialog, placeholder_text="Nom du projet", width=400, height=45)
        name_entry.pack(pady=10)
        
        desc_entry = ctk.CTkTextbox(dialog, width=400, height=100)
        desc_entry.insert("1.0", "Description du projet...")
        desc_entry.pack(pady=10)
        
        status_var = ctk.StringVar(value="À faire")
        ctk.CTkLabel(dialog, text="Statut:", font=ctk.CTkFont(size=14)).pack(pady=5)
        status_menu = ctk.CTkOptionMenu(dialog, values=["À faire", "En cours", "Terminé"], variable=status_var, width=400)
        status_menu.pack(pady=5)
        
        xp_entry = ctk.CTkEntry(dialog, placeholder_text="XP (ex: 500)", width=400, height=45)
        xp_entry.pack(pady=10)
        
        deadline_entry = ctk.CTkEntry(dialog, placeholder_text="Deadline (YYYY-MM-DD)", width=400, height=45)
        deadline_entry.pack(pady=10)
        
        def save_project():
            new_project = {
                "nom": name_entry.get(),
                "description": desc_entry.get("1.0", "end-1c"),
                "statut": status_var.get(),
                "xp": int(xp_entry.get() or 0),
                "deadline": deadline_entry.get()
            }
            
            if 'projets' not in self.current_user:
                self.current_user['projets'] = []
            self.current_user['projets'].append(new_project)
            
            if new_project['statut'] == "Terminé":
                self.current_user['xp'] += new_project['xp']
            
            self.save_user_data()
            dialog.destroy()
            self.show_projects()
        
        ctk.CTkButton(
            dialog,
            text="💾 Enregistrer",
            command=save_project,
            width=400,
            height=50,
            fg_color="#48bb78",
            hover_color="#38a169",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
    
    def show_badges(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="⭐ Mes Badges", font=ctk.CTkFont(size=36, weight="bold"))
        title.pack(pady=(0, 20), anchor="w")
        
        scrollable = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, pady=10)
        
        all_badges = [
            {"nom": "🥇 Premier Projet", "description": "Terminer votre premier projet", "xp_requis": 0},
            {"nom": "🚀 Débutant", "description": "Atteindre 500 XP", "xp_requis": 500},
            {"nom": "⚡ Intermédiaire", "description": "Atteindre 1000 XP", "xp_requis": 1000},
            {"nom": "💎 Expert", "description": "Atteindre 2500 XP", "xp_requis": 2500},
            {"nom": "🏆 Maître", "description": "Atteindre 5000 XP", "xp_requis": 5000},
            {"nom": "👥 Mentor", "description": "Aider 10 étudiants en tutorat", "xp_requis": 0},
            {"nom": "📚 Bibliothécaire", "description": "Partager 20 ressources", "xp_requis": 0},
            {"nom": "🎯 Champion", "description": "Gagner 5 tournois", "xp_requis": 0},
        ]
        
        grid_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        user_badges = self.current_user.get('badges', [])
        current_xp = self.current_user.get('xp', 0)
        
        for i, badge in enumerate(all_badges):
            row = i // 3
            col = i % 3
            
            is_unlocked = (badge['xp_requis'] <= current_xp) or (badge['nom'] in user_badges)
            
            card = ctk.CTkFrame(
                grid_frame,
                corner_radius=15,
                fg_color=("#48bb78" if is_unlocked else "#2a2a2a"),
                width=250,
                height=200
            )
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            ctk.CTkLabel(
                card,
                text=badge['nom'].split()[0],
                font=ctk.CTkFont(size=48)
            ).pack(pady=(20, 10))
            
            ctk.CTkLabel(
                card,
                text=badge['nom'].split(' ', 1)[1] if ' ' in badge['nom'] else badge['nom'],
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="white"
            ).pack(pady=5)
            
            ctk.CTkLabel(
                card,
                text=badge['description'],
                font=ctk.CTkFont(size=11),
                text_color=("white" if is_unlocked else "gray70"),
                wraplength=200
            ).pack(pady=5, padx=10)
            
            if not is_unlocked and badge['xp_requis'] > 0:
                ctk.CTkLabel(
                    card,
                    text=f"🔒 {badge['xp_requis']} XP requis",
                    font=ctk.CTkFont(size=10),
                    text_color="gray60"
                ).pack(pady=5)
        
        for col in range(3):
            grid_frame.grid_columnconfigure(col, weight=1)
    
    def show_chat(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="💬 Chat Anonyme", font=ctk.CTkFont(size=36, weight="bold"))
        title.pack(pady=(0, 20), anchor="w")
        
        chat_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        chat_container.pack(fill="both", expand=True)
        
        self.chat_display = ctk.CTkTextbox(
            chat_container,
            wrap="word",
            font=ctk.CTkFont(size=14),
            state="disabled"
        )
        self.chat_display.pack(fill="both", expand=True, pady=(0, 10))
        
        if not hasattr(self, 'chat_messages'):
            self.chat_messages = [
                {"user": "Étudiant342", "message": "Salut ! Quelqu'un peut m'aider avec le projet Python ?"},
                {"user": "Mentor789", "message": "Oui bien sûr ! Quelle est ta question ?"},
                {"user": "Étudiant342", "message": "Je ne comprends pas les listes en compréhension..."},
                {"user": "Mentor789", "message": "C'est simple ! Par exemple: [x*2 for x in range(10)]"},
            ]
        
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        for msg in self.chat_messages:
            self.chat_display.insert("end", f"{msg['user']}: {msg['message']}\n\n")
        self.chat_display.configure(state="disabled")
        
        input_frame = ctk.CTkFrame(chat_container, fg_color="transparent")
        input_frame.pack(fill="x", pady=10)
        
        self.chat_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="💬 Écrivez votre message anonyme...",
            height=50,
            font=ctk.CTkFont(size=14)
        )
        self.chat_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        send_btn = ctk.CTkButton(
            input_frame,
            text="📤 Envoyer",
            command=self.send_message,
            width=120,
            height=50,
            fg_color="#4a9eff",
            hover_color="#3182ce",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        send_btn.pack(side="right")
        
        self.chat_input.bind("<Return>", lambda e: self.send_message())
    
    def send_message(self):
        message = self.chat_input.get().strip()
        if message:
            anonymous_id = f"Étudiant{random.randint(100, 999)}"
            self.chat_messages.append({"user": anonymous_id, "message": message})
            
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f"{anonymous_id}: {message}\n\n")
            self.chat_display.see("end")
            self.chat_display.configure(state="disabled")
            
            self.chat_input.delete(0, "end")
            self.current_user['xp'] += 5
            self.save_user_data()
    
    def show_calendar(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="📅 Calendrier & Événements", font=ctk.CTkFont(size=36, weight="bold"))
        title.pack(pady=(0, 20), anchor="w")
        
        container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        container.pack(fill="both", expand=True)
        
        left_panel = ctk.CTkFrame(container, fg_color="transparent")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        cal_frame = ctk.CTkFrame(left_panel, corner_radius=15)
        cal_frame.pack(fill="x", pady=10)
        
        now = datetime.now()
        month_name = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                      "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        
        ctk.CTkLabel(
            cal_frame,
            text=f"📅 {month_name[now.month-1]} {now.year}",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        days = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        days_frame = ctk.CTkFrame(cal_frame, fg_color="transparent")
        days_frame.pack(pady=10, padx=20)
        
        for i, day in enumerate(days):
            ctk.CTkLabel(
                days_frame,
                text=day,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=50
            ).grid(row=0, column=i, padx=2)
        
        cal = calendar.monthcalendar(now.year, now.month)
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day == 0:
                    ctk.CTkLabel(days_frame, text="", width=50).grid(row=week_num+1, column=day_num)
                else:
                    is_today = (day == now.day)
                    day_btn = ctk.CTkButton(
                        days_frame,
                        text=str(day),
                        width=50,
                        height=40,
                        fg_color=("#4a9eff" if is_today else "transparent"),
                        hover_color=("#3182ce" if is_today else "#2a2a2a"),
                        font=ctk.CTkFont(size=14, weight="bold" if is_today else "normal")
                    )
                    day_btn.grid(row=week_num+1, column=day_num, pady=2, padx=2)
        
        right_panel = ctk.CTkScrollableFrame(container, width=400, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True)
        
        ctk.CTkLabel(
            right_panel,
            text="🎯 Événements à venir",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(0, 20), anchor="w")
        
        events = [
            {"titre": "Présentation Projet Final", "date": "2025-10-28", "type": "🎓", "color": "#e53e3e"},
            {"titre": "Hackathon La Plateforme", "date": "2025-11-05", "type": "💻", "color": "#9f7aea"},
            {"titre": "Workshop React", "date": "2025-10-25", "type": "📚", "color": "#48bb78"},
            {"titre": "Réunion BDE", "date": "2025-10-30", "type": "🎉", "color": "#f6ad55"},
        ]
        
        for event in sorted(events, key=lambda x: x['date']):
            event_card = ctk.CTkFrame(right_panel, corner_radius=10, fg_color=event['color'])
            event_card.pack(fill="x", pady=8)
            
            ctk.CTkLabel(
                event_card,
                text=f"{event['type']} {event['titre']}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="white"
            ).pack(pady=(15, 5), padx=15, anchor="w")
            
            ctk.CTkLabel(
                event_card,
                text=f"📅 {event['date']}",
                font=ctk.CTkFont(size=12),
                text_color="white"
            ).pack(pady=(0, 15), padx=15, anchor="w")
        
        add_event_btn = ctk.CTkButton(
            right_panel,
            text="➕ Ajouter un événement",
            command=lambda: messagebox.showinfo("Info", "Fonctionnalité ajout d'événement !"),
            height=45,
            fg_color="#48bb78",
            hover_color="#38a169"
        )
        add_event_btn.pack(pady=20, fill="x")
    
    def show_tournaments(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="🎯 Tournois & Compétitions", font=ctk.CTkFont(size=36, weight="bold"))
        title.pack(pady=(0, 20), anchor="w")
        
        create_btn = ctk.CTkButton(
            self.content_frame,
            text="➕ Créer un tournoi",
            command=self.create_tournament,
            width=200,
            height=45,
            fg_color="#9f7aea",
            hover_color="#805ad5"
        )
        create_btn.pack(pady=10, anchor="w")
        
        scrollable = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, pady=10)
        
        tournaments = [
            {
                "nom": "🏆 Code Challenge - Algorithmes",
                "participants": 24,
                "max_participants": 32,
                "date": "2025-11-10",
                "xp_reward": 500,
                "status": "Ouvert"
            },
            {
                "nom": "⚡ Speed Coding Challenge",
                "participants": 15,
                "max_participants": 20,
                "date": "2025-11-15",
                "xp_reward": 300,
                "status": "Ouvert"
            },
            {
                "nom": "💻 Hackathon 48h",
                "participants": 32,
                "max_participants": 32,
                "date": "2025-12-01",
                "xp_reward": 1000,
                "status": "Complet"
            },
        ]
        
        for tournament in tournaments:
            card = ctk.CTkFrame(scrollable, corner_radius=15, fg_color=("#f0f0f0", "#1a1a1a"))
            card.pack(fill="x", pady=10, padx=5)
            
            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=20, pady=15)
            
            ctk.CTkLabel(
                header,
                text=tournament['nom'],
                font=ctk.CTkFont(size=22, weight="bold")
            ).pack(side="left")
            
            status_color = "#48bb78" if tournament['status'] == "Ouvert" else "#e53e3e"
            ctk.CTkLabel(
                header,
                text=tournament['status'],
                fg_color=status_color,
                corner_radius=8,
                text_color="white",
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(side="right", padx=5, pady=5)
            
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(fill="x", padx=20, pady=10)
            
            info_items = [
                f"👥 {tournament['participants']}/{tournament['max_participants']} participants",
                f"📅 {tournament['date']}",
                f"⭐ Récompense: {tournament['xp_reward']} XP"
            ]
            
            for item in info_items:
                ctk.CTkLabel(
                    info_frame,
                    text=item,
                    font=ctk.CTkFont(size=14),
                    text_color=("gray40", "gray70")
                ).pack(anchor="w", pady=2)
            
            if tournament['status'] == "Ouvert":
                join_btn = ctk.CTkButton(
                    card,
                    text="🎮 Rejoindre le tournoi",
                    command=lambda t=tournament: self.join_tournament(t),
                    height=40,
                    fg_color="#4a9eff",
                    hover_color="#3182ce"
                )
                join_btn.pack(pady=15, padx=20, fill="x")
    
    def create_tournament(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Créer un tournoi")
        dialog.geometry("500x550")
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="🎯 Nouveau Tournoi", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        name_entry = ctk.CTkEntry(dialog, placeholder_text="Nom du tournoi", width=400, height=45)
        name_entry.pack(pady=10)
        
        max_entry = ctk.CTkEntry(dialog, placeholder_text="Nombre max de participants", width=400, height=45)
        max_entry.pack(pady=10)
        
        date_entry = ctk.CTkEntry(dialog, placeholder_text="Date (YYYY-MM-DD)", width=400, height=45)
        date_entry.pack(pady=10)
        
        xp_entry = ctk.CTkEntry(dialog, placeholder_text="XP récompense", width=400, height=45)
        xp_entry.pack(pady=10)
        
        ctk.CTkButton(
            dialog,
            text="✨ Créer",
            command=lambda: [messagebox.showinfo("Succès", "Tournoi créé !"), dialog.destroy()],
            width=400,
            height=50,
            fg_color="#9f7aea",
            hover_color="#805ad5",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=30)
    
    def join_tournament(self, tournament):
        messagebox.showinfo("Succès", f"Vous avez rejoint: {tournament['nom']} !")
        self.current_user['xp'] += 10
        self.save_user_data()
    
    def show_courses(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="📚 Partage de Cours & Ressources", font=ctk.CTkFont(size=36, weight="bold"))
        title.pack(pady=(0, 20), anchor="w")
        
        add_btn = ctk.CTkButton(
            self.content_frame,
            text="➕ Partager une ressource",
            command=self.add_course,
            width=250,
            height=45,
            fg_color="#48bb78",
            hover_color="#38a169"
        )
        add_btn.pack(pady=10, anchor="w")
        
        search_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=10)
        
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Rechercher un cours...",
            height=45,
            font=ctk.CTkFont(size=14)
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        filter_menu = ctk.CTkOptionMenu(
            search_frame,
            values=["Tous", "Python", "JavaScript", "React", "Node.js", "Bases de données"],
            width=200,
            height=45
        )
        filter_menu.pack(side="right")
        
        scrollable = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, pady=10)
        
        courses = [
            {
                "titre": "📘 Introduction à Python",
                "auteur": "Marie L.",
                "categorie": "Python",
                "likes": 45,
                "description": "Guide complet pour débuter en Python avec exercices",
                "type": "PDF",
                "date": "2025-10-15"
            },
            {
                "titre": "🎥 Tutorial React Hooks",
                "auteur": "Thomas K.",
                "categorie": "React",
                "likes": 67,
                "description": "Vidéos expliquant les hooks React en détail",
                "type": "Vidéo",
                "date": "2025-10-18"
            },
            {
                "titre": "📝 Fiche SQL - Les Jointures",
                "auteur": "Sarah M.",
                "categorie": "Bases de données",
                "likes": 89,
                "description": "Fiche récap sur les différents types de jointures SQL",
                "type": "Fiche",
                "date": "2025-10-20"
            },
            {
                "titre": "💻 Projet Node.js + Express",
                "auteur": "Lucas P.",
                "categorie": "Node.js",
                "likes": 34,
                "description": "Exemple de projet API REST avec Node.js",
                "type": "Code",
                "date": "2025-10-22"
            },
        ]
        
        for course in courses:
            card = ctk.CTkFrame(scrollable, corner_radius=15, fg_color=("#f0f0f0", "#1a1a1a"))
            card.pack(fill="x", pady=10, padx=5)
            
            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=20, pady=15)
            
            ctk.CTkLabel(
                header,
                text=course['titre'],
                font=ctk.CTkFont(size=20, weight="bold")
            ).pack(side="left")
            
            type_colors = {"PDF": "#e53e3e", "Vidéo": "#9f7aea", "Fiche": "#48bb78", "Code": "#4a9eff"}
            ctk.CTkLabel(
                header,
                text=course['type'],
                fg_color=type_colors.get(course['type'], "gray"),
                corner_radius=8,
                text_color="white",
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(side="right", padx=5, pady=5)
            
            ctk.CTkLabel(
                card,
                text=course['description'],
                font=ctk.CTkFont(size=14),
                text_color=("gray40", "gray70")
            ).pack(anchor="w", padx=20, pady=5)
            
            footer = ctk.CTkFrame(card, fg_color="transparent")
            footer.pack(fill="x", padx=20, pady=15)
            
            ctk.CTkLabel(
                footer,
                text=f"👤 {course['auteur']} • 📅 {course['date']}",
                font=ctk.CTkFont(size=12),
                text_color=("gray50", "gray60")
            ).pack(side="left")
            
            like_btn = ctk.CTkButton(
                footer,
                text=f"❤️ {course['likes']}",
                width=100,
                height=35,
                fg_color="#e53e3e",
                hover_color="#c53030",
                command=lambda c=course: self.like_course(c)
            )
            like_btn.pack(side="right", padx=5)
    
    def add_course(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Partager une ressource")
        dialog.geometry("500x600")
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="📚 Nouvelle Ressource", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        title_entry = ctk.CTkEntry(dialog, placeholder_text="Titre de la ressource", width=400, height=45)
        title_entry.pack(pady=10)
        
        desc_entry = ctk.CTkTextbox(dialog, width=400, height=100)
        desc_entry.insert("1.0", "Description...")
        desc_entry.pack(pady=10)
        
        type_menu = ctk.CTkOptionMenu(dialog, values=["PDF", "Vidéo", "Fiche", "Code"], width=400)
        type_menu.pack(pady=10)
        
        cat_menu = ctk.CTkOptionMenu(
            dialog,
            values=["Python", "JavaScript", "React", "Node.js", "Bases de données"],
            width=400
        )
        cat_menu.pack(pady=10)
        
        ctk.CTkButton(
            dialog,
            text="✨ Partager",
            command=lambda: [
                messagebox.showinfo("Succès", "Ressource partagée ! +20 XP"),
                self.current_user.__setitem__('xp', self.current_user['xp'] + 20),
                self.save_user_data(),
                dialog.destroy()
            ],
            width=400,
            height=50,
            fg_color="#48bb78",
            hover_color="#38a169",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=30)
    
    def like_course(self, course):
        course['likes'] += 1
        self.current_user['xp'] += 2
        self.save_user_data()
        self.show_courses()
    
    def show_tutoring(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="👥 Plateforme de Tutorat", font=ctk.CTkFont(size=36, weight="bold"))
        title.pack(pady=(0, 20), anchor="w")
        
        tabs = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        tabs.pack(fill="x", pady=10)
        
        ctk.CTkButton(
            tabs,
            text="🎓 Devenir Tuteur",
            command=self.show_become_tutor,
            width=200,
            height=45,
            fg_color="#9f7aea",
            hover_color="#805ad5"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            tabs,
            text="🔍 Trouver un Tuteur",
            command=self.show_find_tutor,
            width=200,
            height=45,
            fg_color="#48bb78",
            hover_color="#38a169"
        ).pack(side="left", padx=5)
        
        self.tutoring_content = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.tutoring_content.pack(fill="both", expand=True, pady=10)
        
        self.show_find_tutor()
    
    def show_find_tutor(self):
        for widget in self.tutoring_content.winfo_children():
            widget.destroy()
        
        scrollable = ctk.CTkScrollableFrame(self.tutoring_content, fg_color="transparent")
        scrollable.pack(fill="both", expand=True)
        
        tutors = [
            {
                "nom": "Marie Laurent",
                "specialites": ["Python", "Django", "Algorithmes"],
                "niveau": "Expert",
                "rating": 4.9,
                "sessions": 127,
                "disponibilite": "Lun-Ven 14h-18h"
            },
            {
                "nom": "Thomas Kowalski",
                "specialites": ["React", "JavaScript", "HTML/CSS"],
                "niveau": "Avancé",
                "rating": 4.8,
                "sessions": 89,
                "disponibilite": "Mar-Jeu 16h-20h"
            },
            {
                "nom": "Sarah Martin",
                "specialites": ["SQL", "MongoDB", "Bases de données"],
                "niveau": "Expert",
                "rating": 5.0,
                "sessions": 156,
                "disponibilite": "Lun-Sam 10h-17h"
            },
        ]
        
        for tutor in tutors:
            card = ctk.CTkFrame(scrollable, corner_radius=15, fg_color=("#f0f0f0", "#1a1a1a"))
            card.pack(fill="x", pady=10, padx=5)
            
            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=20, pady=15)
            
            left_section = ctk.CTkFrame(header, fg_color="transparent")
            left_section.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(
                left_section,
                text=f"👤 {tutor['nom']}",
                font=ctk.CTkFont(size=20, weight="bold")
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                left_section,
                text=f"⭐ {tutor['rating']}/5 • {tutor['sessions']} sessions",
                font=ctk.CTkFont(size=12),
                text_color=("gray50", "gray60")
            ).pack(anchor="w", pady=2)
            
            level_colors = {"Expert": "#e53e3e", "Avancé": "#f6ad55", "Intermédiaire": "#48bb78"}
            ctk.CTkLabel(
                header,
                text=tutor['niveau'],
                fg_color=level_colors.get(tutor['niveau'], "gray"),
                corner_radius=8,
                text_color="white",
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(side="right", padx=5, pady=5)
            
            specs_frame = ctk.CTkFrame(card, fg_color="transparent")
            specs_frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(
                specs_frame,
                text="📚 Spécialités: " + ", ".join(tutor['specialites']),
                font=ctk.CTkFont(size=14),
                text_color=("gray40", "gray70")
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                specs_frame,
                text=f"🕐 {tutor['disponibilite']}",
                font=ctk.CTkFont(size=13),
                text_color=("gray50", "gray60")
            ).pack(anchor="w", pady=5)
            
            ctk.CTkButton(
                card,
                text="📅 Réserver une session",
                command=lambda t=tutor: self.book_session(t),
                height=40,
                fg_color="#4a9eff",
                hover_color="#3182ce"
            ).pack(pady=15, padx=20, fill="x")
    
    def show_become_tutor(self):
        for widget in self.tutoring_content.winfo_children():
            widget.destroy()
        
        form_frame = ctk.CTkFrame(self.tutoring_content, corner_radius=15)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            form_frame,
            text="🎓 Devenir Tuteur",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=30)
        
        ctk.CTkLabel(
            form_frame,
            text="Partagez vos connaissances et gagnez de l'XP !",
            font=ctk.CTkFont(size=16),
            text_color=("gray50", "gray70")
        ).pack(pady=10)
        
        specs_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Vos spécialités (ex: Python, React, SQL)",
            width=500,
            height=45
        )
        specs_entry.pack(pady=15)
        
        level_menu = ctk.CTkOptionMenu(
            form_frame,
            values=["Intermédiaire", "Avancé", "Expert"],
            width=500
        )
        level_menu.pack(pady=15)
        
        dispo_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Disponibilités (ex: Lun-Ven 14h-18h)",
            width=500,
            height=45
        )
        dispo_entry.pack(pady=15)
        
        ctk.CTkButton(
            form_frame,
            text="✨ S'inscrire comme tuteur",
            command=lambda: [
                messagebox.showinfo("Succès", "Candidature envoyée ! +50 XP"),
                self.current_user.__setitem__('xp', self.current_user['xp'] + 50),
                self.save_user_data()
            ],
            width=500,
            height=50,
            fg_color="#9f7aea",
            hover_color="#805ad5",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=30)
    
    def book_session(self, tutor):
        messagebox.showinfo("Succès", f"Session réservée avec {tutor['nom']} !")
        self.current_user['xp'] += 15
        self.save_user_data()
    
    def show_deals(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="🗺️ Carte des Bons Plans", font=ctk.CTkFont(size=36, weight="bold"))
        title.pack(pady=(0, 20), anchor="w")
        
        scrollable = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, pady=10)
        
        deals = [
            {"nom": "🍕 Pizza Roma", "reduction": "-20%", "description": "Pizza + boisson", "adresse": "Marseille", "likes": 234},
            {"nom": "☕ Starbucks", "reduction": "-15%", "description": "Café étudiant", "adresse": "Vieux-Port", "likes": 189},
        ]
        
        for deal in deals:
            card = ctk.CTkFrame(scrollable, corner_radius=15, fg_color=("#f0f0f0", "#1a1a1a"))
            card.pack(fill="x", pady=10, padx=5)
            ctk.CTkLabel(card, text=deal['nom'], font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15, padx=20, anchor="w")
            ctk.CTkLabel(card, text=deal['description'], font=ctk.CTkFont(size=14)).pack(pady=5, padx=20, anchor="w")
    
    def show_career(self):
        self.clear_content()
        title = ctk.CTkLabel(self.content_frame, text="💼 Coach Carrière", font=ctk.CTkFont(size=36, weight="bold"))
        title.pack(pady=(0, 20), anchor="w")
        
        stats_frame = ctk.CTkFrame(self.content_frame, corner_radius=15)
        stats_frame.pack(fill="x", pady=20, padx=10)
        
        ctk.CTkLabel(stats_frame, text="📊 Analyse de Profil", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        progress_items = [
            ("Profil complété", 75, "#48bb78"),
            ("CV à jour", 90, "#4a9eff"),
        ]
        
        for label, value, color in progress_items:
            ctk.CTkLabel(stats_frame, text=f"{label}: {value}%", font=ctk.CTkFont(size=14)).pack(pady=10, padx=30, anchor="w")
    
    def save_user_data(self):
        try:
            with open("plateforme_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    data = {"users": []}
        except:
            data = {"users": []}
        
        user_found = False
        for i, user in enumerate(data.get("users", [])):
            if isinstance(user, dict) and user.get("email") == self.current_user.get("email"):
                data["users"][i] = self.current_user
                user_found = True
                break
        
        if not user_found:
            if "users" not in data:
                data["users"] = []
            data["users"].append(self.current_user)
        
        with open("plateforme_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    app = PlateformeXPApp()
    app.mainloop()
