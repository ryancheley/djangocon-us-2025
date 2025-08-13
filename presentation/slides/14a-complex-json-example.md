# Complex Example - JSON Fields

.large-code[

```python

...

contraindication_flags = models.JSONField(
    db_comment="Clinical contraindications per CMS-134v8. "
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

The ETL developer knows the JSON structure without digging through Django code. They can turn these keys into unique columns to make it easier to report on them by the Report Developers
