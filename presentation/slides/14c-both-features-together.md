# Both Features Working Together

--

.xlarge-code[

```python
# The complete picture
class PatientRiskAssessment(models.Model):
    chads_score = models.IntegerField(
        help_text=" ... ",  # For Data Entry Users
        db_comment=" ... "  # For dB Users
    )
```

]

--

.success-point[
**Best Practice**
]

???

- Use both
- serve the intended audience
