from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Sum,Q
from django.conf import settings
from django.urls import reverse

# Create your views here.
from .models import ObjetConnecte, Salle, Profil, Service, HistoriqueConnexion, HistoriqueAction

def index(request):
    nb_salles = Salle.objects.count()
    nb_services = Service.objects.count()
    nb_objets = ObjetConnecte.objects.count()
    total_lits = Salle.objects.aggregate(Sum("nombre_lits"))["nombre_lits__sum"] or 0
    lits_occupes = Salle.objects.aggregate(Sum("lits_occupes"))["lits_occupes__sum"] or 0
    lits_disponibles = total_lits - lits_occupes


    return render(request, 'hopital/index.html', {"nb_salles": nb_salles,
                                                    "nb_services": nb_services,
                                                    "nb_objets": nb_objets,
                                                    "total_lits": total_lits,
                                                    "lits_occupes": lits_occupes,
                                                    "lits_disponibles": lits_disponibles,})

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

            profil.nb_connexions += 1
            profil.save()

            HistoriqueConnexion.objects.create(
                profil=profil,
                points_gagnes=0.25
            )

            maj_niveau(profil)

            return redirect("dashboard")

        return render(request, "hopital/login.html", {
            "error": "Login ou mot de passe incorrect."
        })

    return render(request, "hopital/login.html")

