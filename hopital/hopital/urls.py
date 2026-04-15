from django.urls import path
from .views import liste_objets

urlpatterns = [
    path('objets/', liste_objets, name='liste_objets'),
]