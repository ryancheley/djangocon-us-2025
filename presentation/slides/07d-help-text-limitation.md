# The `help_text` Limitation

.xlarge-code[

```python
class PatientRiskAssessment(models.Model):
    chads_score = models.IntegerField(
        help_text="CHAD2SC-VASc score risk"
        "for stroke risk assessment (0-9)."
        "Higher score indiccates higher"
        "risk score."
    )
```

]

.pain-point[
    **Problem**
]

???

- good tool
- wrong audience.
