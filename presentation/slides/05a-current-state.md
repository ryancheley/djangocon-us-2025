# Current State

--

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
OK, let's jump to what our current Database view might look like. It's Clean, functional, but completely opaque.
