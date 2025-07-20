"""URL patterns for the patient_risk app."""

from django.urls import path

from . import views

app_name = "patient_risk"

urlpatterns = [
    path("", views.risk_assessment_list, name="list"),
    path("create/", views.risk_assessment_create, name="create"),
    path("patient-details/", views.patient_details, name="patient_details"),
    path("search-patients/", views.search_patients, name="search_patients"),
]
