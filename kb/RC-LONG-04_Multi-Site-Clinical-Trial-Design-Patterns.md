RC-LONG-04

**Multi-Site Clinical Trial Design Patterns and Lessons Learned**

| **Article ID** | RC-LONG-04 |
|---|---|
| **Domain** | Longitudinal & Repeated Setup |
| **Applies To** | Multi-site longitudinal clinical trials with regulatory oversight, blinding requirements, and quality control workflows |
| **Prerequisite** | RC-LONG-01 — Longitudinal Project Setup; RC-LONG-02 — Repeated Instruments & Events Setup; RC-LONG-03 — Longitudinal Clinical Research Design Patterns; RC-DAG-01 — Data Access Groups |
| **Version** | 1.0 |
| **Last Updated** | 2026-05-08 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-BL-05 — Branching Logic in Longitudinal Projects; RC-AT-09 — @CALCTEXT & @CALCDATE; RC-USER-02 — User Rights and Roles; RC-RAND-01 — Randomization Concepts; RC-AT-08 — @IF Conditional Logic |

---

# 1. Overview

This article documents design patterns, risks, and lessons learned from a complex multi-site longitudinal clinical trial implemented in REDCap. The project enrolled a dual-cohort population (patient + caregiver dyads), collected a comprehensive battery of validated instruments at baseline and four follow-up timepoints over two years, included built-in randomization, and managed safety reporting (SAE/UPIRSO) alongside quality control workflows.

The patterns here are drawn from direct analysis of a production-quality project design. They extend the general content in RC-LONG-03 with specific guidance for trials that involve multiple enrolling sites, regulatory-grade safety reporting, and coordinating-center quality oversight.

---

# 2. Project Structure Overview

The project described in this article has the following characteristics:

- **Type**: Single-arm longitudinal, multi-site
- **Population**: Dual cohort (patient + caregiver), enrolled as dyads
- **Events**: Baseline, 45-day, 6-month, 12-month, 24-month follow-up, and Discontinuation
- **Instrument count**: ~55 instruments, ~319 fields
- **Features active**: Longitudinal mode, repeating instruments, randomization module, Data Access Groups (DAGs) for site separation
- **Surveys**: Disabled (all data entered by study staff)
- **Status at analysis**: Development (not yet in production)

---

# 3. Design Patterns

## 3.1 Dual-Cohort Instrument Organization

When a study enrolls patient-caregiver dyads under a single record, organize instruments by cohort into logical instrument groups. The patient instruments and caregiver instruments should be clearly separated — both in naming (prefix `patient_` vs `caregiver_`) and in event assignment.

**Implementation observed:**

Patient pathway instruments included: screening, contact, call log, scheduled interview date, interview start/end bookends, validated clinical questionnaires (EQ-5D-5L, PROMIS SF, SAQ, TICS, PHQ, ADL, FRAIL, UAB Life Space), medications, MMAS-4, outcomes/hospitalizations, cognitive battery (Craft Story 21, Number Span, Category/Verbal Fluency, Oral Trail Making), 6-Minute Walk, gift card tracking, randomization.

Caregiver pathway instruments included: screening, contact, call log, interview start/end, baseline characteristics, roles questionnaire, FAQ, Caregiver Burden Inventory.

Both cohorts shared: Safety Report (SAE/UPIRSO), Medical Record Abstraction, QC Checklist.

**Pattern: Interview bookend instruments.** Using a dedicated "Interview Start" and "Interview End" instrument at each event creates a natural workflow wrapper. Staff complete "Start" when the interview begins and "End" when it concludes. This allows tracking of interview duration and creates a clear completion signal that downstream QC can verify.

**Trade-off:** Adds two instruments per event and per cohort, increasing total form count noticeably. Worth the investment for studies where interview timing and completeness are monitored.

---

## 3.2 Repeating Instruments for Safety and Communication Logs

Safety adverse event (SAE) forms and contact/call logs should be configured as repeating instruments rather than non-repeating, because their occurrence is unpredictable and unbounded.

**Implementation observed:**

- `safety_report_sae_upirso` set as repeating on all events (baseline through 12-month)
- `patient_call_log` and `caregiver_call_log` set as repeating on all follow-up events

**Custom form labels** were configured on repeating instances to display meaningful identifiers in the Record Status Dashboard. For the SAE form, the label displayed `[ae_site_rpt_status], [ae_site_rpt_date]`. For call logs, the label displayed `[cont_date], [cont_outcome]`. This makes it immediately clear which instance corresponds to which contact attempt without having to open each one.

