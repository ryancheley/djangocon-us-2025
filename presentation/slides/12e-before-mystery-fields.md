# Before - The Mystery Fields

.xlarge-code[

```python
# patient_risk/models.py
class PatientRiskAssessment(models.Model):
    hasbled_score = models.IntegerField()
    qrisk3_value = models.DecimalField(
        max_digits=5, decimal_places=2)
    contraindication_flags = models.JSONField()
    chads_score = models.IntegerField()
```

]

???

- can't build meaningful dashboards without context
