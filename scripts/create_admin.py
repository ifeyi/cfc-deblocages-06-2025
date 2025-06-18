# ============================
# scripts/create_admin.py
# ============================
#!/usr/bin/env python3
"""
Script pour créer un utilisateur administrateur
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import User, UserRole
from app.core.security import get_password_hash
from sqlalchemy.exc import IntegrityError

def create_admin_user():
    db = SessionLocal()
    
    try:
        # Demander les informations
        print("Création d'un utilisateur administrateur")
        print("-" * 40)
        
        username = input("Nom d'utilisateur: ")
        email = input("Email: ")
        full_name = input("Nom complet: ")
        password = input("Mot de passe: ")
        agency = input("Agence (optionnel): ")
        
        # Créer l'utilisateur
        admin_user = User(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=get_password_hash(password),
            role=UserRole.ADMIN,
            agency=agency or None,
            is_active=True,
            is_superuser=True,
            preferred_language="fr"
        )
        
        db.add(admin_user)
        db.commit()
        
        print(f"\n✅ Utilisateur administrateur '{username}' créé avec succès!")
        
    except IntegrityError:
        print("\n❌ Erreur: Un utilisateur avec ce nom ou email existe déjà.")
        db.rollback()
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
