# ============================
# README.md
# ============================
# CFC Déblocages - Système de Gestion des Déblocages

Application web moderne pour la gestion des déblocages de prêts du Crédit Foncier du Cameroun (CFC).

## 🚀 Fonctionnalités

### Gestion des Prêts
- Création et suivi des demandes de prêts
- Gestion des différents types de prêts (classique acquéreur, locatif, etc.)
- Calcul automatique des mensualités
- Suivi de la validité des offres

### Gestion des Déblocages
- Demandes de déblocage avec suivi des travaux
- Validation multi-niveaux
- Rapports de visite de chantier
- Intégration avec les BET (Bureaux d'Études Techniques)

### Système d'Alertes
- Alertes automatiques pour les échéances
- Niveaux de sévérité (Orange/Rouge)
- Notifications par email et SMS
- Tableau de bord des alertes en temps réel

### Rapports et Tableaux de Bord
- Statistiques en temps réel
- Rapports personnalisables
- Export des données (Excel, PDF)
- Visualisations graphiques

## 🛠️ Stack Technique

### Backend
- **FastAPI** (Python 3.11) - Framework web moderne et performant
- **PostgreSQL** - Base de données principale
- **Redis** - Cache et broker de messages
- **Celery** - Gestion des tâches asynchrones
- **MinIO** - Stockage objet compatible S3
- **SQLAlchemy** - ORM
- **Alembic** - Migrations de base de données

### Frontend
- **React 18** avec TypeScript
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Query** - Gestion des requêtes API
- **React Hook Form + Zod** - Formulaires et validation
- **Zustand** - Gestion d'état
- **React Router** - Navigation
- **i18next** - Internationalisation (FR/EN)
- **Recharts** - Graphiques

### Infrastructure
- **Docker & Docker Compose** - Conteneurisation
- **Nginx** - Reverse proxy
- **GitHub Actions** - CI/CD

## 📋 Prérequis

- Docker et Docker Compose installés
- Git
- (Optionnel) Node.js 18+ et Python 3.11+ pour le développement local

## 🚀 Installation et Démarrage

### 1. Cloner le repository

```bash
git clone https://github.com/votre-org/cfc-deblocages.git
cd cfc-deblocages
```

### 2. Configuration de l'environnement

```bash
# Copier les fichiers d'environnement
cp .env.example .env
cp backend/.env.example backend/.env

# Éditer les fichiers .env avec vos configurations
# IMPORTANT: Changez les mots de passe par défaut!
```

### 3. Démarrage avec Docker Compose

```bash
# Démarrer tous les services
docker-compose up -d

# Vérifier que tous les services sont lancés
docker-compose ps

# Voir les logs
docker-compose logs -f
```

### 4. Initialisation de la base de données

```bash
# Exécuter les migrations
docker-compose exec backend alembic upgrade head

# Créer un utilisateur admin (optionnel)
docker-compose exec backend python scripts/create_admin.py
```

### 5. Accès à l'application

- **Application principale**: http://localhost
- **API Documentation**: http://localhost/api/docs
- **MinIO Console**: http://localhost:9001 (admin/MinioPassword123!)
- **Flower (Celery monitoring)**: http://localhost:5555

## 🔧 Configuration pour Production

### Variables d'environnement importantes

```env
# Backend
SECRET_KEY=<générer-une-clé-sécurisée>
DATABASE_URL=postgresql://user:password@host:5432/dbname
REDIS_URL=redis://:password@host:6379/0
ENVIRONMENT=production

# Sécurité
ALLOWED_HOSTS=example.com,www.example.com
BACKEND_CORS_ORIGINS=https://example.com

# Email
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Déploiement sur un serveur existant

Puisque votre serveur Linux héberge déjà plusieurs applications, voici comment configurer les ports pour éviter les conflits :

```bash
# Modifier docker-compose.yml pour utiliser des ports différents
NGINX_PORT=8080  # ou tout autre port disponible
DB_PORT=5433     # si PostgreSQL 5432 est déjà utilisé
REDIS_PORT=6380  # si Redis 6379 est déjà utilisé
```

### Configuration Nginx du serveur principal

Ajoutez cette configuration à votre Nginx principal pour rediriger vers l'application :

```nginx
server {
    listen 80;
    server_name cfc-deblocages.example.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📚 Documentation API

L'API est documentée automatiquement via OpenAPI/Swagger. Une fois l'application démarrée, accédez à :
- Swagger UI: http://localhost/api/docs
- ReDoc: http://localhost/api/redoc

## 🧪 Tests

```bash
# Tests backend
docker-compose exec backend pytest

# Tests frontend
docker-compose exec frontend npm test

# Tests avec couverture
docker-compose exec backend pytest --cov=app
docker-compose exec frontend npm run test:coverage
```

## 🔒 Sécurité

- Authentification JWT avec refresh tokens
- Rate limiting sur les endpoints sensibles
- Validation stricte des entrées avec Pydantic
- CORS configuré
- Headers de sécurité (CSP, XSS Protection, etc.)
- Chiffrement des mots de passe avec bcrypt

## 📈 Monitoring et Logs

- **Logs centralisés** : Tous les logs sont accessibles via `docker-compose logs`
- **Métriques** : Prometheus metrics disponibles sur `/metrics`
- **Health checks** : Endpoint `/health` pour vérifier l'état de l'application
- **Celery monitoring** : Interface Flower pour surveiller les tâches

## 🤝 Contribution

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push sur la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est la propriété du Crédit Foncier du Cameroun.

## 👥 Support

Pour toute question ou problème :
- Email : support@cfc-deblocages.cm
- Documentation : [Wiki du projet](https://github.com/votre-org/cfc-deblocages/wiki)

## 🎯 Roadmap

- [ ] Intégration avec le système bancaire
- [ ] Application mobile
- [ ] Signature électronique des documents
- [ ] Intelligence artificielle pour la détection des anomalies
- [ ] API publique pour les partenaires

---

Développé avec ❤️ pour le Crédit Foncier du Cameroun