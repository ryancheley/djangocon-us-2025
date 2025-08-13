# Complete Context - Table-Level Documentation

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

--

.success-point[
**Table Level Documention**
]

???

We have a what, and a who for this table!

--

What is this table about?

--

Who is the point of contact?
