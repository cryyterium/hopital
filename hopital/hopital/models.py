from django.db import models
from django.contrib.auth.models import User


class TypeEquipement(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Service(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    etage = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Salle(models.Model):
    nom = models.CharField(max_length=50)
    etage = models.IntegerField(blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.nom


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=10, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    type_membre = models.CharField(max_length=50, blank=True, null=True)

    niveau = models.CharField(max_length=20, default='débutant')
    nb_connexions = models.IntegerField(default=0)
    nb_actions = models.IntegerField(default=0)
    statut = models.CharField(max_length=20, default='non validé')
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class ObjetConnecte(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    marque = models.CharField(max_length=50, blank=True, null=True)
    etat = models.CharField(max_length=20, default='inactif')
    connectivite = models.CharField(max_length=50, blank=True, null=True)
    niveau_batterie = models.IntegerField(blank=True, null=True)
    derniere_interaction = models.DateTimeField(blank=True, null=True)
    salle = models.ForeignKey(Salle, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.nom


class CompetenceUtilisateur(models.Model):
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE)
    type_equipement = models.ForeignKey(TypeEquipement, on_delete=models.CASCADE)
    points = models.FloatField(default=0)
    niveau = models.CharField(max_length=20, default='débutant')

    def __str__(self):
        return f"{self.profil} - {self.type_equipement}"


class HistoriqueConnexion(models.Model):
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE)
    date_heure = models.DateTimeField(auto_now_add=True)
    points_gagnes = models.FloatField(default=0.25)

    def __str__(self):
        return f"Connexion de {self.profil}"


class HistoriqueAction(models.Model):
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE)
    objet = models.ForeignKey(ObjetConnecte, on_delete=models.CASCADE)
    type_action = models.CharField(max_length=50)
    date_heure = models.DateTimeField(auto_now_add=True)
    points_gagnes = models.FloatField(default=0.50)

    def __str__(self):
        return f"{self.type_action} - {self.profil}"


class DonneeObjet(models.Model):
    objet = models.ForeignKey(ObjetConnecte, on_delete=models.CASCADE)
    valeur = models.FloatField()
    unite = models.CharField(max_length=20)
    date_heure = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.objet} : {self.valeur} {self.unite}"


class Actualite(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(Profil, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.titre


class DemandeSuppression(models.Model):
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE)
    objet = models.ForeignKey(ObjetConnecte, on_delete=models.CASCADE)
    motif = models.TextField()
    statut = models.CharField(max_length=20, default='en attente')

    def __str__(self):
        return f"Demande suppression - {self.objet}"