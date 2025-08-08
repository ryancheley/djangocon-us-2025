# The `help_text` Limitation

.large-code[

```python
# help_text - UI focused
class PatientRiskAssessment(models.Model):
    chads_score = models.IntegerField(
        help_text="Enter score 0-9 based on patient risk factors"
    )
```

]

--

**Problem**

???

You might think help_text solves this problem. It doesn't.

help_text is designed for end users filling out forms. It's UI-focused guidance.

The problem is it's only visible in forms, either in the Admin or the Front End. If you're a DBA using pgAdmin, or a data analyst using Tableau, or an ETL developer building data pipelines - you'll never see this help text.

It's the right tool for the wrong audience.
