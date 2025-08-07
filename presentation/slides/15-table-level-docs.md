# Complete Context - Table-Level Documentation

.large-code[

```python
class PatientRiskAssessment(models.Model):
    chads_score = models.IntegerField(
        db_comment="CHA2DS2-VASc stroke risk (0-9)..."
    )

    ...

    class Meta:
        db_table_comment = ("Cardiovascular risk calculations per "
                           "Joint Commission PC-03. Updated nightly "
                           "via clinical_calc_job. Owner: CardioTeam")
```

]

.success-point[
**Table Level Documention:** We have a what, how, and a who for this table!
]
