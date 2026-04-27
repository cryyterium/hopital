import csv
from hopital.models import *

# ===== TYPE EQUIPEMENT =====
with open('hopital/data/type_equipement.csv', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        TypeEquipement.objects.update_or_create(
        id=row['id'],
        defaults={
        'nom': row['nom'],
        'description': row.get('description', '')
    }
)

print("TypeEquipement OK")
# ===== SERVICE =====
with open('hopital/data/service.csv', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        Service.objects.update_or_create(
            id=row['id'],
            defaults={
                'nom': row['nom'],
                'description': row.get('description', ''),
                'etage': row.get('etage') or None,
            }
        )

print("Service OK")
# ===== SALLE =====
with open('hopital/data/salle.csv', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        service = Service.objects.get(id=row['id_service'])

        Salle.objects.create(
            id=row['id'],
            nom=row['nom'],
            etage=row['etage'],
            service=service
        )

print("Salle OK")

# ===== OBJETS =====
with open('hopital/data/objet_connecte.csv', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)

    for row in reader:
        salle = Salle.objects.get(id=row['id_salle'])

        ObjetConnecte.objects.update_or_create(
            id=row['id'],
            defaults={
                'nom': row['nom'],
                'description': row.get('description', ''),
                'type': row.get('type', ''),
                'marque': row.get('marque', ''),
                'etat': row.get('etat', 'inactif'),
                'connectivite': row.get('connectivite', ''),
                'niveau_batterie': row.get('niveau_batterie') or None,
                'derniere_interaction': row.get('derniere_interaction') or None,
                'salle': salle,
            }
        )

print("Objets OK")

# ===== UTILISATEURS =====
from django.contrib.auth.models import User

with open('hopital/data/utilisateur.csv', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        user = User.objects.create_user(
            username=row['pseudo'],
            email=row['email'],
            password=row['mot_de_passe']
        )

        Profil.objects.create(
            user=user,
            age=row['age'],
            genre=row['genre'],
            type_membre=row['type_membre'],
            niveau=row['niveau']
        )

print("Utilisateurs OK")

# ===== ACTUALITES =====
with open('hopital/data/actualite.csv', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        auteur = Profil.objects.get(id=row['id_auteur'])

        Actualite.objects.create(
            titre=row['titre'],
            contenu=row['contenu'],
            auteur=auteur
        )

print("Actualites OK")