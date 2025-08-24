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

- help_text is for end users
- It's UI-focused guidance
