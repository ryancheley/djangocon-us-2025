# Current State

.large-code[

```sql
-- What our database looks like today
CREATE TABLE patient_risk_patientriskassessment (
    id INTEGER PRIMARY KEY,
    hasbled_score INTEGER,
    qrisk3_value DECIMAL(5,2),
    contraindication_flags JSON,
    chads_score INTEGER
);
```

]

???

A Database Administrator (DBA) looking at this table likely has no idea what these are or why they matter.
