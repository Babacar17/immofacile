# 🚀 Guide de déploiement ImmoFacile

Ce guide couvre **4 plateformes** : Railway, Render, PythonAnywhere, VPS.
Lisez la section qui correspond à votre choix.

---

## ⚡ Étape 0 — Préparation locale (OBLIGATOIRE pour toutes les plateformes)

### 0.1 Installer Git
Téléchargez Git : https://git-scm.com/download/win
Vérifiez : `git --version`

### 0.2 Créer un compte GitHub
Allez sur https://github.com et créez un compte gratuit.

### 0.3 Initialiser Git dans votre projet
```bash
cd C:\pourtravailler\immofacile

git init
git add .
git commit -m "Initial commit — ImmoFacile"
```

### 0.4 Créer un dépôt GitHub et pousser
```bash
# Sur GitHub : cliquez "New repository", appelez-le "immofacile", laissez PUBLIC ou PRIVATE
# Puis dans votre terminal :

git remote add origin https://github.com/VOTRE_USERNAME/immofacile.git
git branch -M main
git push -u origin main
```

### 0.5 Générer une SECRET_KEY sécurisée
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copiez la clé affichée — vous en aurez besoin.

---

## 🚂 Option A — Railway (Recommandé — Gratuit au départ)

**Prix :** 5$/mois après le crédit gratuit de démarrage
**Avantage :** Déploiement automatique depuis GitHub, PostgreSQL inclus

### Étapes

**1. Créer un compte Railway**
→ https://railway.app — connectez-vous avec GitHub

**2. Créer un nouveau projet**
- Cliquez "New Project"
- Choisissez "Deploy from GitHub repo"
- Sélectionnez votre dépôt `immofacile`

**3. Ajouter PostgreSQL**
- Dans votre projet Railway, cliquez "+ New"
- Sélectionnez "Database" → "PostgreSQL"
- Railway crée automatiquement la base

**4. Configurer les variables d'environnement**
Dans Railway → votre service Web → onglet "Variables" :

```
DJANGO_SETTINGS_MODULE  = immofacile.settings_production
SECRET_KEY              = [votre clé générée à l'étape 0.5]
DEBUG                   = False
ALLOWED_HOSTS           = votre-app.up.railway.app
DB_ENGINE               = django.db.backends.postgresql
DB_NAME                 = ${{Postgres.PGDATABASE}}
DB_USER                 = ${{Postgres.PGUSER}}
DB_PASSWORD             = ${{Postgres.PGPASSWORD}}
DB_HOST                 = ${{Postgres.PGHOST}}
DB_PORT                 = ${{Postgres.PGPORT}}
DB_SSLMODE              = require
```

**5. Configurer le build**
Dans Railway → Settings → Deploy :
- Build Command :
  ```
  pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
  ```
- Start Command :
  ```
  gunicorn immofacile.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
  ```

**6. Redéployer**
Cliquez "Deploy" — Railway build et lance votre app.

**7. Créer le superuser**
Dans Railway → votre service → onglet "Shell" :
```bash
python manage.py createsuperuser
python manage.py seed_demo
```

**8. Ajouter votre domaine (optionnel)**
Railway → Settings → Networking → Custom Domain → entrez votre domaine.
Ajoutez ensuite le CNAME chez votre registrar DNS.

**Résultat :** Votre app tourne sur `https://votre-app.up.railway.app` ✅

---

## 🎨 Option B — Render (Gratuit avec limitations)

**Prix :** Gratuit (s'endort après 15 min d'inactivité) / 7$/mois sans inactivité
**Avantage :** render.yaml déjà configuré dans votre projet

### Étapes

**1. Créer un compte Render**
→ https://render.com — connectez-vous avec GitHub

**2. Nouveau Web Service**
- "New" → "Web Service"
- Connectez votre dépôt GitHub `immofacile`
- Render détecte `render.yaml` automatiquement

**3. Paramètres manuels si render.yaml non détecté**
- Environment : Python 3
- Build Command :
  ```
  pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
  ```
- Start Command :
  ```
  gunicorn immofacile.wsgi:application --bind 0.0.0.0:$PORT --workers 2
  ```

