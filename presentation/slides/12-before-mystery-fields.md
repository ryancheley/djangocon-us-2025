# Before - The Mystery Fields

???

ETL and Report developers have no idea what these fields represent! And if we're being honest, even the web developer won't know / remember in a few days / weeks!

Let's do a before and after comparison showing how the `db_comment` can help!

--

.large-code[

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

--

.pain-point[
**Problems**
]

--

???

Here we see some typical Django model code.

Clean, functional, but tells us nothing about the business logic.

The ETL developer looks at this and has no idea what chads_score represents. Is it a count? A percentage? A risk level?

The report developer can't build meaningful dashboards without context.

And honestly - be real with me here - even the original web developer who wrote this won't remember what qrisk3_value means in six months!
