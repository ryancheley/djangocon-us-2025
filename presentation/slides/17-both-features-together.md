# Both Features Working Together

.code[
```python
# The complete picture
class PatientRiskAssessment(models.Model):
    chads_score = models.IntegerField(
        help_text="Enter score 0-9 based on patient risk factors",  # For clinicians
        db_comment="CHA2DS2-VASc stroke risk (0-9). ≥2 indicates "
                  "anticoagulation per ESC 2010. Regulatory: CMS-134v8"  # For everyone else
    )
```
]

--

.success-point[
**Best Practice:** Use both - they serve different audiences
]
