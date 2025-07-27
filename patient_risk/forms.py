"""Forms for the patient_risk app."""

from django import forms

from patient.models import Person

from .models import PatientRiskAssessment


class PatientRiskAssessmentForm(forms.ModelForm):
    """Form for creating and editing Patient Risk Assessments."""

    # Individual contraindication fields that will be converted to JSON
    warfarin_allergy = forms.BooleanField(
        required=False,
        label="Warfarin allergy",
        help_text="Patient has known allergy to warfarin",
    )
    bleeding_disorder = forms.BooleanField(
        required=False,
        label="Bleeding disorder",
        help_text="Patient has bleeding disorder or bleeding risk",
    )
    pregnancy_status = forms.BooleanField(
        required=False,
        label="Pregnancy status",
        help_text="Patient is pregnant or planning pregnancy",
    )

    class Meta:
        model = PatientRiskAssessment
        fields = [
            "person",
            "chads_score",
            "hasbled_score",
            "qrisk3_value",
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
            "hasbled_score": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "min": "0",
                    "max": "9",
                    "placeholder": "Enter HAS-BLED score (0-9)",
                }
            ),
            "qrisk3_value": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "min": "0.00",
                    "max": "100.00",
                    "step": "0.01",
                    "placeholder": "Enter QRISK3 percentage (0.00-100.00)",
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
        self.fields["hasbled_score"].help_text = (
            "HAS-BLED score for bleeding risk assessment (0-9). "
            "Higher scores indicate higher bleeding risk."
        )
        self.fields["qrisk3_value"].help_text = (
            "QRISK3 score for cardiovascular risk assessment (0.00-100.00%). "
            "Represents 10-year cardiovascular disease risk percentage."
        )

        # If editing an existing instance, populate the individual contraindication fields
        if self.instance and self.instance.pk and self.instance.contraindication_flags:
            flags = self.instance.contraindication_flags
            self.fields["warfarin_allergy"].initial = flags.get(
                "warfarin_allergy", False
            )
            self.fields["bleeding_disorder"].initial = flags.get(
                "bleeding_disorder", False
            )
            self.fields["pregnancy_status"].initial = flags.get(
                "pregnancy_status", False
            )

    def save(self, commit=True):
        """Convert individual contraindication fields to JSON format."""
        instance = super().save(commit=False)

        # Build contraindication_flags JSON from individual fields
        contraindication_flags = {
            "warfarin_allergy": self.cleaned_data.get("warfarin_allergy", False),
            "bleeding_disorder": self.cleaned_data.get("bleeding_disorder", False),
            "pregnancy_status": self.cleaned_data.get("pregnancy_status", False),
        }

        instance.contraindication_flags = contraindication_flags

        if commit:
            instance.save()
        return instance


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