**Lesson:** Always set custom form labels on repeating instruments. Unlabeled repeating instances are nearly indistinguishable in the dashboard ("Instance 1", "Instance 2", etc.), which makes monitoring and auditing difficult.

---

## 3.3 Multi-Site Configuration via Data Access Groups

For multi-site studies, use Data Access Groups (DAGs) as the primary mechanism for site separation and access control. Beyond their core function of restricting record visibility, DAGs can drive site-specific form behavior through branching logic.

**Implementation observed:**

- Each enrolling site was assigned its own DAG
- Site-specific requirements were enforced by referencing `[record-dag-name]` in branching logic:
  - One site required an additional HIPAA authorization section (shown only when `[record-dag-name]='site_a'`)
  - One site had a caregiver consent requirement not shared by other sites (shown only when `[record-dag-name]='site_b'`)
  - One site had a distinct consent form version, controlled via `@IF([record-dag-name]='site_c', @SHOWCHOICE='80', @HIDECHOICE='80')` to show/hide that version from the consent version dropdown

**Benefit:** A single form can manage multi-site variation without creating site-specific form copies. Version control is simpler — one data dictionary.

**Risks and limitations:**

1. **Scalability ceiling.** This pattern works well for up to roughly 5–6 sites. Beyond that, branching logic across 8+ fields becomes difficult to read and audit. If site expansion is anticipated, document all DAG-conditional fields in a central "site configuration matrix" (a spreadsheet listing each site and each field affected by DAG-based logic).

2. **Caregiver consent scope risk.** If a site-specific requirement (like caregiver consent) becomes applicable at other sites during the study, the branching logic must be manually updated across multiple fields. This is a code-level change requiring careful testing.

3. **DAG name stability.** DAG names used in branching logic must not be changed after deployment. A DAG rename silently breaks all associated branching conditions without any REDCap warning.

---

## 3.4 Role-Based Access Control for Blinded Studies

For studies with blinded roles (e.g., unblinded vs blinded staff, medical monitor vs coordinator), use `[user-role-label]` in branching logic to restrict field visibility by role.

**Implementation observed:**

The medical monitor review section of the SAE form was conditionally displayed using:

```
([user-role-label]='medical monitor' or [user-role-label]='admin' or [user-role-label]='unblinded dcc staff') and [ae_serious]=1 and [ae_category]<>7
```

This ensured that only qualified reviewers could see (and complete) the medical monitor assessment, and only when a serious AE had been reported and it was not a non-safety category.

**Benefit:** Access control is automatic — no manual role check needed before displaying sensitive fields. Preserves blinding and role-appropriate oversight.

**Critical risk — role label fragility.** `[user-role-label]` references the exact display name of the user role as configured in the project's User Rights settings. If a role is renamed (e.g., "medical monitor" → "Medical Monitor" or "med_monitor"), all branching logic referencing the old name silently breaks. The field becomes permanently invisible to everyone.

**Mitigation:**
- Maintain a central document (or a Notes field in a project administration instrument) listing every role name referenced in branching logic
- Treat role renames as a schema change requiring a branching logic audit
- Test role-conditional field visibility after any role configuration change

---

## 3.5 QC Checklist Form Design: Paired Notes on Failure

A Quality Control Checklist instrument that coordinates center staff complete for each record at each event is an effective way to enforce data quality standards programmatically.

**Implementation observed:**

The QC checklist (~112 fields) used a consistent paired-field pattern throughout:

1. A Yes/No or radio question for the QC item (e.g., `qc_consent_uploaded` — "Consent form uploaded to file repository?")
2. A branching notes field that appeared only on failure (e.g., `qc_consent_not_uploaded_note` — visible only when `[qc_consent_uploaded]='0'`)

This pattern was applied to 40+ QC items covering: consent documentation, demographics, insurance, baseline data entry timeliness, questionnaire completion, 6-Minute Walk prerequisites, caregiver screening, medical record abstraction windows, cardiac imaging upload, medication documentation, SAE entry, and final study status.

**Benefit:** The form is uncluttered for passing items (notes fields hidden), but deficiency documentation is captured precisely where it's needed. Reports and dashboards can filter on any QC field to identify problematic records.

**Lesson:** Design QC checklists before study launch, not after. The QC instrument effectively codifies the Study Operations Manual in REDCap. Retrofitting this structure after data collection begins is much harder.

---

## 3.6 Dynamic Visit Window Calculation with @CALCDATE

Use `@CALCDATE` (hidden calculated fields) to compute protocol visit windows from the randomization date, and `@CALCTEXT` to surface those windows as readable text within QC questions.

**Implementation observed:**

Nine hidden system fields in the QC checklist managed the entire medical record abstraction window system:

