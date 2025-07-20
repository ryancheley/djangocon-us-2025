"""Views for the patient app."""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import CustomLoginForm, PersonForm
from .models import Person


def login_view(request):
    """Login view."""
    if request.user.is_authenticated:
        return redirect("patient:person_list")

    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get("next", "patient:person_list")
            return redirect(next_url)
    else:
        form = CustomLoginForm()

    return render(request, "patient/login.html", {"form": form})


@login_required
def logout_view(request):
    """Logout view."""
    logout(request)
    return redirect("/")


@login_required
def person_list(request):
    """List all persons with search functionality."""
    query = request.GET.get("q", "")
    persons = Person.objects.all().order_by("family_names", "given_names")

    if query:
        persons = persons.filter(
            Q(full_name__icontains=query)
            | Q(given_names__icontains=query)
            | Q(family_names__icontains=query)
            | Q(preferred_name__icontains=query)
        )

    paginator = Paginator(persons, 20)  # Show 20 persons per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "query": query, "total_count": persons.count()}

    # For HTMX requests, return just the table content
    if request.headers.get("HX-Request"):
        return render(request, "patient/partials/person_table.html", context)

    return render(request, "patient/person_list.html", context)


@login_required
def person_create(request):
    """Create a new person."""
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.created_by = request.user
            person.updated_by = request.user
            person.save()
            messages.success(
                request, f'Person "{person.display_name}" created successfully.'
            )

            # For HTMX requests, return a success response
            if request.headers.get("HX-Request"):
                return HttpResponse(
                    '<div class="alert alert-success">Person created successfully!</div>',
                    headers={"HX-Trigger": "personCreated"},
                )

            return redirect("patient:person_detail", pk=person.pk)
    else:
        form = PersonForm()

    context = {"form": form, "action": "Create"}

    # For HTMX requests, return just the form
    if request.headers.get("HX-Request"):
        return render(request, "patient/partials/person_form.html", context)

    return render(request, "patient/person_form.html", context)


@login_required
def person_detail(request, pk):
    """Display person details."""
    person = get_object_or_404(Person, pk=pk)
    return render(request, "patient/person_detail.html", {"person": person})


@login_required
def person_edit(request, pk):
    """Edit an existing person."""
    person = get_object_or_404(Person, pk=pk)

    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            person = form.save(commit=False)
            person.updated_by = request.user
            person.save()
            messages.success(
                request, f'Person "{person.display_name}" updated successfully.'
            )

            # For HTMX requests, return a success response
            if request.headers.get("HX-Request"):
                return HttpResponse(
                    '<div class="alert alert-success">Person updated successfully!</div>',
                    headers={"HX-Trigger": "personUpdated"},
                )

            return redirect("patient:person_detail", pk=person.pk)
    else:
        form = PersonForm(instance=person)

    context = {"form": form, "person": person, "action": "Edit"}

    # For HTMX requests, return just the form
    if request.headers.get("HX-Request"):
        return render(request, "patient/partials/person_form.html", context)

    return render(request, "patient/person_form.html", context)


@login_required
@require_http_methods(["DELETE"])
def person_delete(request, pk):
    """Delete a person."""
    person = get_object_or_404(Person, pk=pk)
    person_name = person.display_name
    person.delete()

    messages.success(request, f'Person "{person_name}" deleted successfully.')

    # For HTMX requests, return empty response with trigger
    if request.headers.get("HX-Request"):
        return HttpResponse("", headers={"HX-Trigger": "personDeleted"})

    return redirect("patient:person_list")


@login_required
def pronoun_field(request):
    """Return custom pronouns field based on pronoun selection."""
    pronouns = request.GET.get("pronouns", "")

    if pronouns == "other":
        return render(
            request, "patient/partials/custom_pronouns_field.html", {"show_field": True}
        )
    else:
        return render(
            request,
            "patient/partials/custom_pronouns_field.html",
            {"show_field": False},
        )


@login_required
def search_persons(request):
    """HTMX endpoint for searching persons."""
    query = request.GET.get("q", "").strip()

    if not query:
        persons = Person.objects.none()
    else:
        persons = Person.objects.filter(
            Q(full_name__icontains=query)
            | Q(given_names__icontains=query)
            | Q(family_names__icontains=query)
            | Q(preferred_name__icontains=query)
        ).order_by("family_names", "given_names")[:10]  # Limit to 10 results

    return render(
        request,
        "patient/partials/search_results.html",
        {"persons": persons, "query": query},
    )