**4. Variables d'environnement**
Dans Render → votre service → "Environment" :
```
DJANGO_SETTINGS_MODULE  = immofacile.settings_production
SECRET_KEY              = [votre clé]
DEBUG                   = False
ALLOWED_HOSTS           = votre-app.onrender.com
DB_ENGINE               = django.db.backends.postgresql
DB_NAME                 = [depuis Render PostgreSQL]
DB_USER                 = [depuis Render PostgreSQL]
DB_PASSWORD             = [depuis Render PostgreSQL]
DB_HOST                 = [depuis Render PostgreSQL]
DB_PORT                 = 5432
DB_SSLMODE              = require
```

**5. Créer la base PostgreSQL**
Render → "New" → "PostgreSQL" → notez les credentials.

**6. Créer le superuser via Render Shell**
```bash
python manage.py createsuperuser
```

---

## 🐍 Option C — PythonAnywhere (Le plus simple pour Django)

**Prix :** Gratuit (domaine `.pythonanywhere.com`) / 5$/mois domaine custom
**Avantage :** Interface web, pas de terminal Linux requis

### Étapes

**1. Créer un compte**
→ https://www.pythonanywhere.com

**2. Ouvrir une console Bash**
Dashboard → "Consoles" → "Bash"

**3. Cloner votre projet**
```bash
git clone https://github.com/VOTRE_USERNAME/immofacile.git
cd immofacile
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**4. Créer le fichier .env**
```bash
nano .env
```
Collez et remplissez :
```
SECRET_KEY=votre-cle-secrete
DEBUG=False
ALLOWED_HOSTS=VOTRE_USERNAME.pythonanywhere.com
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=/home/VOTRE_USERNAME/immofacile/db.sqlite3
DJANGO_SETTINGS_MODULE=immofacile.settings_production
```
> Note : PythonAnywhere plan gratuit n'inclut pas PostgreSQL — utilisez SQLite ou payez 5$/mois.

**5. Préparer la base**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --no-input
python manage.py seed_demo
```

**6. Configurer l'application Web**
Dashboard → "Web" → "Add a new web app"
- Framework : Manual configuration
- Python version : 3.11

**7. Configurer le WSGI**
Cliquez sur le lien WSGI file, remplacez tout par :
```python
import os
import sys

path = '/home/VOTRE_USERNAME/immofacile'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'immofacile.settings_production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**8. Configurer Virtual Env**
Dans la section "Virtualenv" : `/home/VOTRE_USERNAME/immofacile/venv`

**9. Fichiers statiques**
| URL    | Directory                                         |
|--------|---------------------------------------------------|
| /static/ | /home/VOTRE_USERNAME/immofacile/staticfiles     |
| /media/  | /home/VOTRE_USERNAME/immofacile/media           |

**10. Reload**
Cliquez le bouton vert "Reload" — votre site est en ligne ! ✅

---

## 🖥️ Option D — VPS (DigitalOcean / Contabo — Contrôle total)

**Prix :** 4$/mois (Contabo) ou 6$/mois (DigitalOcean)
**Avantage :** Performances, contrôle total, SSL gratuit, PostgreSQL inclus

### Prérequis
- Un VPS Ubuntu 22.04
- Un nom de domaine (ex: immofacile.sn)
- Un client SSH (PuTTY sur Windows)

### Étapes

**1. Se connecter au VPS**
```bash
ssh root@VOTRE_IP_VPS
```

**2. Mettre à jour et installer les dépendances**
```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git certbot python3-certbot-nginx
```

**3. Créer la base PostgreSQL**
```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE immofacile_db;
CREATE USER immofacile_user WITH PASSWORD 'MotDePasseFort123!';
ALTER ROLE immofacile_user SET client_encoding TO 'utf8';
ALTER ROLE immofacile_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE immofacile_user SET timezone TO 'Africa/Dakar';
GRANT ALL PRIVILEGES ON DATABASE immofacile_db TO immofacile_user;
\q
```

**4. Déployer le projet**
```bash
cd /var/www
git clone https://github.com/VOTRE_USERNAME/immofacile.git
cd immofacile
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**5. Créer le fichier .env**
```bash
nano .env
```
```env
SECRET_KEY=votre-cle-secrete-generee
DEBUG=False
ALLOWED_HOSTS=immofacile.sn,www.immofacile.sn
DB_ENGINE=django.db.backends.postgresql
DB_NAME=immofacile_db
DB_USER=immofacile_user
DB_PASSWORD=MotDePasseFort123!
DB_HOST=localhost
DB_PORT=5432
DB_SSLMODE=disable
DJANGO_SETTINGS_MODULE=immofacile.settings_production
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=votre@gmail.com
EMAIL_HOST_PASSWORD=votre-app-password
```

