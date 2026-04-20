# ImmoFacile 🏠
Plateforme de location immobilière Django — Sénégal / Afrique de l'Ouest

---

## ⚡ Installation complète (Windows)

Ouvrez un terminal (cmd ou PowerShell) dans le dossier `immofacile/` et exécutez
les commandes dans l'ordre.

### 1. Environnement virtuel
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Dépendances
```bash
pip install -r requirements.txt
```

### 3. Migrations (base de données)
```bash
python manage.py makemigrations accounts
python manage.py makemigrations listings
python manage.py makemigrations agencies
python manage.py makemigrations messaging
python manage.py makemigrations core
python manage.py migrate
```

### 4. Compte administrateur
```bash
python manage.py createsuperuser
```
Choisissez un nom d'utilisateur, email et mot de passe.

### 5. Données de démonstration (optionnel mais recommandé)
```bash
python manage.py seed_demo
```
Crée 14 annonces géolocalisées à Dakar + 2 comptes :
- `demo_proprio` / `Demo@1234` (propriétaire)
- `dakar_immo_pro` / `Demo@1234` (agence)

### 6. Lancer le serveur
```bash
python manage.py runserver
```

Ouvrir dans le navigateur : **http://127.0.0.1:8000**

---

## 🔗 Pages principales

| URL                          | Description                     |
|------------------------------|---------------------------------|
| `/`                          | Accueil + recherche             |
| `/carte/`                    | Carte interactive Leaflet       |
| `/annonces/<id>/`            | Détail d'une annonce            |
| `/annonces/publier/`         | Publier une annonce             |
| `/mes-annonces/`             | Mes annonces                    |
| `/favoris/`                  | Mes favoris                     |
| `/accounts/inscription/`     | Créer un compte                 |
| `/accounts/connexion/`       | Se connecter                    |
| `/accounts/profil/`          | Mon profil                      |
| `/agences/`                  | Liste des agences               |
| `/messages/`                 | Boîte de réception              |
| `/admin/`                    | Interface d'administration      |

---

## 📁 Structure du projet

```
immofacile/
├── manage.py
├── requirements.txt
├── db.sqlite3              ← créé automatiquement après migrate
├── logs/                   ← logs automatiques (app, errors, requests, security)
├── media/                  ← photos uploadées
├── static/                 ← fichiers statiques
│
├── immofacile/             ← configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                   ← middleware de logs + context processors
│   ├── middleware.py
│   └── context_processors.py
│
├── accounts/               ← utilisateurs (locataire / proprio / agence)
├── listings/               ← annonces immobilières
├── agencies/               ← profils agences et avis
├── messaging/              ← messagerie et demandes de visite
│
└── templates/              ← 18 templates HTML
    ├── base.html
    ├── listings/
    ├── accounts/
    ├── agencies/
    └── messaging/
```

---

## 👤 Rôles utilisateurs

| Rôle         | Peut faire                                       |
|--------------|--------------------------------------------------|
| Locataire    | Rechercher, contacter, demander des visites      |
| Propriétaire | Publier des annonces, gérer les demandes         |
| Agence       | Publier des annonces (vérification par admin)    |

---

## 📋 Logs générés automatiquement

Les logs sont dans le dossier `logs/` :

| Fichier          | Contenu                         | Rétention |
|------------------|---------------------------------|-----------|
| `app.log`        | Activité générale               | 30 jours  |
| `errors.log`     | Erreurs uniquement              | 60 jours  |
| `requests.log`   | Chaque requête HTTP             | 14 jours  |
| `security.log`   | 403, tentatives suspectes       | 90 jours  |

---

## 🗺 Carte interactive

La carte Leaflet utilise **OpenStreetMap** — gratuit, sans clé API.

Pour ajouter des coordonnées à une annonce :
1. Aller sur `/admin/` → Annonces → modifier une annonce
2. Remplir les champs **Latitude** et **Longitude**
3. Ou utiliser le bouton "Localiser automatiquement" dans le formulaire de publication

---

## ⚙️ Variables d'environnement (optionnel)

Créez un fichier `.env` à la racine pour personnaliser :

```env
SECRET_KEY=votre-cle-secrete-longue-et-aleatoire
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL (production)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=immofacile_db
DB_USER=postgres
DB_PASSWORD=motdepasse
DB_HOST=localhost
DB_PORT=5432

# Email (production)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=votre@gmail.com
EMAIL_HOST_PASSWORD=mot-de-passe-app
```

---

## 🚀 Commandes utiles

```bash
# Voir les logs en temps réel
type logs\requests.log

# Créer un superutilisateur supplémentaire
python manage.py createsuperuser

# Collecter les fichiers statiques (production)
python manage.py collectstatic

# Shell Django interactif
python manage.py shell

# Réinitialiser la base de données
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
```