```
qc_mrbase_close  = @CALCDATE([baseline_arm_1][random_date], 14, 'd')
qc_mr45d_start   = @CALCDATE([baseline_arm_1][random_date], 45, 'd')
qc_mr45d_close   = @CALCDATE([baseline_arm_1][random_date], 66, 'd')
qc_mr6m_start    = @CALCDATE([baseline_arm_1][random_date], 180, 'd')
qc_mr6m_close    = @CALCDATE([baseline_arm_1][random_date], 209, 'd')
qc_mr12m_start   = @CALCDATE([baseline_arm_1][random_date], 365, 'd')
qc_mr12m_close   = @CALCDATE([baseline_arm_1][random_date], 394, 'd')
```

A `@CALCTEXT` field (`pipe_text_mr`) then concatenated the relevant window dates into a readable string (e.g., "2024-03-15 - 2024-04-05") that was piped into QC question labels for coordinators to reference.

An additional `@CALCTEXT` field (`qc_cur_wind_start`) used nested `if()` logic to return the appropriate window start date based on the current event, enabling a single QC form to work across all events without modification.

**Benefit:** Protocol windows are derived automatically from a single source of truth (randomization date). No manual date calculations, no transcription errors. Window changes (e.g., amended protocol) require updating only the `@CALCDATE` offset value.

**Critical risk — cross-event field references.** The `[baseline_arm_1][random_date]` syntax references a field in a specific event from a different event. If the baseline event is renamed, or if `random_date` is renamed or moved, all seven `@CALCDATE` fields and the two `@CALCTEXT` fields break silently — they return blank without any error message.

**Mitigation:**
- Document all cross-event field references explicitly before moving to production
- Treat the randomization date field name and the baseline event name as frozen after first use — add a note in the project documentation
- Test all calculated fields after any schema change

---

## 3.7 Proxy Assessment Instrument Management

When a validated instrument has a proxy version (to be completed by a caregiver or surrogate when the participant cannot self-report), manage the two versions as separate REDCap instruments assigned to overlapping events with branching logic on the eligibility criteria.

**Implementation observed:**

The project included both `eq5d5l` (patient self-report) and `eq5d5l_proxy` (caregiver-reported) instruments. The proxy version was assigned to follow-up events (45-day through 24-month) but not to baseline — reflecting the protocol logic that proxy assessment is only applicable after baseline eligibility is established. A Callahan Screener instrument at each follow-up event presumably determined which version applied.

**Lesson:** Plan the switching logic between self-report and proxy versions before instrument design begins. Coordinate the Callahan or similar screener output (the switching criterion) with the branching logic on both instruments so only one version is active per record per event.

---

## 3.8 Screening Workflow Design

The screening instrument is often the most complex form in a clinical trial because it captures eligibility determination, consent documentation, and refusal tracking all in one place.

**Implementation observed:**

The patient screening form included:

- A structured eligibility assessment (inclusion criteria met + no exclusion criteria)
- UBACC cognitive assessment to determine consent capacity, with conditional consent discussion requirement
- A consent outcome field with a 9-option radio (Obtained / Refused / Language barrier / Temporary inability / Did not approach / Unwilling / Already enrolled / Other / Unknown) — enabling granular analysis of non-enrollment reasons
- A cascading consent documentation checklist (date, time, staff, version, language, attestation, patient copy, upload) only shown when consent was obtained
- Site-specific HIPAA authorization field shown only for the relevant site

**Lesson:** Never use a simple Yes/No for consent outcome. A structured refusal reason taxonomy is essential for CONSORT flow diagrams, IRB reporting, and retention analysis. Build this into the screening form from the start.

---

# 4. Identified Risks and Mitigations

## 4.1 Missing Time Validation on Safety Event Onset

**Risk:** The SAE form collected adverse event onset date and time, but no `time` field validation was applied to the time field — only `date_mdy` was used for the date portion. For regulatory-grade safety reporting, precise onset time can be required for causality assessment timelines.

**Mitigation:** Apply `time` (HH:MM) validation to any field that collects event onset time on a safety reporting form. Add a note to the field label if the format expected is different (e.g., 24-hour vs 12-hour).

---

## 4.2 Undocumented Scoring Algorithms

**Risk:** The UBACC (University of California Brief Assessment of Capacity to Consent) screener appeared in the screening form with a score field and a category outcome, but no `@CALCTEXT` formula was present — the score appeared to require manual calculation or entry. This creates a data entry error risk and makes auditing difficult.

**Mitigation:** Wherever a validated instrument has a defined scoring algorithm, implement it as a `@CALCTEXT` or calculated field. If manual scoring is required by protocol (e.g., clinician judgment), annotate the field label with the scoring guide and mark the field as requiring source document verification in the QC checklist.

