from django.shortcuts import render

# Create your views here.
from .models import ObjetConnecte

def accueil(request):
    return render(request, 'hopital/accueil.html')

def liste_objets(request):
    objets = ObjetConnecte.objects.all()
    return render(request, 'hopital/liste_objets.html', {'objets': objets})

def index(request):
    return render(request, 'hopital/index.html')

def login_view(request):
    return render(request, 'hopital/login.html')

def register(request):
    return render(request, 'hopital/register.html')

def dashboard(request):
    return render(request, 'hopital/dashboard.html')

def profile(request):
    return render(request, 'hopital/profile.html')

def objects(request):
    return render(request, 'hopital/objects.html')

def room(request):
    return render(request, 'hopital/room.html')

def admin_page(request):
    return render(request, 'hopital/admin.html')

def manage_users(request):
    return render(request, 'hopital/manage-users.html')

def manage_objects(request):
    return render(request, 'hopital/manage-objects.html')

def stats(request):
    return render(request, 'hopital/stats.html')