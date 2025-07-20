"""Forms for the patient_risk app."""

from django import forms

from patient.models import Person

from .models import PatientRiskAssessment


class PatientRiskAssessmentForm(forms.ModelForm):
    """Form for creating and editing Patient Risk Assessments."""

    class Meta:
        model = PatientRiskAssessment
        fields = [
            "person",
            "chads_score",
        ]
        widgets = {
            "person": forms.Select(
                attrs={
                    "class": "form-select",
                    "hx-get": "/patient_risk/patient-details/",
                    "hx-target": "#patient-details",
                    "hx-trigger": "change",
                }
            ),
            "chads_score": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "min": "0",
                    "max": "9",
                    "placeholder": "Enter CHADS2-VASc score (0-9)",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["person"].queryset = Person.objects.all().order_by("full_name")
        self.fields["person"].empty_label = "Select a patient..."

        # Add help text
        self.fields["chads_score"].help_text = (
            "CHADS2-VASc score for stroke risk assessment (0-9). "
            "Higher scores indicate higher stroke risk."
        )


class PatientSearchForm(forms.Form):
    """Form for searching patients in the risk assessment interface."""

    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Search patients by name...",
                "hx-get": "/patient_risk/search-patients/",
                "hx-target": "#patient-search-results",
                "hx-trigger": "input changed delay:300ms",
            }
        ),
    )
