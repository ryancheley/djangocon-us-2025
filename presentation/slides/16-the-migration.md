# The Migration

.large-code[
```python
# Generated migration
operations = [
    migrations.AlterField(
        model_name='patientriskassessment',
        name='chads_score',
        field=models.IntegerField(
            db_comment='CHA2DS2-VASc stroke risk (0-9)...'
        ),
    ),
]
```
]

--

.success-point[
**Safe Migration:** Comments are metadata - no data loss
]