**6. Initialiser la base**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --no-input
python manage.py seed_demo
```

**7. Configurer Gunicorn avec systemd**
```bash
nano /etc/systemd/system/immofacile.service
```
```ini
[Unit]
Description=ImmoFacile Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/immofacile
EnvironmentFile=/var/www/immofacile/.env
ExecStart=/var/www/immofacile/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/immofacile.sock \
    --timeout 120 \
    --access-logfile /var/log/immofacile/access.log \
    --error-logfile /var/log/immofacile/error.log \
    immofacile.wsgi:application

[Install]
WantedBy=multi-user.target
```
```bash
mkdir -p /var/log/immofacile
chown www-data:www-data /var/log/immofacile
chown -R www-data:www-data /var/www/immofacile
systemctl daemon-reload
systemctl enable immofacile
systemctl start immofacile
systemctl status immofacile
```

**8. Configurer Nginx**
```bash
nano /etc/nginx/sites-available/immofacile
```
```nginx
server {
    listen 80;
    server_name immofacile.sn www.immofacile.sn;

    client_max_body_size 10M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /var/www/immofacile;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        root /var/www/immofacile;
        expires 7d;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/immofacile.sock;
        proxy_read_timeout 120;
        proxy_connect_timeout 120;
    }
}
```
```bash
ln -s /etc/nginx/sites-available/immofacile /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

**9. SSL gratuit avec Let's Encrypt**
```bash
certbot --nginx -d immofacile.sn -d www.immofacile.sn
```
Certbot configure automatiquement HTTPS et renouvelle le certificat.

**10. Pointer votre domaine vers le VPS**
Chez votre registrar DNS :
| Type  | Nom | Valeur          |
|-------|-----|-----------------|
| A     | @   | VOTRE_IP_VPS    |
| A     | www | VOTRE_IP_VPS    |

**Votre site est en ligne sur https://immofacile.sn ✅**

---

## 🔄 Mettre à jour le site après des modifications

### Railway / Render (automatique via Git)
```bash
git add .
git commit -m "Mise à jour"
git push origin main
# Le déploiement est automatique !
```

### PythonAnywhere / VPS
```bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input

# PythonAnywhere : cliquez "Reload" dans le dashboard
# VPS :
systemctl restart immofacile
```

---

## ✅ Checklist finale avant mise en ligne

- [ ] `DEBUG=False` dans les variables d'environnement
- [ ] `SECRET_KEY` longue et aléatoire (jamais celle par défaut)
- [ ] `ALLOWED_HOSTS` contient votre vrai domaine
- [ ] Base de données PostgreSQL configurée
- [ ] `python manage.py collectstatic` exécuté
- [ ] `python manage.py migrate` exécuté
- [ ] Compte superuser créé
- [ ] SSL HTTPS activé
- [ ] Testez `/admin/` et `/dashboard/` en production
- [ ] Testez l'inscription, la connexion, la création d'annonce

---

## 🆘 Problèmes fréquents

| Erreur | Solution |
|--------|----------|
| `DisallowedHost` | Ajoutez votre domaine dans `ALLOWED_HOSTS` |
| Page blanche / 500 | Passez `DEBUG=True` temporairement pour voir l'erreur |
| Fichiers statiques manquants | Relancez `python manage.py collectstatic --no-input` |
| `ImproperlyConfigured: SECRET_KEY` | Définissez la variable d'environnement `SECRET_KEY` |
| Images non affichées | Vérifiez la config `MEDIA_URL` et les permissions du dossier `media/` |
| Erreur PostgreSQL | Vérifiez les credentials DB dans `.env` et que psycopg2 est installé |
