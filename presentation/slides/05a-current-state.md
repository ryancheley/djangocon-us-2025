# Current State

.xlarge-code[

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

This is what our database schema looks like today. Clean, functional, but completely opaque.

Look at these field names: hasbled_score, qrisk3_value, contraindication_flags , chads_score. If you're not a cardiologist, these mean absolutely nothing.

A Database Administrator (DBA) looking at this table has no idea what these calculate or why they matter.

--

.pain-point[
**Mystery Fields**
]

???

What do these cryptic names actually mean? This is the **root** of our problem - the database itself contains no business context.
