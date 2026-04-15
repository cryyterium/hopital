from django.contrib import admin

# Register your models here.
from .models import Service, Chambre, ObjetConnecte

admin.site.register(Service)
admin.site.register(Chambre)
admin.site.register(ObjetConnecte)