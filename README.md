# 🏪 Boutique Exclusive - Version Pro

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.0+-green.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Une application de boutique RPG moderne avec interface graphique, développée en Python avec CustomTkinter. Gérez votre inventaire, combattez des ennemis, complétez des quêtes et faites fortune !

![Screenshot](https://via.placeholder.com/800x400/2b2b2b/ffffff?text=Boutique+Exclusive)

## 🌟 Fonctionnalités

### 🛍️ **Système de Boutique**
- Catalogue d'articles avec système de rareté (Commun à Mythique)
- Interface colorée selon la rareté des objets
- Historique complet des achats et ventes
- Ajout d'articles personnalisés

### 🏦 **Système Bancaire**
- Dépôt et retrait d'écus
- Système de prêts avec intérêts
- Gestion sécurisée des fonds
- Suivi des transactions

### ⚔️ **Système de Combat**
- Arène avec différents ennemis
- Statistiques basées sur l'équipement
- Récompenses en écus et expérience
- Progression par niveaux

### 🎯 **Système de Quêtes**
- 5 quêtes automatiques différentes
- Récompenses généreuses
- Suivi de progression en temps réel
- Nouveaux défis réguliers

### 📊 **Statistiques Avancées**
- Tableau de bord complet
- Historique détaillé
- Analyses de performance
- Progression du joueur

### 📈 **Marché Dynamique**
- Taux de change en temps réel
- Simulation de fluctuations
- Opportunités d'investissement
- Interface de trading

## 🚀 Installation

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation Rapide

1. **Cloner le projet**
```bash
git clone https://github.com/votre-username/boutique-exclusive.git
cd boutique-exclusive
```

2. **Installer les dépendances**
```bash
pip install customtkinter
```

3. **Lancer l'application**
```bash
python boutique_shop.py
```

### Installation Alternative (avec environnement virtuel)

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Installer les dépendances
pip install customtkinter

# Lancer l'application
python boutique_shop.py
```

## 🎮 Guide d'Utilisation

### Premier Démarrage
1. L'application démarre avec **1000 écus** pour commencer
2. Explorez les différents onglets pour découvrir les fonctionnalités
3. Vos données sont automatiquement sauvegardées dans `boutique_data.json`

### Navigation
- **🏪 Boutique** : Acheter des articles
- **💰 Banque** : Gérer vos finances
- **🎒 Inventaire** : Consulter vos possessions
- **💼 Vendre** : Revendre vos articles
- **📊 Statistiques** : Analyser vos performances
- **🎯 Quêtes** : Missions à accomplir
- **📈 Marché** : Taux de change
- **⚔️ Combat** : Combattre des ennemis

### Système de Progression

#### Niveaux et Expérience
- Gagnez de l'**expérience (XP)** en achetant, vendant et combattant
- Montez de **niveau** tous les 100 XP
- Recevez des **bonus en écus** à chaque niveau (niveau × 50 écus)

#### Quêtes Disponibles
1. **Premier Achat** : Effectuez votre premier achat (+50 écus)
2. **Collectionneur** : Achetez 5 articles différents (+200 écus)
3. **Marchand** : Vendez 3 articles (+100 écus)
4. **Épargnant** : Économisez 1000 écus en banque (+150 écus)
5. **Aventurier Légendaire** : Atteignez le niveau 5 (+500 écus)

#### Système de Combat
- Vos **statistiques** dépendent de votre équipement
- Combattez des ennemis selon votre niveau
- Gagnez des **récompenses** en cas de victoire
- Perdez des écus en cas de défaite

### Astuces de Jeu

💡 **Conseils pour Débutants**
- Commencez par acheter des objets bon marché pour gagner de l'XP
- Utilisez la banque pour sécuriser vos écus
- Complétez les quêtes faciles en premier
- Équipez-vous avant de combattre

💎 **Stratégies Avancées**
- Diversifiez votre inventaire pour maximiser les statistiques
- Surveillez le marché pour les meilleures opportunités
- Équilibrez achats et ventes pour optimiser les profits
- Utilisez les prêts intelligemment pour investir

## 🛠️ Structure du Projet

```
boutique-exclusive/
│
├── shop.py          # Application principale
├── boutique_data.json        # Fichier de sauvegarde (généré automatiquement)
├── README.md                 # Ce fichier
├── LICENSE                   # Licence du projet
└── requirements.txt          # Dépendances Python
```

### Architecture du Code

```python
class BoutiqueShop:
    ├── __init__()              # Initialisation
    ├── setup_ui()              # Interface utilisateur
    ├── show_boutique()         # Page boutique
    ├── show_banque()           # Page banque
    ├── show_inventaire()       # Page inventaire
    ├── show_vendre()           # Page vente
    ├── show_statistiques()     # Page statistiques
    ├── show_quetes()           # Page quêtes
    ├── show_marche()           # Page marché
    ├── show_combat()           # Page combat
    ├── save_data()             # Sauvegarde
    └── load_data()             # Chargement

class NotificationSystem:
    ├── show_notification()     # Afficher notification
    └── close_notification()   # Fermer notification
```

## 📁 Fichiers de Données

### boutique_data.json
```json
{
  "ecus": 1000,
  "ecus_banque": 0,
  "experience": 0,
  "niveau": 1,
  "inventaire": [],
  "articles": [...],
  "historique_achats": [],
  "historique_ventes": [],
  "quetes": [...]
}
```

## 🎨 Personnalisation

### Ajouter de Nouveaux Articles
1. Utilisez le bouton **"➕ Ajouter"** dans l'interface
2. Ou modifiez directement le code dans `self.articles`

### Modifier les Quêtes
Éditez la méthode `init_quetes()` pour ajouter vos propres défis :

```python
{
    "nom": "Ma Quête",
    "description": "Description de la quête",
    "recompense": 100,
    "complete": False,
    "type": "achat",  # achat, vente, banque, niveau
    "objectif": 5
}
```

### Personnaliser l'Interface
- Modifiez `ctk.set_appearance_mode()` pour le thème (dark/light)
- Changez `ctk.set_default_color_theme()` pour les couleurs
- Ajustez les couleurs de rareté dans `create_article_widget()`

## 🐛 Dépannage

### Problèmes Courants

**L'application ne se lance pas**
```bash
# Vérifiez votre version de Python
python --version

# Réinstallez CustomTkinter
pip uninstall customtkinter
pip install customtkinter
```

**Erreur de sauvegarde**
- Vérifiez les permissions d'écriture dans le dossier
- Assurez-vous que le fichier `boutique_data.json` n'est pas ouvert ailleurs

**Interface déformée**
- Augmentez la taille de la fenêtre
- Vérifiez la résolution de votre écran
- Redémarrez l'application

### Logs et Debug
Ajoutez ces lignes pour le debug :
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment participer :

1. **Fork** le projet
2. Créez une **branche** pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. **Committez** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une **Pull Request**

### Idées de Contributions
- 🎨 Nouveaux thèmes visuels
- ⚔️ Nouveaux types d'ennemis
- 🎯 Système de quêtes étendu
- 📊 Graphiques de statistiques
- 🌐 Multijoueur local
- 💾 Système de profils multiples

## 🔄 Historique des Versions

### Version 2.0.0 - Version Pro (Actuelle)
- ✨ Système de combat complet
- 🎯 Quêtes automatiques
- 📈 Marché dynamique
- 🔔 Notifications personnalisées
- 📊 Statistiques avancées
- 🐛 Corrections de bugs majeurs

### Version 1.0.0 - Version Originale
- 🏪 Boutique de base
- 💰 Système bancaire simple
- 🎒 Inventaire basique
- 💼 Vente d'articles

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**Votre Nom**
- GitHub: [@votre-username](https://github.com/votre-username)
- Email: votre.email@example.com

## 🙏 Remerciements

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) pour l'interface moderne
- La communauté Python pour les outils fantastiques
- Tous les contributeurs du projet

## 📞 Support

Besoin d'aide ? Voici vos options :

1. 📖 Consultez ce README
2. 🐛 Ouvrez une [issue](https://github.com/votre-username/boutique-exclusive/issues)
3. 💬 Rejoignez notre [Discord](https://discord.gg/votre-serveur)
4. 📧 Contactez-nous par email

---

<div align="center">

**⭐ N'oubliez pas de donner une étoile si ce projet vous plaît ! ⭐**

[🏠 Retour au sommaire](#-boutique-exclusive---version-pro) | [📥 Télécharger](https://github.com/votre-username/boutique-exclusive/releases) | [🐛 Signaler un bug](https://github.com/votre-username/boutique-exclusive/issues)

</div>
