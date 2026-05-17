---
id: RC-DSGN-01
title: REDCap Project Design Best Practices
domain: Project Design Best Practices
applies_to:
- All REDCap projects
- all REDCap project designers and reviewers
prerequisites:
- None
version: '1.3'
last_updated: '2026-05-11'
related:
- id: RC-FD-08
  title: 'Data Dictionary: Column Reference & Advanced Techniques'
- id: RC-LONG-01
  title: Longitudinal Project Setup
- id: RC-LONG-02
  title: Repeated Instruments & Events Setup
- id: RC-OPS-01
  title: Using REDCap as an Operational Request Management System
tags:
- project design best practices
---

# 1. Overview

This article documents recommended best practices for REDCap project design. The conventions here reflect patterns that tend to produce cleaner forms, more maintainable data dictionaries, and fewer data quality problems in practice.

These are defaults, not mandates. Individual projects may deviate when there is a good reason, but deviations should be intentional and documented, not accidental.

**How to use this guide:**

- **Project designers** — review this before building a new instrument. The conventions exist because they reduce common mistakes and create a more consistent experience for data entry users and analysts.
- **Reviewers** — use this as a checklist when reviewing a new data dictionary or instrument design before a project goes into production.

---

# 2. Field Alignment (Column N — Custom Alignment)

REDCap supports four alignment codes: `LH`, `LV`, `RH`, and `RV`. See RC-FD-08 Section 5.12 for a full explanation of what each code does visually.

The short version:
- **L (Left)** = field spans full page width
- **R (Right)** = field is approximately half-width (right side of page)
- **H (Horizontal)** = label and input are side by side
- **V (Vertical)** = label sits above the input

The default when the column is left blank is `RV`.

## 2.1 Notes fields (`notes` field type)

**Best practice: use `LH` or `LV`**

A `notes` field with `RH` or `RV` alignment renders at roughly half the page width, which makes the text area cramped and difficult to type in. Setting alignment to `LH` or `LV` gives the text area the full page width.

There is rarely a good reason to use a half-width notes field. If you are using one, consider whether a single-line `text` field would be more appropriate.

## 2.2 Radio and checkbox fields

**Best practice: `LV` for longer lists, `LH` for short lists**

The Vertical/Horizontal component controls whether answer choices are stacked (V) or displayed in a single row (H). As a rule of thumb:

- 2–4 short choices → `LH` (horizontal, full width) reads cleanly
- 5 or more choices, or long choice labels → `LV` (vertical, full width) is easier to scan

The Left/Right component controls which side of the page choices appear on. Left (`L`) is generally preferred as it aligns with natural reading direction and gives more visual space.

## 2.3 Text, dropdown, yesno, truefalse

**Best practice: leave blank (accept `RV` default) unless there is a layout reason to change**

These field types are compact and the width difference between Left and Right alignment is less impactful than with `notes` fields. Accept the default unless you are deliberately composing a specific layout.

## 2.4 Consistency within an instrument

**Best practice: avoid mixing Left and Right fields in the same section without a clear layout purpose**

Alternating between full-width and half-width fields creates a visually fragmented form. If you are setting alignment on any field, consider whether the surrounding fields should also be aligned consistently.

---

# 3. Project Structure

## 3.1 Do not use longitudinal mode if each form is only used once

**Best practice: use longitudinal mode only when instruments are repeated across multiple events**

Longitudinal mode is designed for studies where participants complete the same instruments at multiple time points (e.g., baseline, month 3, month 6). If your project has multiple forms but each form is used at a single point in time (e.g., a Screening form, an Enrollment form, and a Follow-up form — each completed once), a classic (non-longitudinal) project achieves the same result with less configuration overhead.

Using longitudinal mode for a single-arm, single-instance-per-form project adds unnecessary complexity: event setup, event-scoped branching logic syntax, and a more confusing record status dashboard — with no functional benefit.

**Use longitudinal mode when:**
- The same instrument is completed by the same participant at more than one time point, OR
- You need to track scheduling windows, multiple arms, or event-based branching logic

**Use classic mode when:**
- Each instrument is completed exactly once per participant, regardless of how many instruments exist

**Exception:** Some institutions use longitudinal mode for purely structural reasons (e.g., to use repeated instruments without repeating events). If you have a specific architectural reason, document it in the project notes.

