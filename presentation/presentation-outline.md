# Django `db_comment` Presentation Outline - Final Form

## 25 Minutes Total

### Opening Hook (3 minutes)

**Slide 1: "The Cross-Team Confusion"**

- Slack thread: Developer adds new field → ETL developer needs to understand it → Report developer needs context
- ETL developer looking at database schema with cryptic field names
- **Pain point:** "What does `chads_score` actually calculate for this new dimension?"

**Slide 2: The Real Cost**

- ETL pipeline delays waiting for field clarification
- Report development blocked on dimension requirements
- Developer productivity loss across teams
- Regulatory compliance challenges

### Problem Definition (3 minutes)

**Slide 3: Current State - EHR Database Schema**


    -- What our database looks like today
    CREATE TABLE patient_risk_patientriskassessment (
        id INTEGER PRIMARY KEY,
        chads_score INTEGER,
        hasbled_score INTEGER,
        qrisk3_value DECIMAL(5,2),
        last_calc_date TIMESTAMP
    );


**Slide 4: The Documentation Gap**

- Code comments ≠ Database documentation
- Wiki pages get stale
- Tribal knowledge doesn't scale
- Regulatory auditors need field-level documentation

### "Why Not Just `help_text`?" (4 minutes)

**Slide 5: The `help_text` Limitation**


    # help_text - UI focused
    class PatientRiskAssessment(models.Model):
        chads_score = models.IntegerField(
            help_text="Enter the patient's CHA2DS2-VASc score"
        )


**Slide 6: Different Audiences, Different Needs**

|  Stakeholder |  Needs |  `help_text` |  `db_comment` |
| ---- | ---- | ---- | ----  |
|  End Users |  Form guidance |  ✅ |  ❌ |
|  Developers |  Field purpose |  ❌* |  ✅ |
|  DBAs |  Schema understanding |  ❌ |  ✅ |
|  Auditors |  Compliance documentation |  ❌ |  ✅ |
|  Data Analysts |  Direct DB access context |  ❌ |  ✅ |

*Only if they're looking at Django admin

**Slide 7: Where `help_text` Falls Short**

- **Data team using Metabase/Tableau:** Can't see `help_text`
- **Database migrations:** No context for schema changes
- **Legacy system integration:** External tools need field documentation
- **Regulatory audits:** Auditors examine database directly, not Django admin
- **Cross-team collaboration:** ETL developers building dimensions without field context

### Solution Introduction (3 minutes)

**Slide 8: Django 4.2's `db_comment`**


    class PatientRiskAssessment(models.Model):
        chads_score = models.IntegerField(
            db_comment="CHA2DS2-VASc stroke risk score calculation"
        )


**Slide 9: What This Generates**


    -- PostgreSQL output
    CREATE TABLE patient_risk_patientriskassessment (
        chads_score INTEGER NOT NULL
    );
    COMMENT ON COLUMN patient_risk_patientriskassessment.chads_score IS
    'CHA2DS2-VASc stroke risk score calculation';


### Code Walkthrough (8 minutes)

**Slide 10: Before - The Mystery Fields**


    # patient_risk/models.py
    class PatientRiskAssessment(models.Model):
        chads_score = models.IntegerField()
        hasbled_score = models.IntegerField()
        qrisk3_value = models.DecimalField(max_digits=5, decimal_places=2)
        contraindication_flags = models.JSONField()


**Slide 11: After - Self-Documenting Models**


    class PatientRiskAssessment(models.Model):
        chads_score = models.IntegerField(
            db_comment="CHA2DS2-VASc stroke risk (0-9). "
                      "≥2 indicates anticoagulation consideration. "
                      "Per 2010 ESC Guidelines."
        )
        hasbled_score = models.IntegerField(
            db_comment="HAS-BLED bleeding risk (0-9). "
                      "≥3 indicates high bleeding risk. "
                      "FDA guidance 2019."
        )


**Slide 12: Complex Example - JSON Fields**


    contraindication_flags = models.JSONField(
        db_comment="Clinical contraindications per CMS-134v8. "
                  "Keys: warfarin_allergy, bleeding_disorder, "
                  "pregnancy_status. Boolean values only."
    )


**Slide 13: Complete Context - Table-Level Documentation**


    class PatientRiskAssessment(models.Model):
        chads_score = models.IntegerField(
            db_comment="CHA2DS2-VASc stroke risk (0-9)..."
        )
        hasbled_score = models.IntegerField(
            db_comment="HAS-BLED bleeding risk (0-9)..."
        )

        class Meta:
            db_table_comment = ("Cardiovascular risk calculations per "
                               "Joint Commission PC-03. Updated nightly "
                               "via clinical_calc_job. Owner: CardioTeam")


**Slide 14: The Migration**


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


**Slide 15: Both Features Working Together**


    # The complete picture
    class PatientRiskAssessment(models.Model):
        chads_score = models.IntegerField(
            help_text="Enter score 0-9 based on patient risk factors",  # For clinicians
            db_comment="CHA2DS2-VASc stroke risk (0-9). ≥2 indicates "
                      "anticoagulation per ESC 2010. Regulatory: CMS-134v8"  # For everyone else
        )


### Real-World Impact (2 minutes)

**Slide 16: Database Administrator View**

- Screenshot of pgAdmin showing column comments
- How DBAs can now understand fields without calling developers

**Slide 17: Measurable Results**

- Developer onboarding: 3 weeks → 1 week
- Regulatory audit prep: 40 hours → 15 hours
- Production incidents from field confusion: 3 → 0

### Takeaways (2 minutes)

**Slide 18: Start Today - 3 Steps**

1. **Audit:** Identify your top 10 confusing fields
2. **Document:** Add `db_comment` with business context + compliance notes
3. **Standardize:** Update code review templates

**Slide 19: Resources**

- GitHub repo: `github.com/yourhandle/django-db-comments-patient-risk`
- Django docs reference
- Healthcare-specific comment templates
* * *

## Key Presentation Notes:

- **App name:** `patient_risk` (following Django underscore convention)
- **Total slides:** 19 slides for 25 minutes
- **Core message:** `db_comment` serves different stakeholders than `help_text`
- **Healthcare angle:** Regulatory compliance and patient safety throughout
- **Practical focus:** Real code examples, measurable outcomes, immediate next steps
