# Django 4.2's `db_comment`

* Released on April 3, 2023

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

???

- The magic happens with the migration
- it puts this comment directly into the database
- where anyone can see it
