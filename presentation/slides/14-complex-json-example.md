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

Data analysts know the JSON structure without digging through code
