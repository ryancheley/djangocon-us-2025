# What This Generates

.large-code[

```sql
-- PostgreSQL output

CREATE TABLE patient_risk_patientriskassessment (
    chads_score INTEGER NOT NULL
);
COMMENT ON COLUMN patient_risk_patientriskassessment.chads_score IS
'CHA2DS2-VASc stroke risk score calculation';
```

]

--

.success-point[
**Result**
]

???

Anyone querying the database sees the documentation!
