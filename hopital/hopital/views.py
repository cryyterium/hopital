from django.shortcuts import render

# Create your views here.
from .models import ObjetConnecte

def liste_objets(request):
    objets = ObjetConnecte.objects.all()
    return render(request, 'hopital/liste_objets.html', {'objets': objets})