# Makefile (racine du projet)
.PHONY: help build up down restart logs shell test clean backup restore init-alembic status

# Variables - CORRECTED SERVICE NAMES
DOCKER_COMPOSE = docker-compose
BACKEND_SERVICE = backend
FRONTEND_SERVICE = frontend
DB_SERVICE = postgres
BACKEND_CONTAINER = cfc_backend
FRONTEND_CONTAINER = cfc_frontend
DB_CONTAINER = cfc_postgres

help:
	@echo "CFC Déblocages - Commandes disponibles:"
	@echo ""
	@echo " make build          - Construire toutes les images Docker"
	@echo " make up             - Démarrer tous les services"
	@echo " make down           - Arrêter tous les services"
	@echo " make restart        - Redémarrer tous les services"
	@echo " make logs           - Afficher les logs en temps réel"
	@echo " make logs-back      - Afficher les logs du backend"
	@echo " make logs-db        - Afficher les logs de la base de données"
	@echo " make status         - Afficher le statut des conteneurs"
	@echo " make shell-back     - Ouvrir un shell dans le conteneur backend"
	@echo " make shell-front    - Ouvrir un shell dans le conteneur frontend"
	@echo " make test           - Lancer tous les tests"
	@echo " make migrate        - Exécuter les migrations de base de données"
	@echo " make migration      - Créer une nouvelle migration (usage: make migration message='description')"
	@echo " make backup         - Sauvegarder la base de données"
	@echo " make restore        - Restaurer la base de données"
	@echo " make clean          - Nettoyer les conteneurs et volumes"
	@echo " make dev            - Démarrer en mode développement"
	@echo " make prod           - Démarrer en mode production"
	@echo " make setup          - Configuration initiale complète du projet"

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) restart

logs:
	$(DOCKER_COMPOSE) logs -f

logs-back:
	$(DOCKER_COMPOSE) logs -f $(BACKEND_SERVICE)

logs-db:
	$(DOCKER_COMPOSE) logs -f $(DB_SERVICE)

status:
	@echo "Statut des conteneurs:"
	@$(DOCKER_COMPOSE) ps
	@echo ""
	@echo "Conteneurs en cours d'exécution:"
	@docker ps --filter "name=cfc_" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

shell-back:
	@if [ "$$($(DOCKER_COMPOSE) ps -q $(BACKEND_SERVICE))" = "" ]; then \
		echo "❌ Le service $(BACKEND_SERVICE) n'est pas en cours d'exécution."; \
		echo "Lancez 'make up' d'abord."; \
		exit 1; \
	fi
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) /bin/bash

shell-front:
	@if [ "$$($(DOCKER_COMPOSE) ps -q $(FRONTEND_SERVICE))" = "" ]; then \
		echo "❌ Le service $(FRONTEND_SERVICE) n'est pas en cours d'exécution."; \
		echo "Lancez 'make up' d'abord."; \
		exit 1; \
	fi
	$(DOCKER_COMPOSE) exec $(FRONTEND_SERVICE) /bin/sh

migrate:
	@echo "🔄 Running database migrations..."
	@echo ""
	@echo "📊 Checking service status..."
	@$(DOCKER_COMPOSE) ps $(BACKEND_SERVICE)
	@echo ""
	@if [ "$$($(DOCKER_COMPOSE) ps -q $(BACKEND_SERVICE))" = "" ]; then \
		echo "❌ Backend service not running. Starting services..."; \
		$(DOCKER_COMPOSE) up -d; \
		echo "⏳ Waiting for services to be ready..."; \
		sleep 15; \
	fi
	@echo "✅ Running Alembic migrations..."
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) alembic upgrade head

migration:
	@if [ -z "$(message)" ]; then \
		echo "Usage: make migration message='Your migration description'"; \
		exit 1; \
	fi
	@echo "Creating new migration: $(message)"
	@if [ "$$($(DOCKER_COMPOSE) ps -q $(BACKEND_SERVICE))" = "" ]; then \
		echo "❌ Backend service not running. Starting services..."; \
		$(DOCKER_COMPOSE) up -d; \
		sleep 10; \
	fi
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) alembic revision --autogenerate -m "$(message)"

