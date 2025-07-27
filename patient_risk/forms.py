"""Forms for the patient_risk app."""

from django import forms

from patient.models import Person

from .models import PatientRiskAssessment


class PatientRiskAssessmentForm(forms.ModelForm):
    """Form for creating and editing Patient Risk Assessments."""

    # Individual contraindication fields that will be converted to JSON
    active_bleeding = forms.BooleanField(
        required=False,
        label="Active bleeding",
        help_text="Patient has active bleeding or bleeding disorder",
    )
    recent_stroke = forms.BooleanField(
        required=False,
        label="Recent hemorrhagic stroke",
        help_text="Recent hemorrhagic stroke or intracranial hemorrhage",
    )
    high_bleeding_risk = forms.BooleanField(
        required=False,
        label="High bleeding risk",
        help_text="Patient has high bleeding risk factors",
    )
    patient_refusal = forms.BooleanField(
        required=False,
        label="Patient refusal",
        help_text="Patient refused anticoagulation therapy",
    )
    renal_impairment = forms.BooleanField(
        required=False,
        label="Severe renal impairment",
        help_text="End-stage renal disease or severe kidney impairment",
    )
    hepatic_impairment = forms.BooleanField(
        required=False,
        label="Hepatic impairment",
        help_text="Liver disease or hepatic impairment",
    )
    drug_interactions = forms.BooleanField(
        required=False,
        label="Drug interactions",
        help_text="Significant drug interactions with anticoagulants",
    )
    surgical_risk = forms.BooleanField(
        required=False,
        label="Upcoming surgery",
        help_text="Recent or upcoming surgery with bleeding risk",
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
            self.fields["active_bleeding"].initial = flags.get("active_bleeding", False)
            self.fields["recent_stroke"].initial = flags.get("recent_stroke", False)
            self.fields["high_bleeding_risk"].initial = flags.get(
                "high_bleeding_risk", False
            )
            self.fields["patient_refusal"].initial = flags.get("patient_refusal", False)
            self.fields["renal_impairment"].initial = flags.get(
                "renal_impairment", False
            )
            self.fields["hepatic_impairment"].initial = flags.get(
                "hepatic_impairment", False
            )
            self.fields["drug_interactions"].initial = flags.get(
                "drug_interactions", False
            )
            self.fields["surgical_risk"].initial = flags.get("surgical_risk", False)

    def save(self, commit=True):
        """Convert individual contraindication fields to JSON format."""
        instance = super().save(commit=False)

        # Build contraindication_flags JSON from individual fields
        contraindication_flags = {
            "active_bleeding": self.cleaned_data.get("active_bleeding", False),
            "recent_stroke": self.cleaned_data.get("recent_stroke", False),
            "high_bleeding_risk": self.cleaned_data.get("high_bleeding_risk", False),
            "patient_refusal": self.cleaned_data.get("patient_refusal", False),
            "renal_impairment": self.cleaned_data.get("renal_impairment", False),
            "hepatic_impairment": self.cleaned_data.get("hepatic_impairment", False),
            "drug_interactions": self.cleaned_data.get("drug_interactions", False),
            "surgical_risk": self.cleaned_data.get("surgical_risk", False),
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
