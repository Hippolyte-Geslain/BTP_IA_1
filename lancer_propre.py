#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur propre - Force le rechargement complet
"""

import os
import sys
import shutil
import subprocess
import time

# Obtenir le répertoire du script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("=" * 50)
print("   NETTOYAGE ET LANCEMENT")
print("=" * 50)

# 1. Supprimer __pycache__
print("\n[1/3] Suppression du cache Python...")
pycache_dir = os.path.join(script_dir, "__pycache__")
if os.path.exists(pycache_dir):
    shutil.rmtree(pycache_dir)
    print("✓ Cache supprimé")
else:
    print("✓ Pas de cache trouvé")

# 2. Supprimer les fichiers .pyc
print("\n[2/3] Suppression des fichiers .pyc...")
count = 0
for root, dirs, files in os.walk(script_dir):
    for file in files:
        if file.endswith('.pyc'):
            os.remove(os.path.join(root, file))
            count += 1
print(f"✓ {count} fichiers .pyc supprimés")

# 3. Lancer l'application
print("\n[3/3] Lancement de l'application...")
print("=" * 50)
print()

# Importer et lancer
import tkinter as tk
from importlib import reload
import app_gui

# Forcer le rechargement du module
reload(app_gui)

# Créer et lancer l'interface
root = tk.Tk()
app = app_gui.PlateformeXPGUI(root)
root.mainloop()
