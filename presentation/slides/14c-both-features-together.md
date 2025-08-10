# Both Features Working Together

--

.large-code[

```python
# The complete picture
class PatientRiskAssessment(models.Model):
    chads_score = models.IntegerField(
        help_text="Enter score 0-9 based "
            "on patient risk factors",  # For clinicians
        db_comment="CHA2DS2-VASc stroke"
            " risk (0-9). ≥2 indicates "
            "anticoagulation per ESC 2010."
            "Regulatory: CMS-134v8"  # For everyone else
    )
```

]

--

.success-point[
**Best Practice**
]

???

The help text let's the user know what the range should be ... but we should still have field level validation, right 😉

Use both - they serve different audiences
