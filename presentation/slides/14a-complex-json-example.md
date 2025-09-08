# JSON Fields

.xlarge-code[
```python
contraindication_flags = models.JSONField(
    db_comment="Clinical contraindications "
    "per CMS-134v8. "
    "Keys: warfarin_allergy, bleeding_disorder, "
    "pregnancy_status. Boolean values only."
)
```

]

--

.success-point[
**Why This Matters**
]

???

- The ETL developer knows the JSON structure
- They can turn these keys into unique columns
- ease report / dashboard development
