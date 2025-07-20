"""URL configuration for the patient app."""

from django.urls import path

from . import views

app_name = "patient"

urlpatterns = [
    # Authentication
    path("logout/", views.logout_view, name="logout"),
    # Person CRUD
    path("", views.person_list, name="person_list"),
    path("create/", views.person_create, name="person_create"),
    path("<int:pk>/", views.person_detail, name="person_detail"),
    path("<int:pk>/edit/", views.person_edit, name="person_edit"),
    path("<int:pk>/delete/", views.person_delete, name="person_delete"),
    # HTMX endpoints
    path("pronoun-field/", views.pronoun_field, name="pronoun_field"),
    path("search/", views.search_persons, name="search_persons"),
]
