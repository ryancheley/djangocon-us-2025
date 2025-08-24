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

- only visible in forms
- DBA using pgAdmin
- a data analyst using Vix Tool
- an ETL developer building data pipelines
- you'll never see this help text.
