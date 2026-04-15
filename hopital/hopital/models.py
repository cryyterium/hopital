from django.db import models

# Create your models here.

class Service(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.nom


class Chambre(models.Model):
    numero = models.CharField(max_length=20)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"Chambre {self.numero}"


class ObjetConnecte(models.Model):
    nom = models.CharField(max_length=100)
    type_objet = models.CharField(max_length=100)
    statut = models.CharField(max_length=50)
    batterie = models.IntegerField()
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom