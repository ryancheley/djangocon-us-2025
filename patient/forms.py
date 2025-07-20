"""Forms for the patient app."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Person


class PersonForm(forms.ModelForm):
    """Form for creating and editing Person records."""

    class Meta:
        model = Person
        fields = [
            "full_name",
            "given_names",
            "family_names",
            "preferred_name",
            "patronymic",
            "matronymic",
            "middle_names",
            "suffix",
            "prefix",
            "legal_name",
            "date_of_birth",
            "gender_identity",
            "biological_sex",
            "pronouns",
            "custom_pronouns",
            "legal_sex",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter full name as preferred",
                }
            ),
            "given_names": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "First/given names"}
            ),
            "family_names": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Last/family names"}
            ),
            "preferred_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Preferred name or nickname",
                }
            ),
            "patronymic": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Father's name derivative"}
            ),
            "matronymic": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Mother's name derivative"}
            ),
            "middle_names": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Middle names"}
            ),
            "suffix": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Jr., Sr., III, etc."}
            ),
            "prefix": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Dr., Prof., etc."}
            ),
            "legal_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Full legal name on documents",
                }
            ),
            "date_of_birth": forms.DateInput(
                attrs={"class": "form-input", "type": "date"}
            ),
            "gender_identity": forms.Select(attrs={"class": "form-select"}),
            "biological_sex": forms.Select(attrs={"class": "form-select"}),
            "pronouns": forms.Select(
                attrs={
                    "class": "form-select",
                    "hx-trigger": "change",
                    "hx-target": "#custom-pronouns-field",
                    "hx-get": "/patient/pronoun-field/",
                }
            ),
            "custom_pronouns": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "e.g., fae/faer"}
            ),
            "legal_sex": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add empty choice to select fields
        choice_fields = ["gender_identity", "biological_sex", "pronouns", "legal_sex"]
        for field_name in choice_fields:
            if field_name in self.fields:
                choices = list(self.fields[field_name].choices)
                choices.insert(0, ("", "-- Select --"))
                self.fields[field_name].choices = choices


class CustomLoginForm(AuthenticationForm):
    """Custom login form with styling."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-input", "placeholder": "Password"}
        )
    )
