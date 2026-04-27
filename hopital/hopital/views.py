from django.shortcuts import render

# Create your views here.
from .models import ObjetConnecte

def accueil(request):
    return render(request, 'hopital/accueil.html')

def liste_objets(request):
    objets = ObjetConnecte.objects.all()
    return render(request, 'hopital/liste_objets.html', {'objets': objets})

def index(request):
    return render(request, 'hospital/index.html')

def login_view(request):
    return render(request, 'hospital/login.html')

def register(request):
    return render(request, 'hospital/register.html')

def dashboard(request):
    return render(request, 'hospital/dashboard.html')

def profile(request):
    return render(request, 'hospital/profile.html')

def objects(request):
    return render(request, 'hospital/objects.html')

def room(request):
    return render(request, 'hospital/room.html')

def admin_page(request):
    return render(request, 'hospital/admin.html')

def manage_users(request):
    return render(request, 'hospital/manage-users.html')

def manage_objects(request):
    return render(request, 'hospital/manage-objects.html')

def stats(request):
    return render(request, 'hospital/stats.html')