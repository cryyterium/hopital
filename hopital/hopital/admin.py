from django.contrib import admin
from .models import (
    TypeEquipement,
    Salle,
    Profil,
    ObjetConnecte,
    CompetenceUtilisateur,
    HistoriqueConnexion,
    HistoriqueAction,
    DonneeObjet,
    Actualite,
    DemandeSuppression
)

admin.site.register(TypeEquipement)
admin.site.register(Salle)
admin.site.register(Profil)
admin.site.register(ObjetConnecte)
admin.site.register(CompetenceUtilisateur)
admin.site.register(HistoriqueConnexion)
admin.site.register(HistoriqueAction)
admin.site.register(DonneeObjet)
admin.site.register(Actualite)
admin.site.register(DemandeSuppression)