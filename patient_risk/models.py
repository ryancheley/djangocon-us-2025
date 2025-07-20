from django.db import models
from django.utils import timezone

from patient.models import Person


class PatientRiskAssessment(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    chads_score = models.IntegerField(
        help_text="CHADS2-VASc score (0-9) for stroke risk assessment"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Patient Risk Assessment"
        verbose_name_plural = "Patient Risk Assessments"
        ordering = ["-created_at"]
        unique_together = ("person", "chads_score")

    def __str__(self):
        return f"Risk Assessment for {self.person.full_name} - CHADS Score: {self.chads_score}"
