# 🔧 INDEX DES SCRIPTS BAT

Derniere mise a jour: 30/10/2025 13:24:39,38

## 📂 Structure

### Startup Scripts (scripts\startup\)
Scripts de demarrage des services

- **START_ALL.bat** - Demarre tous les services (backend + frontend)
- **START_BACKEND.bat** - Demarre uniquement le backend
- **START_WEB.bat** - Demarre uniquement le frontend web

### Maintenance Scripts (scripts\maintenance\)
Scripts de maintenance et nettoyage

- **NETTOYER_ET_RELANCER.bat** - Nettoie et relance les services
- **KILL_PORTS.bat** - Tue les processus sur les ports utilises

### Utilities Scripts (scripts\utilities\)
Scripts utilitaires divers

- **REORGANIZE_DOCS.bat** - Reorganise les fichiers de documentation

### Archive (scripts\archive\)
Scripts obsoletes ou remplaces

## 🚀 Utilisation Rapide

### Demarrage Normal
```batch
scripts\startup\START_ALL.bat
```

### Demarrage Selectif
```batch
REM Backend seulement
scripts\startup\START_BACKEND.bat

REM Frontend seulement
scripts\startup\START_WEB.bat
```

### Maintenance
```batch
REM Nettoyage complet et redemarrage
scripts\maintenance\NETTOYER_ET_RELANCER.bat

REM Liberer les ports
scripts\maintenance\KILL_PORTS.bat
```

### Utilitaires
```batch
REM Reorganiser la documentation
scripts\utilities\REORGANIZE_DOCS.bat
```

## ⚠️ Notes

- Tous les scripts doivent etre executes depuis la racine du projet
- Les scripts de startup ouvrent de nouvelles fenetres de terminal
- Les scripts de maintenance peuvent necessiter des privileges administrateur

