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

Let's do a before and after comparison showing how the `db_comment` can help!
