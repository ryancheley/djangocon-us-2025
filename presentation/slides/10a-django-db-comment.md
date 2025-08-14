# Django 4.2's `db_comment`

--

`db_comment` was introduced in Django 4.2 which was released on April 3, 2023

???

Quick show of hands, how many of you have used this feature?

--

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
