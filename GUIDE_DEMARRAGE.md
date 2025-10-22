# 🚀 Guide de Démarrage Rapide - Plateforme XP

## ⚡ Installation en 3 étapes

### 1️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2️⃣ Lancer l'application
```bash
python test.py
```

### 3️⃣ Créer votre compte
- Choisissez l'option `1` dans le menu
- Entrez votre nom et email
- Notez votre ID utilisateur !

## 🎮 Scénario de Démonstration

### Scénario 1 : Premier Jour d'un Étudiant

1. **Créer un compte**
   ```
   Menu > 1
   Nom: Alice Dupont
   Email: alice@laplateforme.io
   ```

2. **Se connecter**
   ```
   Menu > 2
   ID: 1
   ```

3. **Voir mon profil**
   ```
   Menu > 3
   → Niveau 1, 0 XP
   ```

4. **Consulter les projets**
   ```
   Menu > 4
   → Liste des 5 projets disponibles
   ```

5. **Compléter un projet facile**
   ```
   Menu > 5
   ID du projet: 1 (Site Web Portfolio)
   → +50 XP ! Niveau 1 → Progression
   → Badge "Premier Projet" débloqué !
   ```

6. **Aider un autre étudiant**
   ```
   Menu > 6
   ID de l'étudiant: 2
   → +30 XP pour l'entraide
   → Badge "Mentor" débloqué !
   ```

7. **Poster sur le chat anonyme**
   ```
   Menu > 7 > 2
   Message: "Comment déployer une app Flask ?"
   → Message posté anonymement
   ```

8. **Voir le classement**
   ```
   Menu > 9
   → Position dans le leaderboard
   ```

9. **Générer mon badge QR**
   ```
   Menu > 10
   → Fichier badge_1.png créé
   → À scanner pour accéder à l'école
   ```

### Scénario 2 : Montée de Niveau

1. **Compléter plusieurs projets**
   ```
   Projet 1 (Easy): +50 XP
   Projet 2 (Medium): +100 XP
   Projet 3 (Hard): +200 XP
   → Total: 350 XP
   → Niveau 2 atteint ! 🎉
   ```

2. **Débloquer tous les badges**
   - 🏆 Premier Projet (automatique)
   - 🎓 Mentor (aider un étudiant)
   - Plus de badges à venir...

### Scénario 3 : Événements & Social

1. **Consulter les événements**
   ```
   Menu > 8
   → Soirée Gaming BDE (15/11)
   → Workshop IA (20/11)
   → Hackathon 48h (01/12)
   ```

2. **Lire le chat d'entraide**
   ```
   Menu > 7 > 1
   → Voir les 10 derniers messages
   ```

## 📊 Comprendre le Système XP

### Calcul du Niveau
```
Niveau = √(XP / 100) + 1

Exemples:
- 0-99 XP → Niveau 1
- 100-399 XP → Niveau 2
- 400-899 XP → Niveau 3
- 900-1599 XP → Niveau 4
```

### XP par Activité
| Activité | XP |
|----------|-----|
| Projet Easy | 50 |
| Projet Medium | 100-120 |
| Projet Hard | 200-250 |
| Aide apportée | 30 |
| Participation événement | 20-100 |

## 🎯 Objectifs Progressifs

### Débutant (Niveau 1-2)
- ✅ Créer son compte
- ✅ Compléter 1 projet facile
- ✅ Poster 1 message anonyme
- ✅ Générer son badge QR

### Intermédiaire (Niveau 3-5)
- ✅ Compléter 5 projets
- ✅ Aider 3 étudiants
- ✅ Participer à 2 événements
- ✅ Débloquer tous les badges

### Avancé (Niveau 6+)
- ✅ Atteindre le top 3 du classement
- ✅ Compléter tous les projets Hard
- ✅ Devenir mentor actif (10+ aides)
- ✅ Participer à tous les événements

## 🐛 Résolution de Problèmes

### L'application ne démarre pas
```bash
# Vérifier la version Python
python --version
# Doit être 3.8+

# Réinstaller les dépendances
pip install --upgrade -r requirements.txt
```

### Erreur "Module not found: qrcode"
```bash
pip install qrcode pillow
```

### Données perdues
- Les données sont sauvegardées dans `plateforme_data.json`
- Utilisez l'option 11 pour sauvegarder manuellement
- Sauvegarde automatique à la fermeture

### Badge QR non généré
- Vérifiez que Pillow est installé: `pip install Pillow`
- Le fichier est créé dans le dossier courant
- Nom du fichier: `badge_{votre_id}.png`

## 💡 Astuces & Tips

### Maximiser son XP
1. Commencez par les projets Easy pour débloquer le badge
2. Aidez régulièrement les autres (+30 XP à chaque fois)
3. Participez aux événements BDE
4. Complétez les projets Hard pour les gros gains d'XP

### Utiliser le Chat Efficacement
- Posez des questions précises
- Utilisez l'anonymat pour les questions "sensibles"
- Aidez les autres pour gagner de l'XP

### Progression Optimale
```
Semaine 1: Projets Easy → Niveau 2
Semaine 2: Projets Medium + Entraide → Niveau 3
Semaine 3: Projets Hard → Niveau 4
Mois 1: Top 10 du classement
```

## 🎨 Personnalisation Future

Le prototype actuel est en CLI (ligne de commande). Les versions futures incluront :

- 🎨 Interface web moderne
- 📱 Application mobile
- 🌈 Thèmes personnalisables
- 🖼️ Avatars et skins
- 🏰 Guildes et équipes

## 📞 Support

Des questions ? Des bugs ?
- Ouvrez une issue sur GitHub
- Contactez l'équipe de développement
- Consultez la documentation complète dans README.md

---

**🎮 Bon jeu et bon apprentissage !**

*Transformez votre formation en aventure épique !*