---

# 4. Field Notes vs. Field Annotations

## 4.1 Field Note (Column G) — for data entry users only

**Best practice: use the Field Note for short, user-facing clarifications about how to fill in the field**

The Field Note appears below the variable on the form and is visible to anyone completing the instrument — data entry staff and survey participants alike. Use it to answer the question the user is likely to ask at the moment they see the field.

Common uses:
- Units of measure (e.g., `mg/L`, `mmol/mol`, `kg`)
- Date format reminders (e.g., `YYYY-MM-DD`)
- Scope clarifications (e.g., `Include prescribed medications only`)
- Range expectations (e.g., `Normal range: 4.0–11.0`)

Keep it brief. A Field Note that runs to multiple sentences will be ignored. If the field needs more explanation than a line or two, consider whether the instrument design or the field label should be doing more of that work.

## 4.2 Field Annotation (Column R) — for designers only

**Best practice: use the Field Annotation box for notes intended for other project designers, not for data entry users**

Field Annotation content is visible only in the Data Dictionary and the Online Designer — it is never shown on the form. This makes it the right place for:
- Design rationale (e.g., `Mapped to variable X in the source dataset`)
- Outstanding questions or to-dos (e.g., `Confirm unit with PI before go-live`)
- Coding notes (e.g., `Raw value 99 = missing per protocol`)

Field Annotations can be combined with action tags in the same cell. When doing so, put the plain-text note first and the action tags after, separated by a space or line break. Action tags always begin with `@` and are not affected by surrounding text.

Example annotation cell containing both a note and action tags:
```
Confirm unit with PI. @HIDDEN-SURVEY @READONLY
```

> **Important:** Never put user-facing instructions in the Field Annotation — they will not be seen by the person filling in the form. Use the Field Note (Column G) for anything the data entry user needs to read.

---

# 5. Branching Logic Design

## 5.1 Do not hardcode user identifiers in branching logic

**Best practice: never use hardcoded usernames, NetIDs, or system IDs as branching logic conditions**

A common pattern for hiding admin-only fields is to write branching logic that checks whether the currently logged-in user matches a known identifier:

```
[reviewer_field] = 'abc123' or [reviewer_field] = 'xyz456'
```

This approach creates several problems. If staff change or leave, every branching logic expression that references their ID must be updated manually, across every instrument it appears in. The identifiers also end up embedded in the data dictionary, creating an informal personnel record that is hard to audit and potentially privacy-sensitive.

**Preferred approach: use a role-based or configurable field**

Instead of hardcoding identifiers, collect the reviewer's identity in a dedicated field and gate visibility on a role or a flag value that is easy to update:

- Use a dropdown or radio field (e.g., `reviewer_role`) populated with role names rather than personal identifiers.
- Gate admin-only fields on `[reviewer_role] = 'admin'` instead of on a specific person's username.
- If the set of reviewers is small and changes rarely, consider a single configuration field at the project level whose value can be updated without touching the data dictionary.

**Rationale:** Hardcoded IDs tie the instrument design to specific individuals, make maintenance error-prone, and expose personnel information in the data dictionary. Role-based logic survives staff turnover without requiring structural changes.

**Exception:** In a tightly controlled internal tool where the reviewer list is stable and the project owner accepts the maintenance burden, hardcoded identifiers may be acceptable as a short-term convenience. Document the intent in the Field Annotation so future designers understand why it is there.

## 5.2 Use a descriptive field to display a conditional warning or alert

**Best practice: use a `descriptive` field type with branching logic to surface warnings inline on the form**

When a user makes a combination of choices that requires an action or creates a likely error, a descriptive field with targeted branching logic can display a warning directly on the form — no external notification needed. Example: show a warning only when a user selects "No" for an end-date waiver but then leaves the end date field blank.

```
[ongoing] = '2' and [enddate] = ''
```

The descriptive field is shown only when that condition is true, and it can include styled HTML (e.g., red text) to make the warning visually distinct.

**Rationale:** Inline warnings catch data entry errors at the moment they occur, reducing cleanup later. They are less intrusive than required-field validation, which blocks form submission entirely, and more visible than post-submission alerts.

**Tip:** Keep the warning label short and action-oriented (e.g., "You selected 'No' to ongoing access but no end date was entered. Please enter an end date above or change your selection."). Style with `<span style="color:red;font-weight:bold;">` for visibility.

