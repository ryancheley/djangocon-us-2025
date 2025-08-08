# Complete Context - Table-Level Documentation

??

We may know more about the fields, but do we know as much as we can about the table that will hold these fields? Not yet, but we can. Also introduced in 4.2 was the `db_table_comment`


--

.large-code[

```python
class PatientRiskAssessment(models.Model):

    ...

    class Meta:
        db_table_comment = ("Cardiovascular risk "
                            "calculations per "
                            "Joint Commission PC-03. "
                            "Owner: CardioTeam@example.com")
```

]

.success-point[
**Table Level Documention**
]

???

We have a what, and a who for this table!
