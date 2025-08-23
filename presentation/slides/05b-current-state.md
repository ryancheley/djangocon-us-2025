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

Look at these field names: hasbled_score, qrisk3_value, contraindication_flags , chads_score.
I work in healthcare and these aren't fields that I'm aware of.
You would likely wouldn't know about them or their meaning unless you're not a cardiologist.