def logout_view(request):
    logout(request)
    return redirect("index")


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
    total_lits = Salle.objects.aggregate(Sum("nombre_lits"))["nombre_lits__sum"] or 0
    lits_occupes = Salle.objects.aggregate(Sum("lits_occupes"))["lits_occupes__sum"] or 0
    lits_disponibles = total_lits - lits_occupes
    connexions = HistoriqueConnexion.objects.filter(profil=profil).order_by("-date_heure")[:5]
    actions = HistoriqueAction.objects.filter(profil=profil).order_by("-date_heure")[:5]
    actifs = ObjetConnecte.objects.filter(etat="actif").count()
    maintenance = ObjetConnecte.objects.filter(etat="maintenance").count()
    batterie_faible = ObjetConnecte.objects.filter(niveau_batterie__lt=20).count()

    total = ObjetConnecte.objects.count()

    if total > 0:
        taux_maintenance = (maintenance / total) * 100
    else:
        taux_maintenance = 0

    points = profil.nb_connexions * 0.25 + profil.nb_actions * 0.50
    if profil.niveau == "débutant":
        points_min = 0
        points_max = 5
    elif profil.niveau == "intermediaire":
        points_min = 5
        points_max = 10
    elif profil.niveau == "avancé":
        points_min = 10
        points_max = 20
    else:
        points_min = 20
        points_max = 20

    if points_max > points_min:
        progression = ((points - points_min) / (points_max - points_min)) * 100
    else:
        progression = 100

    progression = max(0, min(progression, 100))

    context = {
        "profil": profil,
        "nb_objets": nb_objets,
        "nb_salles": nb_salles,
        "lits_disponibles": lits_disponibles,
        "points": points,
        "progression": progression,
        "connexions": connexions,
        "actions": actions,
        "actifs": actifs,
        "maintenance": maintenance,
        "batterie_faible": batterie_faible,
        "taux_maintenance": taux_maintenance,
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

            # +0.5 point car modification du profil
            profil.nb_actions += 1

            # Mise à jour du niveau
            maj_niveau(profil)
            
            profil.save()

            success = "Profil modifié avec succès. Vous avez gagné 0.5 point."

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

                # +0.5 point car changement de mot de passe
                profil.nb_actions += 1

                maj_niveau(profil)

                profil.save()

                success = "Mot de passe modifié avec succès. Vous avez gagné 0.5 point."
    
    points = profil.nb_connexions * 0.25 + profil.nb_actions * 0.50

    if profil.niveau == "débutant":
        prochain_niveau = "intermediaire"
        points_requis = 5
        points_min = 0
        progression = ((points - points_min) / (points_requis - points_min)) * 100
    elif profil.niveau == "intermediaire":
        prochain_niveau = "avancé"
        points_requis = 10
        points_min = 5
        progression = ((points - points_min) / (points_requis - points_min)) * 100
    elif profil.niveau == "avancé":
        prochain_niveau = "expert"
        points_requis = 20
        points_min = 10
        progression = ((points - points_min) / (points_requis - points_min)) * 100
    else:
        prochain_niveau = "max"
        points_requis = 0
        progression = 100
    
    progression = max(0, min(progression, 100))

    points_restants = max(points_requis - points, 0)
        

    return render(request, 'hopital/profile.html', {
        "profil": profil,
        "points": points,
        "points": points,
        "prochain_niveau": prochain_niveau,
        "points_requis": points_requis,
        "points_restants": points_restants,
        "progression": progression,
        "error": error,
        "success": success,})

@login_required
def objects(request):
    profil, created = Profil.objects.get_or_create(user=request.user)
    
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

    return render(request, 'hopital/objects.html', {'objets': objets,"salles": salles,"profil": profil})

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

@login_required
def manage_objects(request):
    profil = Profil.objects.get(user=request.user)

    # sécurité
    if profil.niveau not in ["avancé", "expert"]:
        return redirect("objects")

    salles = Salle.objects.all()
    objets = ObjetConnecte.objects.order_by("-id")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add":
            objet =ObjetConnecte.objects.create(
                nom=request.POST.get("nom"),
                type=request.POST.get("type"),
                etat=request.POST.get("etat"),
                salle_id=request.POST.get("salle"),
                connectivite=request.POST.get("connectivite"),
                niveau_batterie=request.POST.get("niveau_batterie") or None,
                description=request.POST.get("description"),
                marque=request.POST.get("marque"),
            )
            HistoriqueAction.objects.create(
                profil=profil,
                objet=objet,
                type_action="ajout"
            )

            profil.nb_actions += 1

        elif action == "edit":
            objet = ObjetConnecte.objects.get(id=request.POST.get("objet_id"))
            objet.nom = request.POST.get("nom")
            objet.type = request.POST.get("type")
            objet.etat = request.POST.get("etat")
            objet.salle_id = request.POST.get("salle")
            objet.description = request.POST.get("description")
            objet.marque = request.POST.get("marque")
            objet.connectivite = request.POST.get("connectivite")
            objet.niveau_batterie = request.POST.get("niveau_batterie") or None
            objet.save()
            profil.nb_actions += 1

            HistoriqueAction.objects.create(
                profil=profil,
                objet=objet,
                type_action="modification"
            )

        elif action == "delete":
            objet = ObjetConnecte.objects.get(id=request.POST.get("objet_id"))
            HistoriqueAction.objects.create(
                profil=profil,
                objet=objet,
                type_action="suppression"
            )
            objet.delete()
            profil.nb_actions += 1

        maj_niveau(profil)

        return redirect("manage_objects")

    return render(request, "hopital/manage-objects.html", {"salles": salles,"objets": objets})

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


def maj_niveau(profil):

    points = profil.nb_connexions * 0.25 + profil.nb_actions * 0.50

    if points >= 20:
        profil.niveau = "expert"
    elif points >= 10:
        profil.niveau = "avancé"
    elif points >= 5:
        profil.niveau = "intermediaire"
    else:
        profil.niveau = "débutant"

    profil.save()

@login_required
def members(request):
    profils = Profil.objects.select_related("user").all()

    q = request.GET.get("q")

    if q:
        profils = profils.filter(user__username__icontains=q)

    return render(request, "hopital/members.html", {
        "profils": profils
    })

@login_required
def objet_detail(request, id):
    profil, created = Profil.objects.get_or_create(user=request.user)
    objet = get_object_or_404(ObjetConnecte, id=id)

    HistoriqueAction.objects.create(
        profil=profil,
        objet=objet,
        type_action="consultation"
    )

    return render(request, "hopital/objet_detail.html", {"objet": objet})
