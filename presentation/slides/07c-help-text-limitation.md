# The `help_text` Limitation

.xlarge-code[

```python
# help_text - UI focused
class PatientRiskAssessment(models.Model):
    chads_score = models.IntegerField(
        help_text="Enter score 0-9 based"
        "on patient risk factors"
    )
```

]

.pain-point[
    **Problem**
]

???

The problem is it's only visible in forms, either in the Admin or the Front End. If you're a DBA using pgAdmin, or a data analyst using Tableau, or an ETL developer building data pipelines - you'll never see this help text.
