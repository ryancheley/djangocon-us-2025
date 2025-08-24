# After - Self-Documenting Models

.xlarge-code[
```python
    hasbled_score = models.IntegerField(
        db_comment="HAS-BLED bleeding "
                   "risk (0-9). ≥3 indicates "
                   "high bleeding risk. "
                   "FDA guidance 2019."
    )
```
]
--

.success-point[
**Result**
]

???

- Context
- for ETL
- report development