## 5.3 Admin-only review sections: gate with a reviewer identity field, not user rights alone

**Best practice: when a form contains fields that only an administrator should see, use a dedicated reviewer identity field as the branching logic gate — in addition to any user rights restrictions**

Admin-only review fields (e.g., reviewer notes, status codes, internal dates) can be hidden from data entry users by placing them behind branching logic that checks a reviewer-identity field. The reviewer enters their own identifier into that field, which unlocks the admin section.

```
[reviewer_field] <> ''
```

This is distinct from relying on REDCap's user rights alone. User rights prevent editing, but they do not hide fields from view. Branching logic provides the visual hiding.

**Rationale:** Combining user rights (to prevent unauthorized editing) with branching logic (to prevent visual exposure of internal fields) gives a cleaner experience for requesters completing a survey and a clearer separation of concerns in the form layout.

**Note:** See Section 5.1 for guidance on what value to check in the reviewer identity field — prefer role-based values over hardcoded personal identifiers.

## 5.4 Always add branching logic to "Other (specify)" free-text fields

**Best practice: any free-text field paired with an "Other" choice must have branching logic that hides it when that choice is not selected**

A radio or dropdown field that includes an "Other (specify)" option typically has a companion free-text field for the specified value. Without branching logic on that companion field, it is visible at all times — even when the respondent has not selected "Other." This produces spurious blank fields in the dataset and clutters the form unnecessarily.

The branching logic on the "Other (specify)" field should match the exact code assigned to the "Other" choice in the parent field:

```
[parent_field] = '666'
```

Adjust to match whatever code your project assigns to the "Other" choice.

**Do not embed the field name in the choice label as a substitute.** A pattern sometimes seen is writing the companion field name directly in the choice label (e.g., `666, Other — {specify_field}`). REDCap does not parse curly-brace or similar notation in choice labels — the text renders literally and the field remains unconditionally visible. Use standard branching logic on the companion field instead.

**Rationale:** When the free-text field is hidden unless "Other" is selected, a blank value unambiguously means "not applicable." When it is always visible, a blank value is ambiguous — it could mean not applicable, not answered, or overlooked. Branching logic eliminates that ambiguity and keeps forms clean.

## 5.5 Do not mark a field as required when the requirement is conditional

**Best practice: if a field is only meaningful based on another field's value, use branching logic to hide it when not applicable — not the "Required" flag**

REDCap's Required flag blocks form completion until the field contains a value. When a required field is always visible but only sometimes relevant, users must enter a placeholder ("N/A", "none", "-") to save the form, which pollutes the dataset and complicates analysis.

Common examples where this pattern causes problems:

- A "Deviation Description" field required on every test case, even when the test result is "Pass" (no deviation exists)
- A "Modification Approved By" field required on version 1.0 of a document (no modifications have been made)
- A "Reason for early withdrawal" field required even for participants who completed the study

**Preferred approach:** Use branching logic to show the field only when it is applicable. When a field is hidden by branching logic, REDCap does not enforce the Required constraint — the field is treated as not applicable.

```
// Show Deviation Description only when the test failed
[pass_fail] = '0'
```

If you want to enforce entry without blocking form save, use the inline warning pattern from Section 5.2 instead.

**Rationale:** Required-always fields that are conditionally relevant train users to enter meaningless placeholder values. Branching logic is the correct mechanism for conditional data entry — it keeps the dataset clean and the form free of fields that don't apply in context.

---

# 6. Repeating Instruments

## 6.1 Use custom form labels to identify repeating instrument instances

**Best practice: set the custom form label on repeating instruments to display the key identifying field(s) for that instance**

