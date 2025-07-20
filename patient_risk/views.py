from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from patient.models import Person

from .forms import PatientRiskAssessmentForm, PatientSearchForm
from .models import PatientRiskAssessment


def risk_assessment_list(request):
    """List all patient risk assessments with search and filtering."""
    assessments = PatientRiskAssessment.objects.select_related("person").all()
    search_form = PatientSearchForm()

    # Handle search
    search_query = request.GET.get("search", "")
    if search_query:
        assessments = assessments.filter(
            Q(person__full_name__icontains=search_query)
            | Q(person__given_names__icontains=search_query)
            | Q(person__family_names__icontains=search_query)
        )

    context = {
        "assessments": assessments,
        "search_form": search_form,
        "search_query": search_query,
    }

    return render(request, "patient_risk/risk_assessment_list.html", context)


def risk_assessment_create(request):
    """Create a new patient risk assessment."""
    if request.method == "POST":
        form = PatientRiskAssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save()
            messages.success(
                request, f"Risk assessment created for {assessment.person.full_name}"
            )

            # Return partial template for HTMX
            if request.headers.get("HX-Request"):
                return render(
                    request,
                    "patient_risk/partials/assessment_success.html",
                    {"assessment": assessment},
                )

            return redirect("patient_risk:list")
    else:
        form = PatientRiskAssessmentForm()

    context = {"form": form}

    # Return partial template for HTMX
    if request.headers.get("HX-Request"):
        return render(request, "patient_risk/partials/assessment_form.html", context)

    return render(request, "patient_risk/risk_assessment_form.html", context)


def patient_details(request):
    """Get patient details for selected patient (HTMX endpoint)."""
    patient_id = request.GET.get("person")

    if patient_id:
        try:
            patient = Person.objects.get(id=patient_id)
            context = {"patient": patient}
            return render(
                request, "patient_risk/partials/patient_details.html", context
            )
        except Person.DoesNotExist:
            pass

    return render(
        request, "patient_risk/partials/patient_details.html", {"patient": None}
    )


def search_patients(request):
    """Search patients for the risk assessment form (HTMX endpoint)."""
    search_query = request.GET.get("search", "").strip()

    if search_query and len(search_query) >= 2:
        patients = Person.objects.filter(
            Q(full_name__icontains=search_query)
            | Q(given_names__icontains=search_query)
            | Q(family_names__icontains=search_query)
        ).order_by("full_name")[:10]  # Limit to 10 results
    else:
        patients = []

    context = {
        "patients": patients,
        "search_query": search_query,
    }

    return render(request, "patient_risk/partials/patient_search_results.html", context)
