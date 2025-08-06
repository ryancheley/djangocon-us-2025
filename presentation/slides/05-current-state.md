# Current State - EHR Database Schema

.large-code[
```sql
-- What our database looks like today
CREATE TABLE patient_risk_patientriskassessment (
    id INTEGER PRIMARY KEY,
    chads_score INTEGER,
    hasbled_score INTEGER,
    qrisk3_value DECIMAL(5,2),
    contraindication_flags JSON,
    last_calc_date TIMESTAMP
);
```
]

--

.pain-point[
**Mystery Fields:** What do these cryptic names actually mean?
]

???

This is what our database schema looks like today. Clean, functional, but completely opaque.

Look at these field names: chads_score, hasbled_score, qrisk3_value. If you're not a cardiologist, these mean absolutely nothing.

A DBA looking at this table has no idea what these calculate or why they matter.

This is the root of our problem - the database itself contains no business context.
