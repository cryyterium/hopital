from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

# Create your views here.
from .models import ObjetConnecte, Salle, Profil, Service

def index(request):
    return render(request, 'hopital/index.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            profil, created = Profil.objects.get_or_create(user=user)

            if not profil.valide:
                return render(request, "hopital/login.html", {
                    "error": "Veuillez valider votre email avant de vous connecter."
                })

            login(request, user)
            return redirect("dashboard")

        return render(request, "hopital/login.html", {
            "error": "Login ou mot de passe incorrect."
        })

    return render(request, "hopital/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        prenom = request.POST.get("prenom")
        nom = request.POST.get("nom")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        if password != password_confirm:
            return render(request, "hopital/register.html", {
                "error": "Les mots de passe ne correspondent pas"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "hopital/register.html", {
                "error": "Login déjà utilisé"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=prenom,
            last_name=nom
        )

        profil = Profil.objects.create(
            user=user,
            niveau="débutant",
            statut="non validé",
            type_membre="Patient",
            valide=False
        )

        # lien de validation
        link = request.build_absolute_uri(
            reverse('validate_email', args=[user.id])
        )

        send_mail(
            "Validation de votre compte",
            f"Cliquez sur ce lien pour valider votre compte : {link}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

    return render(request, "hopital/register.html", {"success": "Un email de validation a été envoyé !"})

@login_required
def dashboard(request):
    profil, created = Profil.objects.get_or_create(user=request.user)

    nb_objets = ObjetConnecte.objects.count()
    nb_salles = Salle.objects.count()
    lits_disponibles = Salle.objects.count()

    points = profil.nb_connexions * 0.25 + profil.nb_actions * 0.50

    context = {
        "profil": profil,
        "nb_objets": nb_objets,
        "nb_salles": nb_salles,
        "lits_disponibles": lits_disponibles,
        "points": points,
    }
    return render(request, "hopital/dashboard.html", context)

@login_required
def profile(request):
    profil, created = Profil.objects.get_or_create(user=request.user)

    points = profil.nb_connexions * 0.25 + profil.nb_actions * 0.50
    error = None
    success = None

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "profile":
            request.user.first_name = request.POST.get("prenom")
            request.user.last_name = request.POST.get("nom")
            request.user.email = request.POST.get("email")
            request.user.save()

            profil.age = request.POST.get("age") or None
            profil.genre = request.POST.get("genre")
            profil.save()

            success = "Profil modifié avec succès."

        elif action == "password":
            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if not request.user.check_password(old_password):
                error = "Ancien mot de passe incorrect."
            elif new_password != confirm_password:
                error = "Les nouveaux mots de passe ne correspondent pas."
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                success = "Mot de passe modifié avec succès."

    return render(request, 'hopital/profile.html', {
        "profil": profil,
        "points": points,
        "error": error,
        "success": success,})

@login_required
def objects(request):
    objets = ObjetConnecte.objects.all()
    salles = Salle.objects.all()

    q = request.GET.get("q")
    type_objet = request.GET.get("type")
    etat = request.GET.get("etat")
    salle = request.GET.get("salle")

    if q:
        objets = objets.filter(
            Q(nom__icontains=q) | Q(description__icontains=q)
        )

    if type_objet:
        objets = objets.filter(type=type_objet)

    if etat:
        objets = objets.filter(etat=etat)

    if salle:
        objets = objets.filter(salle_id=salle)

    return render(request, 'hopital/objects.html', {'objets': objets,"salles": salles})

@login_required
def room(request):
    salles = Salle.objects.all()
    services = Service.objects.all()

    q = request.GET.get("q")
    service = request.GET.get("service")
    etage = request.GET.get("etage")

    if q:
        salles = salles.filter(nom__icontains=q)

    if service:
        salles = salles.filter(service_id=service)

    if etage:
        salles = salles.filter(etage=etage)

    return render(request, "hopital/room.html", {"salles": salles,"services": services,})

def admin_page(request):
    return render(request, 'hopital/admin.html')

def manage_users(request):
    return render(request, 'hopital/manage-users.html')

def manage_objects(request):
    return render(request, 'hopital/manage-objects.html')

def stats(request):
    return render(request, 'hopital/stats.html')

def validate_email(request, user_id):
    from django.contrib.auth.models import User
    from .models import Profil

    user = User.objects.get(id=user_id)
    profil = Profil.objects.get(user=user)

    profil.valide = True
    profil.statut = "validé"
    profil.save()

    return redirect("login")