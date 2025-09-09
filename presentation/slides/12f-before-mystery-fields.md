# Before Comments

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

- be real with me here
- even the original web developer
- who wrote this
- won't remember what qrisk3_value means in six months
