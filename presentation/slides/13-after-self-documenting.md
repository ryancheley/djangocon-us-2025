# After - Self-Documenting Models

.large-code[
```python
class PatientRiskAssessment(models.Model):
    chads_score = models.IntegerField(
        db_comment="CHA2DS2-VASc stroke risk (0-9). "
                  "≥2 indicates anticoagulation consideration. "
                  "Per 2010 ESC Guidelines."
    )
```
]

--

```python
    hasbled_score = models.IntegerField(
        db_comment="HAS-BLED bleeding risk (0-9). "
                  "≥3 indicates high bleeding risk. "
                  "FDA guidance 2019."
    )
```

--

.success-point[
**Result:** Context for ETL dimension creation and report development
]
