# What This Generates

.xlarge-code[

```sql
COMMENT ON COLUMN
  patient_risk_patientriskassessment.chads_score IS
  'CHA2DS2-VASc stroke risk (0-9). ' ||
  '≥2 indicates anticoagulation consideration. ' ||
  'Per 2010 ESC Guidelines.';
```

]

--

.success-point[
**Result**
]

???

Anyone querying the database sees the documentation!
