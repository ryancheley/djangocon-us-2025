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


.pain-point[
**Mystery Fields**
]

???

What do these cryptic names actually mean? This is the **root** of our problem - the database itself contains no business context.
