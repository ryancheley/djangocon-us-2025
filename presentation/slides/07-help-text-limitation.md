# The `help_text` Limitation

.large-code[

```python
# help_text - UI focused
class PatientRiskAssessment(models.Model):
    chads_score = models.IntegerField(
        help_text="Enter the patient's CHA2DS2-VASc score"
    )
```

]

--

**Problem:** Only visible in Django admin forms

???

Many Django developers think help_text solves this problem. It doesn't.

help_text is designed for end users filling out forms. It's UI-focused guidance.

The problem is it's only visible in Django admin forms. If you're a DBA using pgAdmin, or a data analyst using Tableau, or an ETL developer building data pipelines - you'll never see this help text.

It's the right tool for the wrong audience.