When an instrument repeats, the record status dashboard shows each instance as "Instance 1", "Instance 2", etc. by default. Adding a custom form label that pipes in a meaningful field (e.g., the user's name, a project title, or a date) makes it immediately clear what each instance contains without opening it.

Example custom form label for a user request instrument:
```
[institutional_id], [user_name]
```

Example for a project request instrument:
```
[projectname] ([server_field]), pid: [pid]
```

**Rationale:** When a record has many repeating instances, unlabeled instances are difficult to navigate. Custom form labels cost nothing to set up and significantly reduce confusion during data review.

**Where to set it:**

- **Repeating instruments** — Project Setup → Enable optional modules and customizations → Repeating instruments (Enable / Modify). In the popup, enter the piping expression in the custom label field next to the instrument name. This is the only place this label can be configured; it is not available in the Online Designer. (RC-LONG-02 §4–6)
- **Repeating events** — The custom label field in the repeating instruments popup is greyed out for events set to "Repeat entire event." Instead, set the label in **Define My Events** using the **Custom Event Label** column. (RC-LONG-01 §4.2, RC-LONG-02 §6)

---

# 7. Field and Form Hygiene

## 7.1 Every field must have a label

**Best practice: no field should have a blank field label**

REDCap allows a field to be saved with an empty label, but doing so creates a blank space on the form that gives the respondent no indication of what the field is for. This most commonly happens with companion fields added late in the design process (e.g., a file upload added to hold a generated PDF, or a "specify" text field placed after a radio option).

Check for unlabeled fields before the project goes live. A quick way to audit: export the data dictionary and filter for rows where the `field_label` column is blank (excluding the record ID field, which is legitimately label-free in some configurations).

**Common causes:**
- Companion "Other (specify)" fields where the designer assumed the parent choice label was sufficient
- File upload fields added as an afterthought to hold generated outputs or summary documents
- Descriptive fields used as spacers, left blank intentionally — these should at minimum contain a comment in the Field Annotation documenting their purpose

**Rationale:** Unlabeled fields are confusing to data entry users and future designers alike. They signal an incomplete design and make it hard to distinguish intentional placeholders from accidental omissions.

## 7.2 Audit instrument-event and repeating-instrument settings across all arms

**Best practice: when a project has multiple arms, verify that repeating instrument configuration is consistent across all arms that use the same workflow structure**

In a multi-arm project where each arm represents a parallel lifecycle phase or patient cohort with the same event structure, the repeating instrument settings should generally be identical across arms. A common oversight is configuring a repeating instrument in Arms 2–4 while leaving it non-repeating in Arm 1 — because Arm 1 was built first and the repeating configuration was added later without being back-applied.

The result is that one arm has a different data collection capacity than the others: Arm 1 records can only have one instance, while Arms 2–4 records can have many. This inconsistency is difficult to detect from the form UI and only becomes apparent when a user tries to add a second instance in Arm 1 and cannot.

**How to check:** Project Setup → Repeating Instruments and Events → review the list of configured repeating instruments. Each entry shows the event name and arm. Verify that equivalent events in every arm appear in the list if they should repeat.

---

## 3.2 Multi-entity registration using separate instruments per entity

**Best practice: when collecting the same set of fields for a small, bounded number of entities (e.g., up to 4 children in a family registration), separate instruments per entity can be a cleaner alternative to repeating instruments**

When the maximum count of entities is known upfront and small (typically 2–5), creating one instrument per entity slot (e.g., Child 1, Child 2, Child 3, Child 4) avoids the complexity of repeating instruments while still giving each entity its own dedicated survey page and navigation step.

**How it works:**

1. Add a count selector field early in the registration (e.g., "How many children are you registering?" — radio with options 1, 2, 3, 4).
2. Apply branching logic or survey queue rules so that only the relevant entity instruments are shown (e.g., Child 3 and Child 4 instruments are skipped when the respondent selected "2").
3. Field naming follows a numeric suffix convention: `vnaam1`, `vnaam2`, `vnaam3`, `vnaam4` for first name across child instruments.

**When to prefer this over repeating instruments:**

- The max count is small and fixed (≤ 4–5) and unlikely to change
- Each entity form benefits from being a distinct survey page (cleaner navigation, progress indicators, per-page save points)
- Survey queue integration is in use and needs to route participants to per-entity forms
- The downstream export or reporting tool works better with a flat, predictable column structure than with instance-numbered rows

**When to prefer repeating instruments instead:**

- The count is large, unknown, or unbounded at design time
- The same set of data is collected by staff rather than via survey (data entry grids work well with repeating instruments)
- You need the record status dashboard to reflect individual instance completion states

**Tradeoffs to document:**

The flat-column approach produces a wider dataset with many NULL columns for families registering fewer children than the maximum. If there is any chance the maximum will increase (e.g., a fifth child is needed), new instruments and corresponding fields must be added manually. Note this explicitly in the project design documentation.

---

## 5.6 Use descriptive fields as piped context summaries at the top of each form

**Best practice: at the top of each follow-on instrument in a multi-form survey, place a descriptive field that pipes in key values from earlier forms as a reminder for the respondent**

When a survey spans multiple instruments and collects linked but separate information (e.g., parent details first, then per-child details), respondents may lose track of which family member or entity the current page refers to. A descriptive field at the top of each subsequent form can pipe in identifying information (e.g., the child's name and date of birth) to anchor the respondent without requiring them to navigate back.

Example field label for a child instrument:
```
Child: {vnaam1} {anaam1} — Date of birth: {dob1}
```

This field has no variable and stores no data — it exists purely to display piped context.

**When this pattern adds the most value:**

- Multi-entity forms (see Section 3.2) where each instrument covers a different person or item
- Long surveys split across multiple pages where earlier answers are no longer visible
- Review or confirmation pages that summarize what the respondent entered before they submit

**Implementation note:** These fields are `descriptive` type. Give them a meaningful variable name (e.g., `kinddesc1`) so they are easy to identify in the data dictionary. Add a Field Annotation noting that the field is a display-only context header. Because they are descriptive, they export as blank columns — which is expected and acceptable. If you want to suppress them from exports entirely, the `@HIDDEN` action tag can be applied.

---

## 7.3 Use a dedicated metrics instrument for built-in enrollment dashboards

**Best practice: if a project needs to track aggregate counts (e.g., enrollment per class, applications per category), consider adding a separate instrument containing only calculated fields that tally those counts**

Placing summary calculated fields in a dedicated instrument — separate from the data entry forms — keeps the data collection instruments clean and makes it easy to view or export aggregate metrics independently. This pattern works well for enrollment and registration projects where a program coordinator needs to quickly see headcounts without building a separate report.

Example calculated fields for a class registration project:
- `speelsum` — count of children registered for the youngest group
- `groep1sum` through `groep8sum` — per-grade enrollment counts
- `vosum` — count of secondary-school-age registrations

These fields use the REDCap `sum()` function (or equivalent logic) across the per-child group selection fields.

**Considerations:**

- Calculated fields in this instrument will only reflect values from the same record. For project-wide totals across all records, use Reports or a REDCap dashboard instead — calculated fields cannot aggregate across records.
- This pattern is appropriate for per-record summaries (e.g., total number of children in a family registration) but not for multi-record totals (e.g., total enrollment across all families). For multi-record totals, use the REDCap aggregate smart variables or a custom report.
- Keep the metrics instrument at the end of the instrument list to avoid cluttering the survey queue or data entry workflow.

---

## 7.4 Deferred file upload: give respondents the option to upload documents later

**Best practice: when a survey requires document uploads (e.g., vaccination records, supporting documents) that respondents may not have immediately available, offer an explicit "upload now or later" choice and provide a dedicated follow-up instrument for deferred uploads**

Requiring a file upload at the time of initial registration blocks form completion for respondents who need to locate documents. Offering "Upload now / Upload later" as a radio choice, followed by a separate instrument dedicated to deferred uploads, improves completion rates while still collecting the required documents.

**Implementation pattern:**

1. In the main per-entity form, add a radio field asking whether the respondent wants to upload the document now or later (e.g., `vacup1`, choices: `1=Now | 2=Later`).
2. If "Now": show an inline file upload field on the same instrument, gated behind branching logic (`[vacup1] = '1'`).
3. Create a separate "Document Upload" instrument that contains file upload fields for all entities, each gated behind branching logic checking for the "Later" response (`[vacup1] = '2'`).
4. Use the Survey Queue to present the deferred upload instrument to the respondent on a return visit, or send a targeted alert/notification with the survey link after initial registration is complete.

**Rationale:** Splitting the upload from the core registration reduces friction at the most critical point in the workflow (initial form completion) without permanently losing the requirement. The deferred instrument also serves as a convenient standalone link for respondents who need to update documents later (e.g., when vaccination records change).

---

# 8. Related Articles

- RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques
- RC-LONG-01 — Longitudinal Project Setup
- RC-LONG-02 — Repeated Instruments & Events Setup
- RC-OPS-01 — Using REDCap as an Operational Request Management System
- RC-SURV-01 — Survey Basics