---

## 4.3 SQL Dropdown Fragility

**Risk:** Staff selection dropdowns used SQL field type with a multi-table JOIN query to filter the user list by site and role. This is sophisticated but fragile: if underlying field names change, the SQL query breaks without any REDCap warning. SQL queries in REDCap are also not visible in the standard data dictionary view and require admin access to review.

**Mitigation:** Document all SQL field queries in a separate reference document. Treat SQL field queries as code — subject to version control and change review. Test SQL dropdowns when any user, role, or DAG configuration changes.

---

## 4.4 Action Tag Ordering Convention

**Risk:** Action tags were not applied in a consistent order across fields (e.g., `@HIDDEN @CALCDATE` in some places, `@CALCDATE @HIDDEN` in others). While REDCap generally processes action tags independently, inconsistent ordering creates cognitive overhead during audits and may produce unexpected behavior in edge cases involving tag interactions.

**Mitigation:** Establish and document a standard action tag ordering convention before project build begins. A reasonable convention is: visibility tags first (`@HIDDEN`, `@READONLY`), then value tags (`@DEFAULT`, `@CALCTEXT`, `@CALCDATE`), then display-modifying tags (`@IF`, `@SHOWCHOICE`, `@HIDECHOICE`). Apply this consistently across the data dictionary.

---

# 5. Best Practices Observed

The following design choices in the analyzed project represent strong implementation patterns worth replicating:

**Paired QC notes fields.** Every QC item had a paired notes field visible only on failure. Efficient and systematic.

**Custom form labels on repeating instruments.** Made the Record Status Dashboard readable for SAE and call log monitoring.

**Calculated visit windows.** Single source of truth for protocol windows; eliminates manual calculation errors.

**Event-based field visibility in shared forms.** Using `[event-name]` branching in a single QC form to serve five distinct events reduces maintenance burden versus separate per-event forms.

**Role-gated medical monitor section.** Automated enforcement of review role separation in SAE reporting is more reliable than relying on staff to self-enforce.

**Granular consent refusal taxonomy.** Nine-option refusal reason radio enables detailed CONSORT reporting.

**Progressive disclosure for adverse event severity.** The medical monitor risk assessment field appeared only when: AE was serious, causality was attributed, and the event was unexpected — exactly when the assessment is relevant. This reduces form burden for low-risk AE entries.

---

# 6. Common Questions

**Q: How many sites can DAG-based branching realistically support before it becomes unmanageable?**

Five to six sites is a reasonable upper bound before the branching logic becomes difficult to read and audit in a standard data dictionary. Beyond that, consider whether site-specific requirements can be harmonized (eliminating branching), or whether a separate "site configuration" tracking instrument could centralize site parameters that other forms reference.

**Q: We have both patient and caregiver cohorts in one record. Should they share instruments or have separate ones?**

Separate instruments are strongly preferred. Sharing a single instrument between two different data sources (patient vs. caregiver) creates ambiguity about who completed which fields and makes export/analysis harder. Duplicate the instrument and prefix field names clearly (e.g., `pt_` vs. `cg_`).

**Q: Should the QC checklist be one form or several?**

For large studies, a single QC checklist per event can exceed 100 fields — which is functional but requires scrolling and can feel overwhelming to coordinators. Consider splitting by domain (e.g., Consent QC, Interview QC, Medical Records QC) as separate instruments all assigned to the same event. This also makes it easier to assign QC review tasks to different team members.

**Q: How do we handle protocol amendments that change visit windows?**

If windows are calculated via `@CALCDATE` offsets from randomization date, a protocol amendment changing a visit window requires only updating the numeric offset in the relevant calculated field. For records enrolled before the amendment, the new calculation applies immediately (REDCap recalculates on load). If amendment-specific windows are needed for pre-amendment records, this becomes more complex and may require a separate "amendment date" reference field and conditional `@CALCTEXT` logic.

---

# 7. Related Articles

- RC-LONG-01 — Longitudinal Project Setup
- RC-LONG-02 — Repeated Instruments and Events Setup
- RC-LONG-03 — Longitudinal Clinical Research Design Patterns
- RC-AT-09 — Action Tags: @CALCTEXT & @CALCDATE
- RC-AT-08 — Action Tags: @IF Conditional Logic
- RC-BL-05 — Branching Logic in Longitudinal Projects
- RC-USER-02 — User Rights: Adding Users and Managing Roles
- RC-RAND-01 — Randomization Concepts
- RC-DAG-01 — Data Access Groups
