# ============================
# scripts/init_data.py
# ============================
#!/usr/bin/env python3
"""
Script pour initialiser les données de test
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Client, Loan, LoanType, LoanStatus
from datetime import datetime, timedelta
import random

def create_test_data():
    db = SessionLocal()
    
    try:
        print("Création des données de test...")
        
        # Créer des clients
        clients = []
        for i in range(10):
            client = Client(
                client_number=f"CL{str(i+1).zfill(6)}",
                name=f"Client Test {i+1}",
                company_name=f"Entreprise {i+1}" if i % 2 == 0 else None,
                address=f"{i+1} Rue de Test, Yaoundé",
                phone=f"6{random.randint(70, 99)}{random.randint(100000, 999999)}",
                email=f"client{i+1}@example.com",
                id_card_number=f"ID{str(i+1).zfill(8)}",
                is_active=True
            )
            db.add(client)
            clients.append(client)
        
        db.flush()
        
        # Créer des prêts
        loan_types = list(LoanType)
        statuses = [LoanStatus.APPROVED, LoanStatus.IN_PROGRESS, LoanStatus.DISBURSING]
        
        for i, client in enumerate(clients[:5]):
            loan = Loan(
                loan_number=f"2024/102/{str(i+1).zfill(7)}/541",
                client_id=client.id,
                loan_type=random.choice(loan_types),
                status=random.choice(statuses),
                amount=random.randint(10, 100) * 1000000,  # Entre 10M et 100M FCFA
                duration_months=random.choice([120, 180, 240]),  # 10, 15 ou 20 ans
                grace_period_months=random.choice([0, 6, 12]),
                interest_rate=random.choice([5.5, 6.0, 6.5]),
                monthly_payment=random.randint(200000, 1000000),
                approval_date=datetime.now() - timedelta(days=random.randint(30, 90)),
                validity_end_date=datetime.now() + timedelta(days=random.randint(30, 60)),
                property_title_number=f"TF{str(i+1).zfill(5)}",
                property_location=f"Quartier {i+1}, Yaoundé",
                life_insurance_company="SUNU Assurance",
                fire_insurance_company="AXA Cameroun"
            )
            db.add(loan)
        
        db.commit()
        print("✅ Données de test créées avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()