test:
	@echo "Running backend tests..."
	@if [ "$$($(DOCKER_COMPOSE) ps -q $(BACKEND_SERVICE))" = "" ]; then \
		echo "❌ Backend service not running. Please run 'make up' first."; \
		exit 1; \
	fi
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) pytest
	@echo "Running frontend tests..."
	@if [ "$$($(DOCKER_COMPOSE) ps -q $(FRONTEND_SERVICE))" = "" ]; then \
		echo "❌ Frontend service not running. Please run 'make up' first."; \
		exit 1; \
	fi
	$(DOCKER_COMPOSE) exec $(FRONTEND_SERVICE) npm test

backup:
	@echo "Backing up database..."
	@if [ "$$($(DOCKER_COMPOSE) ps -q $(DB_SERVICE))" = "" ]; then \
		echo "❌ Database service not running. Please run 'make up' first."; \
		exit 1; \
	fi
	@mkdir -p backups
	@BACKUP_FILE="backups/cfc_backup_$$(date +%Y%m%d_%H%M%S).sql"; \
	$(DOCKER_COMPOSE) exec -T $(DB_SERVICE) pg_dump -U cfc_user cfc_deblocages > $$BACKUP_FILE; \
	echo "Backup saved to $$BACKUP_FILE"

restore:
	@echo "Available backups:"
	@ls -la backups/*.sql 2>/dev/null || echo "No backups found"
	@echo ""
	@read -p "Enter backup filename to restore: " BACKUP_FILE; \
	if [ -f "$$BACKUP_FILE" ]; then \
		if [ "$$($(DOCKER_COMPOSE) ps -q $(DB_SERVICE))" = "" ]; then \
			echo "❌ Database service not running. Please run 'make up' first."; \
			exit 1; \
		fi; \
		$(DOCKER_COMPOSE) exec -T $(DB_SERVICE) psql -U cfc_user cfc_deblocages < $$BACKUP_FILE; \
	else \
		echo "Backup file not found: $$BACKUP_FILE"; \
	fi

clean:
	$(DOCKER_COMPOSE) down -v
	docker system prune -f

dev:
	$(DOCKER_COMPOSE) up

prod:
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml up -d

# Quick health check
health:
	@echo "🏥 Health check des services CFC..."
	@echo ""
	@echo "📊 Statut des conteneurs:"
	@$(DOCKER_COMPOSE) ps
	@echo ""
	@echo "🔍 Test de connectivité:"
	@if curl -s http://localhost:8000/docs > /dev/null 2>&1; then \
		echo "✅ Backend API accessible"; \
	else \
		echo "❌ Backend API non accessible"; \
	fi
	@echo ""
	@echo "💾 Vérification de la base de données:"
	@$(DOCKER_COMPOSE) exec $(DB_SERVICE) pg_isready -U cfc_user -d cfc_deblocages 2>/dev/null && echo "✅ Base de données prête" || echo "❌ Base de données non prête"

# User management commands - add these to your Makefile

create-admin:
	@echo "🔐 Creating admin account..."
	@echo ""
	@if [ "$$($(DOCKER_COMPOSE) ps -q $(BACKEND_SERVICE))" = "" ]; then \
		echo "❌ Backend service not running. Starting services..."; \
		$(DOCKER_COMPOSE) up -d; \
		echo "⏳ Waiting for services to be ready..."; \
		sleep 15; \
	fi
	@echo "📝 Creating admin user with default credentials..."
	@echo "   Username: admin"
	@echo "   Email: admin@cfc.com"
	@echo "   Password: admin123"
	@echo "   Role: ADMIN"
	@echo ""
	@echo 'import sys' > /tmp/create_admin.py
	@echo 'import os' >> /tmp/create_admin.py
	@echo 'sys.path.append("/app")' >> /tmp/create_admin.py
	@echo 'os.chdir("/app")' >> /tmp/create_admin.py
	@echo '' >> /tmp/create_admin.py
	@echo 'from app.database import SessionLocal' >> /tmp/create_admin.py
	@echo 'from app.models.user import User, UserRole' >> /tmp/create_admin.py
	@echo 'from app.core.security import get_password_hash' >> /tmp/create_admin.py
	@echo 'from sqlalchemy.exc import IntegrityError' >> /tmp/create_admin.py
	@echo '' >> /tmp/create_admin.py
	@echo 'db = SessionLocal()' >> /tmp/create_admin.py
	@echo 'try:' >> /tmp/create_admin.py
	@echo '    existing_user = db.query(User).filter(User.email == "admin@cfc.com").first()' >> /tmp/create_admin.py
	@echo '    if existing_user:' >> /tmp/create_admin.py
	@echo '        print("❌ Admin user already exists with email: admin@cfc.com")' >> /tmp/create_admin.py
	@echo '        sys.exit(1)' >> /tmp/create_admin.py
	@echo '    ' >> /tmp/create_admin.py
	@echo '    admin_user = User(' >> /tmp/create_admin.py
	@echo '        username="admin",' >> /tmp/create_admin.py
	@echo '        email="admin@cfc.com",' >> /tmp/create_admin.py
	@echo '        full_name="Administrator User",' >> /tmp/create_admin.py
	@echo '        hashed_password=get_password_hash("admin123"),' >> /tmp/create_admin.py
	@echo '        role=UserRole.ADMIN,' >> /tmp/create_admin.py
	@echo '        is_active=True,' >> /tmp/create_admin.py
	@echo '        is_superuser=True,' >> /tmp/create_admin.py
	@echo '        preferred_language="fr"' >> /tmp/create_admin.py
	@echo '    )' >> /tmp/create_admin.py
	@echo '    ' >> /tmp/create_admin.py
	@echo '    db.add(admin_user)' >> /tmp/create_admin.py
	@echo '    db.commit()' >> /tmp/create_admin.py
	@echo '    ' >> /tmp/create_admin.py
	@echo '    print("✅ Admin user created successfully!")' >> /tmp/create_admin.py
	@echo '    print("   Username: admin")' >> /tmp/create_admin.py
	@echo '    print("   Email: admin@cfc.com")' >> /tmp/create_admin.py
	@echo '    print("   Password: admin123")' >> /tmp/create_admin.py
	@echo '    print("   Role: ADMIN")' >> /tmp/create_admin.py
	@echo '    print("   Please change the password after first login.")' >> /tmp/create_admin.py
	@echo '' >> /tmp/create_admin.py
	@echo 'except IntegrityError as e:' >> /tmp/create_admin.py
	@echo '    print("❌ Error creating admin user (user may already exist):", str(e))' >> /tmp/create_admin.py
	@echo '    db.rollback()' >> /tmp/create_admin.py
	@echo 'except Exception as e:' >> /tmp/create_admin.py
	@echo '    print("❌ Error creating admin user:", str(e))' >> /tmp/create_admin.py
	@echo '    db.rollback()' >> /tmp/create_admin.py
	@echo 'finally:' >> /tmp/create_admin.py
	@echo '    db.close()' >> /tmp/create_admin.py
	@docker cp /tmp/create_admin.py $(BACKEND_CONTAINER):/tmp/create_admin.py
	@$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) bash -c "cd /app && python /tmp/create_admin.py"
	@rm -f /tmp/create_admin.py

list-users:
	@echo "👥 Listing all users..."
	@echo ""
	@if [ "$$($(DOCKER_COMPOSE) ps -q $(BACKEND_SERVICE))" = "" ]; then \
		echo "❌ Backend service not running. Please run 'make up' first."; \
		exit 1; \
	fi
	@echo 'from app.database import SessionLocal' > /tmp/list_users.py
	@echo 'from app.models.user import User' >> /tmp/list_users.py
	@echo '' >> /tmp/list_users.py
	@echo 'db = SessionLocal()' >> /tmp/list_users.py
	@echo 'try:' >> /tmp/list_users.py
	@echo '    users = db.query(User).all()' >> /tmp/list_users.py
	@echo '    ' >> /tmp/list_users.py
	@echo '    if not users:' >> /tmp/list_users.py
	@echo '        print("No users found in database.")' >> /tmp/list_users.py
	@echo '    else:' >> /tmp/list_users.py
	@echo '        print(f"Found {len(users)} user(s):")' >> /tmp/list_users.py
	@echo '        print("")' >> /tmp/list_users.py
	@echo '        ' >> /tmp/list_users.py
	@echo '        for user in users:' >> /tmp/list_users.py
	@echo '            status = "🟢 Active" if user.is_active else "🔴 Inactive"' >> /tmp/list_users.py
	@echo '            role_icon = "👑" if user.is_superuser else "👤"' >> /tmp/list_users.py
	@echo '            ' >> /tmp/list_users.py
	@echo '            print(f"  {user.id}: {user.username} ({user.email})")' >> /tmp/list_users.py
	@echo '            print(f"      Name: {user.full_name}")' >> /tmp/list_users.py
	@echo '            print(f"      Role: {role_icon} {user.role.value}")' >> /tmp/list_users.py
	@echo '            print(f"      Agency: {user.agency if user.agency else \"Not specified\"}")' >> /tmp/list_users.py
	@echo '            print(f"      Status: {status}")' >> /tmp/list_users.py
	@echo '            print(f"      Language: {user.preferred_language}")' >> /tmp/list_users.py
	@echo '            print(f"      Created: {user.created_at}")' >> /tmp/list_users.py
	@echo '            if user.last_login:' >> /tmp/list_users.py
	@echo '                print(f"      Last Login: {user.last_login}")' >> /tmp/list_users.py
	@echo '            print("")' >> /tmp/list_users.py
	@echo '' >> /tmp/list_users.py
	@echo 'except Exception as e:' >> /tmp/list_users.py
	@echo '    print("❌ Error listing users:", str(e))' >> /tmp/list_users.py
	@echo 'finally:' >> /tmp/list_users.py
	@echo '    db.close()' >> /tmp/list_users.py
	@docker cp /tmp/list_users.py $(BACKEND_CONTAINER):/tmp/list_users.py
	@$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python /tmp/list_users.py
	@rm -f /tmp/list_users.py

reset-user-password:
	@echo "🔑 Resetting user password..."
	@echo ""
	@if [ "$$($(DOCKER_COMPOSE) ps -q $(BACKEND_SERVICE))" = "" ]; then \
		echo "❌ Backend service not running. Please run 'make up' first."; \
		exit 1; \
	fi
	@read -p "Enter username or email: " IDENTIFIER; \
	read -s -p "Enter new password: " NEW_PASSWORD; \
	echo ""; \
	echo "🔄 Updating password..."; \
	echo 'import sys' > /tmp/reset_password.py; \
	echo "identifier = \"$$IDENTIFIER\"" >> /tmp/reset_password.py; \
	echo "new_password = \"$$NEW_PASSWORD\"" >> /tmp/reset_password.py; \
	echo '' >> /tmp/reset_password.py; \
	echo 'if not identifier or not new_password:' >> /tmp/reset_password.py; \
	echo '    print("❌ Username/email and password are required")' >> /tmp/reset_password.py; \
	echo '    sys.exit(1)' >> /tmp/reset_password.py; \
	echo '' >> /tmp/reset_password.py; \
	echo 'from app.database import SessionLocal' >> /tmp/reset_password.py; \
	echo 'from app.models.user import User' >> /tmp/reset_password.py; \
	echo 'from app.core.security import get_password_hash' >> /tmp/reset_password.py; \
	echo '' >> /tmp/reset_password.py; \
	echo 'db = SessionLocal()' >> /tmp/reset_password.py; \
	echo 'try:' >> /tmp/reset_password.py; \
	echo '    user = db.query(User).filter(' >> /tmp/reset_password.py; \
	echo '        (User.email == identifier) | (User.username == identifier)' >> /tmp/reset_password.py; \
	echo '    ).first()' >> /tmp/reset_password.py; \
	echo '    ' >> /tmp/reset_password.py; \
	echo '    if not user:' >> /tmp/reset_password.py; \
	echo '        print(f"❌ User not found: {identifier}")' >> /tmp/reset_password.py; \
	echo '        sys.exit(1)' >> /tmp/reset_password.py; \
	echo '    ' >> /tmp/reset_password.py; \
	echo '    user.hashed_password = get_password_hash(new_password)' >> /tmp/reset_password.py; \
	echo '    db.commit()' >> /tmp/reset_password.py; \
	echo '    ' >> /tmp/reset_password.py; \
	echo '    print(f"✅ Password updated successfully for user: {user.username} ({user.email})")' >> /tmp/reset_password.py; \
	echo '' >> /tmp/reset_password.py; \
	echo 'except Exception as e:' >> /tmp/reset_password.py; \
	echo '    print("❌ Error updating password:", str(e))' >> /tmp/reset_password.py; \
	echo '    db.rollback()' >> /tmp/reset_password.py; \
	echo 'finally:' >> /tmp/reset_password.py; \
	echo '    db.close()' >> /tmp/reset_password.py; \
	docker cp /tmp/reset_password.py $(BACKEND_CONTAINER):/tmp/reset_password.py; \
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python /tmp/reset_password.py; \
	rm -f /tmp/reset_password.py

delete-user:
	@echo "🗑️ Deleting user..."
	@echo ""
	@if [ "$$($(DOCKER_COMPOSE) ps -q $(BACKEND_SERVICE))" = "" ]; then \
		echo "❌ Backend service not running. Please run 'make up' first."; \
		exit 1; \
	fi
	@read -p "Enter username or email to delete: " IDENTIFIER; \
	read -p "Are you sure you want to delete this user? (y/N): " CONFIRM; \
	if [ "$$CONFIRM" = "y" ] || [ "$$CONFIRM" = "Y" ]; then \
		echo 'import sys' > /tmp/delete_user.py; \
		echo "identifier = \"$$IDENTIFIER\"" >> /tmp/delete_user.py; \
		echo '' >> /tmp/delete_user.py; \
		echo 'if not identifier:' >> /tmp/delete_user.py; \
		echo '    print("❌ Username or email is required")' >> /tmp/delete_user.py; \
		echo '    sys.exit(1)' >> /tmp/delete_user.py; \
		echo '' >> /tmp/delete_user.py; \
		echo 'from app.database import SessionLocal' >> /tmp/delete_user.py; \
		echo 'from app.models.user import User' >> /tmp/delete_user.py; \
		echo '' >> /tmp/delete_user.py; \
		echo 'db = SessionLocal()' >> /tmp/delete_user.py; \
		echo 'try:' >> /tmp/delete_user.py; \
		echo '    user = db.query(User).filter(' >> /tmp/delete_user.py; \
		echo '        (User.email == identifier) | (User.username == identifier)' >> /tmp/delete_user.py; \
		echo '    ).first()' >> /tmp/delete_user.py; \
		echo '    ' >> /tmp/delete_user.py; \
		echo '    if not user:' >> /tmp/delete_user.py; \
		echo '        print(f"❌ User not found: {identifier}")' >> /tmp/delete_user.py; \
		echo '        sys.exit(1)' >> /tmp/delete_user.py; \
		echo '    ' >> /tmp/delete_user.py; \
		echo '    username = user.username' >> /tmp/delete_user.py; \
		echo '    email = user.email' >> /tmp/delete_user.py; \
		echo '    ' >> /tmp/delete_user.py; \
		echo '    db.delete(user)' >> /tmp/delete_user.py; \
		echo '    db.commit()' >> /tmp/delete_user.py; \
		echo '    ' >> /tmp/delete_user.py; \
		echo '    print(f"✅ User deleted successfully: {username} ({email})")' >> /tmp/delete_user.py; \
		echo '' >> /tmp/delete_user.py; \
		echo 'except Exception as e:' >> /tmp/delete_user.py; \
		echo '    print("❌ Error deleting user:", str(e))' >> /tmp/delete_user.py; \
		echo '    db.rollback()' >> /tmp/delete_user.py; \
		echo 'finally:' >> /tmp/delete_user.py; \
		echo '    db.close()' >> /tmp/delete_user.py; \
		docker cp /tmp/delete_user.py $(BACKEND_CONTAINER):/tmp/delete_user.py; \
		$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python /tmp/delete_user.py; \
		rm -f /tmp/delete_user.py; \
	else \
		echo "❌ User deletion cancelled."; \
	fi