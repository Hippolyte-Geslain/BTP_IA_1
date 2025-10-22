#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration automatique de Plateforme XP
Ce script illustre toutes les fonctionnalités du prototype
"""

import time
import sys

# Import du module principal
from test import PlateformeXP, User, print_banner


def print_step(step_number: int, title: str):
    """Affiche un titre d'étape avec style"""
    print("\n" + "="*70)
    print(f"📍 ÉTAPE {step_number}: {title}")
    print("="*70)
    time.sleep(1)


def wait_user():
    """Attend que l'utilisateur appuie sur Entrée"""
    input("\n⏸️  Appuyez sur Entrée pour continuer...")


def demo():
    """Exécute la démonstration complète"""
    
    print_banner()
    print("🎬 DÉMONSTRATION AUTOMATIQUE DE PLATEFORME XP")
    print("Cette démo va créer plusieurs utilisateurs et simuler leurs interactions")
    wait_user()
    
    # Initialiser l'application
    app = PlateformeXP()
    
    # ===== ÉTAPE 1: Création de Comptes =====
    print_step(1, "Création de 3 utilisateurs")
    
    alice = app.register_user("Alice Dupont", "alice@laplateforme.io")
    time.sleep(0.5)
    
    bob = app.register_user("Bob Martin", "bob@laplateforme.io")
    time.sleep(0.5)
    
    charlie = app.register_user("Charlie Bernard", "charlie@laplateforme.io")
    
    print(f"\n✅ 3 utilisateurs créés:")
    print(f"   - Alice (ID: {alice.user_id})")
    print(f"   - Bob (ID: {bob.user_id})")
    print(f"   - Charlie (ID: {charlie.user_id})")
    wait_user()
    
    # ===== ÉTAPE 2: Alice complète des projets =====
    print_step(2, "Alice complète plusieurs projets")
    
    app.login(alice.user_id)
    app.list_projects()
    
    print("\n🎯 Alice complète 3 projets...")
    time.sleep(1)
    
    app.complete_project(1)  # Easy - 50 XP
    time.sleep(0.5)
    
    app.complete_project(2)  # Medium - 100 XP
    time.sleep(0.5)
    
    app.complete_project(5)  # Medium - 120 XP
    
    print(f"\n📊 Alice a maintenant {alice.xp} XP et est niveau {alice.level}")
    app.view_profile()
    wait_user()
    
    # ===== ÉTAPE 3: Bob complète un projet et aide Alice =====
    print_step(3, "Bob complète un projet et aide Alice")
    
    app.login(bob.user_id)
    
    print("\n🎯 Bob complète un projet Hard...")
    app.complete_project(3)  # Hard - 200 XP
    time.sleep(1)
    
    print("\n🤝 Bob aide Alice...")
    app.help_student(alice.user_id)
    
    print(f"\n📊 Bob a maintenant {bob.xp} XP et est niveau {bob.level}")
    app.view_profile()
    wait_user()
    
    # ===== ÉTAPE 4: Chat Anonyme =====
    print_step(4, "Interactions sur le chat anonyme")
    
    print("\n💬 Alice pose une question anonyme...")
    app.login(alice.user_id)
    app.post_anonymous_message("Comment déployer une application Flask sur Heroku ?")
    time.sleep(0.5)
    
    print("\n💬 Bob pose aussi une question...")
    app.login(bob.user_id)
    app.post_anonymous_message("Des conseils pour optimiser mes requêtes SQL ?")
    time.sleep(0.5)
    
    print("\n💬 Charlie participe...")
    app.login(charlie.user_id)
    app.post_anonymous_message("Quelqu'un pour m'expliquer les décorateurs Python ?")
    
    print("\n📖 Consultation du chat:")
    app.view_chat()
    wait_user()
    
    # ===== ÉTAPE 5: Charlie rattrape son retard =====
    print_step(5, "Charlie complète plusieurs projets rapidement")
    
    app.login(charlie.user_id)
    
    print("\n🚀 Charlie est motivé et complète 4 projets !")
    app.complete_project(1)  # 50 XP
    time.sleep(0.3)
    app.complete_project(2)  # 100 XP
    time.sleep(0.3)
    app.complete_project(3)  # 200 XP
    time.sleep(0.3)
    app.complete_project(4)  # 250 XP
    
    print(f"\n🌟 Charlie a fait un bond incroyable !")
    print(f"   XP: {charlie.xp} | Niveau: {charlie.level}")
    app.view_profile()
    wait_user()
    
    # ===== ÉTAPE 6: Classement Final =====
    print_step(6, "Classement général des étudiants")
    
    app.view_leaderboard()
    wait_user()
    
    # ===== ÉTAPE 7: Événements =====
    print_step(7, "Consultation des événements à venir")
    
    app.list_events()
    wait_user()
    
    # ===== ÉTAPE 8: Génération de Badges =====
    print_step(8, "Génération des badges QR Code")
    
    print("\n📱 Génération du badge QR pour Alice...")
    app.login(alice.user_id)
    app.generate_qr_badge()
    time.sleep(0.5)
    
    print("\n📱 Génération du badge QR pour Bob...")
    app.login(bob.user_id)
    app.generate_qr_badge()
    time.sleep(0.5)
    
    print("\n📱 Génération du badge QR pour Charlie...")
    app.login(charlie.user_id)
    app.generate_qr_badge()
    
    print("\n✅ 3 badges QR Code générés avec succès !")
    print("   Les fichiers badge_*.png contiennent les QR codes")
    wait_user()
    
    # ===== ÉTAPE 9: Statistiques Finales =====
    print_step(9, "Statistiques et bilan")
    
    print("\n📊 BILAN DE LA DÉMONSTRATION")
    print("="*70)
    
    all_users = [alice, bob, charlie]
    total_xp = sum(u.xp for u in all_users)
    total_projects = sum(len(u.projects_completed) for u in all_users)
    total_badges = sum(len(u.badges) for u in all_users)
    
    print(f"\n👥 Utilisateurs créés: {len(all_users)}")
    print(f"✨ XP total gagné: {total_xp}")
    print(f"📚 Projets complétés: {total_projects}")
    print(f"🏆 Badges débloqués: {total_badges}")
    print(f"💬 Messages postés: {len(app.chat_messages)}")
    print(f"📅 Événements disponibles: {len(app.events)}")
    
    print("\n🏆 PODIUM FINAL:")
    sorted_users = sorted(all_users, key=lambda u: u.xp, reverse=True)
    for i, user in enumerate(sorted_users, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        print(f"{medal} {user.name}: Niveau {user.level} - {user.xp} XP")
        print(f"   Badges: {', '.join(user.badges) if user.badges else 'Aucun'}")
    
    # ===== ÉTAPE 10: Sauvegarde =====
    print_step(10, "Sauvegarde des données")
    
    app.save_data()
    print("\n✅ Toutes les données ont été sauvegardées dans plateforme_data.json")
    print("   Vous pouvez maintenant lancer test.py et vous connecter avec:")
    print(f"   - Alice (ID: {alice.user_id})")
    print(f"   - Bob (ID: {bob.user_id})")
    print(f"   - Charlie (ID: {charlie.user_id})")
    
    # ===== FIN =====
    print("\n" + "="*70)
    print("🎉 DÉMONSTRATION TERMINÉE !")
    print("="*70)
    print("\n🎮 Fonctionnalités démontrées:")
    print("   ✅ Création de comptes utilisateurs")
    print("   ✅ Système XP et progression de niveaux")
    print("   ✅ Complétion de projets avec récompenses")
    print("   ✅ Système d'entraide entre étudiants")
    print("   ✅ Chat anonyme d'entraide")
    print("   ✅ Déblocage de badges")
    print("   ✅ Classement/Leaderboard")
    print("   ✅ Liste d'événements")
    print("   ✅ Génération de badges QR Code")
    print("   ✅ Sauvegarde/Chargement de données")
    
    print("\n📝 Prochaines étapes suggérées:")
    print("   1. Lancez 'python test.py' pour tester l'interface interactive")
    print("   2. Connectez-vous avec l'un des utilisateurs créés")
    print("   3. Explorez toutes les fonctionnalités du menu")
    print("   4. Consultez le fichier plateforme_data.json pour voir les données")
    print("   5. Scannez les badges QR générés (badge_*.png)")
    
    print("\n🚀 Versions futures prévues:")
    print("   • Interface web (Flask/Django)")
    print("   • Application mobile")
    print("   • Système de tutorat")
    print("   • Carte des bons plans")
    print("   • Coach carrière avec IA")
    print("   • Tournois et compétitions")
    
    print("\n💻 Happy Coding @ La Plateforme_ !")
    print("="*70 + "\n")


def demo_rapide():
    """Version rapide de la démo sans attentes"""
    print_banner()
    print("🚀 DÉMONSTRATION RAPIDE\n")
    
    app = PlateformeXP()
    
    # Créer utilisateurs
    u1 = app.register_user("Alice", "alice@test.io")
    u2 = app.register_user("Bob", "bob@test.io")
    
    # Alice fait des projets
    app.login(u1.user_id)
    app.complete_project(1)
    app.complete_project(2)
    
    # Bob aussi
    app.login(u2.user_id)
    app.complete_project(3)
    app.help_student(u1.user_id)
    
    # Chat
    app.post_anonymous_message("Question test 1")
    app.login(u1.user_id)
    app.post_anonymous_message("Question test 2")
    
    # Affichages
    app.view_leaderboard()
    app.view_chat()
    
    # Sauvegarder
    app.save_data()
    
    print("\n✅ Démo rapide terminée !")


if __name__ == "__main__":
    print("\n🎬 DÉMO PLATEFORME XP")
    print("="*70)
    print("Choisissez un mode:")
    print("1. 🎥 Démonstration complète (avec explications)")
    print("2. ⚡ Démonstration rapide (automatique)")
    print("="*70)
    
    choice = input("\n➤ Votre choix (1 ou 2): ").strip()
    
    if choice == "1":
        demo()
    elif choice == "2":
        demo_rapide()
    else:
        print("❌ Choix invalide")
        sys.exit(1)
