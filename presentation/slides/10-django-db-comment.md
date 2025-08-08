# Django 4.2's `db_comment`

.xlarge-code[

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

Here's the solution: Django 4.2 introduced the db_comment parameter.

This simple addition to your field definition puts documentation directly into the database schema.

Notice how clean this is - just add db_comment with a description of what the field contains.

The magic happens when Django generates the migration - it puts this comment directly into the database where anyone can see it.


--

.success-point[
**Solution**
]

???

**Documentation lives in the database itself!**
