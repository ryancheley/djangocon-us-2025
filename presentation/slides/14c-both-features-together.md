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

The help text let's the user know what the range should be ... but we should still have field level validation, right 😉

Use both - they serve different audiences
