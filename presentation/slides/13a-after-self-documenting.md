# After

.xlarge-code[

```python
class PatientRiskAssessment(models.Model):
    chads_score = models.IntegerField(
        db_comment="CHA2DS2-VASc stroke "
                "risk (0-9). "
                "≥2 indicates "
                "anticoagulation consideration. "
                "Per 2010 ESC Guidelines."
    )
    ...

```

]
