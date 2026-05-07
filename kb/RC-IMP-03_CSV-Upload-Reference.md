RC-IMP-03

**CSV Upload Reference: All Bulk Upload Options in REDCap**

| **Article ID** | RC-IMP-03 |
|---|---|
| **Domain** | Data Import |
| **Applies To** | All REDCap project types; required rights vary per feature |
| **Prerequisite** | RC-IMP-01 — Data Import Overview |
| **Skill Level** | Intermediate |
| **Version** | 1.0 |
| **Last Updated** | 2026-05-07 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-IMP-01 — Data Import Overview; RC-FD-03 — Data Dictionary; RC-LONG-01 — Longitudinal Project Setup; RC-USER-02 — User Rights: Adding Users & Managing Roles; RC-DAG-01 — Data Access Groups |

---

# 1. Overview

REDCap offers CSV-based upload and download for many areas of a project — not just participant data. Knowing which settings can be managed via file upload lets you work more efficiently on large projects and move configurations between projects without rebuilding them by hand.

This article is a comprehensive reference of every REDCap setting that supports CSV upload. For each, it describes: where to find the upload option in the UI, what the upload does (additive vs. replace), and which article covers the full details.

> **CSV vs. other file types:** This article focuses on CSV uploads. REDCap also supports XML (for full project backups and record imports via CDISC ODM format) and ZIP files (for importing individual instruments). See RC-IMP-01 — Data Import Overview for coverage of those formats.

---

# 2. Quick Reference Table

| **What you're uploading** | **Location in REDCap** | **Upload behavior** | **Rights required** | **Detailed article** |
|---|---|---|---|---|
| Data Dictionary | Project Setup or Online Designer | **Replaces** all instruments and fields | Project Design and Setup | RC-FD-03 |
| Arms | Define My Events | **Additive** — adds new arms, existing unchanged | Project Design and Setup | RC-LONG-01 |
| Events | Define My Events | **Additive** — adds new events, existing unchanged | Project Design and Setup | RC-LONG-01 |
| Instrument–Event Mappings | Designate Instruments for My Events | **Replaces** entire mapping | Project Design and Setup | RC-LONG-01 |
| Record Data | Applications → Data Import Tool | Additive by default; can overwrite with setting | Data Entry rights | RC-IMP-01 |
| Users | User Rights | Additive/update | User Rights | RC-USER-02 |
| User Roles | User Rights | Additive/update | User Rights | RC-USER-02 |
| User–Role Assignments | User Rights | Additive/update | User Rights | RC-USER-02 |
| Data Access Groups (DAGs) | DAGs / User Rights | Additive/update | Data Access Groups | RC-DAG-01 |
| User–DAG Assignments | DAGs / User Rights | Additive/update | Data Access Groups | RC-DAG-01 |
| Alerts & Notifications | Alerts & Notifications | Additive — imports alert definitions | Project Design and Setup | RC-ALERT-01 |
| Automated Survey Invitations (ASI) | Online Designer → Automated Survey Invitations button | Additive/update | Project Design and Setup | RC-SURV-06 |
| Survey Queue | Online Designer → Survey Queue button | Additive/update | Project Design and Setup | RC-SURV-07 |
| Survey Settings | Online Designer → Survey Settings button | Additive/update | Project Design and Setup | RC-SURV-02 |
| Form Display Logic | Online Designer → Form Display Logic | Additive/update | Project Design and Setup | RC-FDL-01 |
| Data Quality Rules | Data Quality module | Additive/update | Project Design and Setup | RC-DQ-01 |
| Language Setups (MLM) | Multi-Language Management | Additive/update | Project Design and Setup | RC-MLM-01 |
| Randomization Allocation Table | Randomization module | Replaces active allocation table | Randomization Setup rights | RC-RAND-02 |

> **Download-only:** The Logging module supports CSV *download* but not upload.

---

# 3. Project Structure

## 3.1 Data Dictionary

**Location:** Project Setup → "Data Collection Instruments" section → Data Dictionary button; or the Online Designer header.

**What it does:** Defines all variables and instruments in the project. A single CSV file represents the complete instrument configuration — every field, label, choice, validation rule, branching logic expression, and instrument assignment lives here.

**Upload behavior — Replace:** Uploading a Data Dictionary **replaces the entire current configuration**. Variables present in the project but absent from the uploaded file are deleted, along with any data they contain.

**Key safety practice:** Always download and save a snapshot of the current Data Dictionary before uploading a modified version. This is your only recovery path if a bad upload needs to be rolled back.

**Full details:** RC-FD-03 — Data Dictionary

---

## 3.2 Instrument–Event Mappings

**Location:** Define My Events → Designate Instruments for My Events → "Upload or download instrument mappings" dropdown.

**What it does:** Defines which instruments are assigned (designated) to which events in a longitudinal project. Each row in the CSV represents one instrument–event combination.

**Upload behavior — Replace:** Unlike the arms and events uploads, the instrument–event mapping upload **replaces the entire mapping**. Any instrument–event combination omitted from the file will be unchecked — potentially deleting data if that combination had records saved in it. Always download the current mapping first and edit it rather than building a new file from scratch.

**CSV columns:** `arm_num`, `unique_event_name`, `form`

**Full details:** RC-LONG-01 — Longitudinal Project Setup, Section 6.2

---

# 4. Longitudinal Setup

## 4.1 Arms

**Location:** Define My Events → "Upload or download arms/events" dropdown.

**What it does:** Creates arms (participant cohorts) in a longitudinal project. Each row defines one arm.

**Upload behavior — Additive:** REDCap adds any arms in the file that do not already exist. Existing arms not in the file are left unchanged.

**CSV columns:** `arm_num`, `name`

> **Single-arm projects:** Arm 1 is created automatically when longitudinal mode is enabled. Skip the arms upload entirely for single-arm projects — start directly with the events upload.

**Upload order:** When setting up a longitudinal project from scratch via CSV, always upload in sequence: **arms → events → instrument-event mappings**. Events reference arm numbers, and mappings reference unique event names — uploading out of order will cause references to fail.

**Full details:** RC-LONG-01 — Longitudinal Project Setup, Section 6.1

---

## 4.2 Events

**Location:** Define My Events → "Upload or download arms/events" dropdown.

**What it does:** Creates events (time points) within arms of a longitudinal project.

**Upload behavior — Additive:** REDCap adds any events in the file that do not already exist. Existing events not in the file are left unchanged.

**CSV columns (core):** `event_name`, `arm_num`, `unique_event_name`, `custom_event_label`

- `unique_event_name` may be left blank — REDCap auto-generates it from the event name and arm number. **Recommended:** leave this column blank and let REDCap generate the value. Hand-typed unique event names frequently diverge from what REDCap generates (particularly for event names containing hyphens, which REDCap removes rather than converting to underscores).
- `custom_event_label` may be left blank if piped event labels are not in use.

**CSV columns (with Scheduling module active):** adds `day_offset`, `offset_min`, `offset_max`

**Full details:** RC-LONG-01 — Longitudinal Project Setup, Section 6.1

---

# 5. User Access & DAGs

## 5.1 Users, User Roles, and User–Role Assignments

**Location:** User Rights → "Upload or download users, roles, and assignments" button (top right of the User Rights page).

**What it does:** The bulk user management feature lets you download the current configuration of all users, roles, and role assignments as structured files, then upload modified versions to apply changes in bulk. This is useful for large projects or migrating a user configuration from another project.

**Upload behavior:** Additive/update — new users are added, existing user configurations are updated to match the file.

**Rights required:** User Rights privilege.

**Full details:** RC-USER-02 — User Rights: Adding Users & Managing Roles, Section 7

---

## 5.2 Data Access Groups (DAGs) and User–DAG Assignments

**Location:** Applications → DAGs (or User Rights → Data Access Group tab) → "Upload or download DAGs/User-DAG assignments" button.

**What it does:** Two related uploads are available here:

- **DAGs upload** — creates DAG definitions (group names). Useful for initial setup of a multi-site project.
- **User–DAG assignments upload** — assigns users to DAGs in bulk.

**Upload behavior:** Additive/update — new DAGs or assignments are added; existing ones may be updated.

**Rights required:** Data Access Groups privilege.

**DAGs CSV columns:** `data_access_group_name`, `unique_group_name`

- `data_access_group_name` — Human-readable display name (e.g., `Boston Site`). Quote values that contain spaces or commas.
- `unique_group_name` — System identifier used in all API and data entry operations. Leave blank to let REDCap auto-generate it (lowercase, spaces → underscores). Exports include a third column, `data_access_group_id`, which is read-only and ignored on import.

**User–DAG assignments CSV columns:** `username`, `redcap_data_access_group`

- `username` — REDCap login name; must match an existing project user.
- `redcap_data_access_group` — The `unique_group_name` of the target DAG (not the display name). Leave blank to remove the user from all DAGs (grants all-DAG access).

**Full details:** RC-API-29 — Import DAGs; RC-API-32 — Import User-DAG Assignments; RC-DAG-01 — Data Access Groups, Section 7

---

# 6. Records (Participant Data)

## 6.1 Record Data Import

**Location:** Applications → Data Import Tool.

**What it does:** Imports participant record data in bulk from a CSV file. Any REDCap data export in CSV format can be re-imported into the same project as-is. Partial imports (specific fields or records only) are also supported.

**Upload behavior:** Additive by default — blank cells in the import file are ignored and existing values are preserved. An optional setting ("Overwrite data with blank values") can be enabled to erase existing values with blank cells.

**Important:** Clicking "Upload File" only stages a preview. The data is not saved until you scroll down and click "Import Data" on the results screen.

**Full details:** RC-IMP-01 — Data Import Overview, Sections 8 and 9

### Column Reference

Every record data CSV — whether built from scratch or downloaded from REDCap — uses the same set of column types. The columns below appear in the order REDCap places them in a standard export.

| **Column** | **Required?** | **Notes** |
|---|---|---|
| `record_id` *(or project-specific name)* | Always | First column. The variable name must match the project's Record ID field exactly (e.g., `participant_id`, `patient_id`). |
| `redcap_event_name` | Longitudinal projects | Unique event name in the format `uniqueeventname_arm_N` (e.g., `baseline_arm_1`). Find all values under Project Setup → Define My Events. |
| `redcap_repeat_instrument` | Repeating instruments | The instrument's variable name (lowercase, underscored) for the repeating instrument this row belongs to. Empty for regular event rows and for repeating-event rows. |
| `redcap_repeat_instance` | Repeating instruments or events | Integer instance number starting at 1. When `redcap_repeat_instrument` is empty but this column has a value, REDCap treats the row as a repeating-event instance. Use the value `new` to let REDCap assign the next available instance number automatically. |
| `redcap_survey_identifier` | Never import | Present in exports — holds the survey participant identifier (e.g., name or email used for survey invitations). **Read-only system value. Omit this column or leave it blank on import; the Data Import Tool ignores it.** |
| `redcap_data_access_group` | Conditional | Required only when the uploading user is assigned to one or more DAGs. Omit entirely if the project does not use DAGs. |
| *Instrument fields* (e.g., `screen_age_over_18`) | As needed | Include only the variables you want to set. Omitting a column leaves existing data unchanged (additive behavior). Values must be raw-coded (numbers, dates, text) — not choice labels. |
| `fieldname___N` *(checkbox choices)* | As needed | Checkbox fields produce one column per answer choice. `N` is the raw coded value for that choice (e.g., `demo_race___1`, `demo_race___2`). Values are `1` (checked) or `0` (unchecked). Omitting a checkbox column leaves existing checked state unchanged. |
| `*_timestamp` *(e.g., `demographics_timestamp`)* | Never import | Present in exports — auto-generated timestamp recording when a survey instrument was submitted. **Read-only system value. Omit or leave blank; values in these columns are ignored by the Data Import Tool.** |
| `*_complete` *(e.g., `demographics_complete`)* | Optional | Form completion status. Integer: `0` = Incomplete, `1` = Unverified, `2` = Complete. Import to set or update form status. When omitted, existing status is unchanged. |

### Example: Longitudinal Project with a Repeating Instrument

The table below illustrates how a single record spans multiple rows in a longitudinal project that also has a repeating instrument (`medication_list`). Only selected columns are shown — a real export includes all project fields across all instruments, so most cells in any given row will be empty.

| `record_id` | `redcap_event_name` | `redcap_repeat_instrument` | `redcap_repeat_instance` | `screen_date` | `phq9_total` | `med_name` | `med_start_date` | `screening_complete` | `phq9_complete` | `medication_list_complete` |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `screening_arm_1` | *(empty)* | *(empty)* | 2026-04-30 | *(empty)* | *(empty)* | *(empty)* | 1 | *(empty)* | *(empty)* |
| 1 | `baseline_arm_1` | *(empty)* | *(empty)* | *(empty)* | 12 | *(empty)* | *(empty)* | *(empty)* | 0 | *(empty)* |
| 1 | `3_month_arm_1` | *(empty)* | *(empty)* | *(empty)* | 10 | *(empty)* | *(empty)* | *(empty)* | 1 | *(empty)* |
| 1 | `baseline_arm_1` | `medication_list` | 1 | *(empty)* | *(empty)* | Metformin | 2026-05-01 | *(empty)* | *(empty)* | 2 |
| 1 | `baseline_arm_1` | `medication_list` | 2 | *(empty)* | *(empty)* | Lisinopril | 2026-05-01 | *(empty)* | *(empty)* | 1 |
| 1 | `3_month_arm_1` | `medication_list` | 1 | *(empty)* | *(empty)* | Metformin | 2026-05-01 | *(empty)* | *(empty)* | 0 |

Key points illustrated by this example:

- **One row per event** — regular (non-repeating) event data goes in a row where both repeat columns are empty. REDCap includes a row for every event in an export, even events with no data entered.
- **One row per repeating instrument instance** — each instance of a repeating instrument gets its own row with `redcap_repeat_instrument` and `redcap_repeat_instance` filled in.
- **Same repeating instrument at multiple events** — `medication_list` has instances at both `baseline_arm_1` and `3_month_arm_1`. Instance numbers are independent per event — instance 1 at baseline and instance 1 at 3 months are separate records.
- **Most cells are empty in any given row** — a row carries data only for the fields belonging to that event or instrument instance. In a wide project with many instruments, the vast majority of cells will be empty. This is correct and expected — not a sign of file corruption.
- **Complete status columns (`*_complete`) appear at the end of each instrument's field group** — they can be imported alongside data fields or omitted.

### Getting the Right Header Row

Two methods reliably produce the correct column layout for your project:

- **Download the Data Import Template** from within the Data Import Tool. The template is header-only (no data rows) and includes the exact column set and coordinate variables your project requires.
- **Export existing data** from Applications → Data Exports, Reports & Stats. The export uses the same header structure and, if records already exist, provides real examples of correctly formatted values.

Building the header row manually is error-prone. Always start from one of these two sources.

---

# 7. Other Project Configuration

## 7.1 Alerts & Notifications

**Location:** Applications → Alerts & Notifications → "Upload or download alerts" button.

**What it does:** Exports all alert definitions from a project as a CSV file and allows importing alert configurations — useful for copying a set of alerts from one project to another or for making bulk edits outside of REDCap.

**Upload behavior:** Additive — imported alerts are added to the existing list.

**Rights required:** Project Design and Setup.

**Full details:** RC-ALERT-01 — Alerts & Notifications: Setup

### Column Reference

Each row in the file represents one alert. The table below documents every column.

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `alert-unique-id` | No (new) / Yes (update) | REDCap-assigned identifier in the format `A-XXXX` (e.g., `A-2482`). Leave blank when creating new alerts — REDCap assigns the ID on import. Required when updating or copying specific existing alerts. |
| `alert-title` | No | Free-text display name. Optional but strongly recommended; this is the primary identifier in the Alerts management view and the notification log. |
| `alert-trigger` | Yes | `SUBMIT` — completion or combination trigger (fires on instrument save). `LOGIC` — logic trigger (fires when logic becomes true, regardless of save source, including imports and API writes). |
| `unique-form-name` | Yes (SUBMIT) | The instrument's unique name (variable name, not display label). Required for `SUBMIT` triggers; specifies which instrument save activates the alert. |
| `unique-event-name` | No | The event's unique name (e.g., `baseline_arm_1`). Leave blank for classic (non-longitudinal) projects. When blank in a longitudinal project, the alert applies to any event where the instrument appears. Event context for recipients and message content is specified via piping syntax inside `email-to` and `alert-message` instead. |
| `saved-with-form-status` | No | `COMPLETE` — fires only when the instrument is saved with Complete status (value 2). Leave blank to fire on any save status. |
| `alert-condition` | No | Logic expression string (same syntax as branching logic). Required for combination triggers and logic triggers. Leave blank for pure completion triggers. |
| `ensure-logic-still-true` | Yes | `Y` or `N`. When `Y`, REDCap re-evaluates the trigger logic immediately before sending. If the logic is no longer true at send time, the queued alert is cancelled. Most useful when the alert has a scheduled delay. |
| `do-not-clear-recurrences` | Yes | `Y` or `N`. Controls whether a new trigger event clears previously queued recurrences for the same record. |
| `alert-stop-type` | Yes | Trigger limit — how many times the alert can fire per record. `RECORD` — once per record. Additional values for longitudinal/repeated projects include `EVENT` (once per event), `INSTANCE` (once per repeat instance), and `EVENT_INSTANCE` (once per event-instance combination). |
| `send-on` | Yes | When to send after the trigger fires. `NOW` — immediately. `TIME_LAG` — after a specified delay (configure with `send-on-time-lag-days`, `send-on-time-lag-hours`, `send-on-time-lag-minutes`). `NEXT_DAY` — next occurrence of a specified day type (configure with `send-on-next-day-type` and `send-on-next-time`). `EXACT_DATE` — at a specific date/time (configure with `send-on-date`). `FIELD` — relative to a date stored in a project field (configure with `send-on-field`). |
| `send-on-next-day-type` | Conditional | Day-type value for `NEXT_DAY` sends (e.g., weekday, Monday). Leave blank otherwise. |
| `send-on-next-time` | Conditional | Time component (HH:MM) for `NEXT_DAY` sends. Leave blank otherwise. |
| `send-on-time-lag-days` | Conditional | Number of days for `TIME_LAG` delay. All three lag columns (`days`, `hours`, `minutes`) must be specified together — use `0` for units not needed. |
| `send-on-time-lag-hours` | Conditional | Hours component of `TIME_LAG` delay. Use `0` if not needed. |
| `send-on-time-lag-minutes` | Conditional | Minutes component of `TIME_LAG` delay. Use `0` if not needed. |
| `send-on-field-after` | Conditional | Direction for `TIME_LAG` sends: `after` (send N days/hours/minutes after the trigger). Leave blank for `NOW` sends. |
| `send-on-field` | Conditional | The project field name used as a reference date for `FIELD` sends. Leave blank otherwise. |
| `send-on-date` | Conditional | Specific date/time for `EXACT_DATE` sends (server time zone applies). Leave blank otherwise. |
| `alert-send-how-many` | Yes | `ONCE` — send a single time per trigger event. `MULTIPLE` — send on a recurring basis (configure with `every-time-type`, `repeat-for`, `repeat-for-units`, `repeat-for-max`). |
| `every-time-type` | Conditional | Required when `alert-send-how-many` = `MULTIPLE`. The unit for the recurrence interval. |
| `repeat-for` | Conditional | Numeric interval between recurring sends. |
| `repeat-for-units` | Conditional | Unit for `repeat-for` (days, hours, or minutes). |
| `repeat-for-max` | Conditional | Maximum number of sends including the first. **Always set this** — leaving it blank causes REDCap to send indefinitely. |
| `alert-expiration` | No | Date/time after which REDCap will not send any further instances of this alert, and will cancel any already-queued ones. |
| `alert-type` | Yes | `EMAIL` — standard email (always available). `SMS` — text message (if enabled). `VOICE` — voice call (if enabled). `SENDGRID` — SendGrid delivery (if configured). |
| `email-from-display` | No | Optional display name for the from address (e.g., `Heart Study Team`). Leave blank to use the raw email address as the display name. |
| `email-from` | Yes (email) | The from email address. Must be an address associated with a current project user's REDCap profile. |
| `email-to` | Yes (email) | Recipient(s). Accepts: a static email address; a project field variable (`[field_name]`); or an event-prefixed field variable for longitudinal projects (`[event_name][field_name]`, e.g., `[baseline_arm_1][contact_email]`). Multiple recipients separated by semicolons. |
| `email-cc` | No | CC recipient(s). Same syntax as `email-to`. |
| `email-bcc` | No | BCC recipient(s). Same syntax as `email-to`. |
| `email-failed` | No | Email address to notify if REDCap fails to deliver the alert. Only one address is accepted. |
| `email-subject` | Yes (email) | Subject line. Supports piping syntax. Avoid piping identifiers here unless the `prevent-piping-identifiers` column is set to `N`. |
| `alert-message` | Yes | The message body. Supports HTML, piped variables, and smart variables (e.g., `[survey-link:instrument_name:Link text]`). In longitudinal projects, prefix survey link smart variables with the target event: `[event_name][survey-link:instrument_name:Link text]`. The field can span multiple lines in the CSV — the entire value is quoted. |
| `sendgrid-template-id` | No | SendGrid template ID. Leave blank for standard email alerts. |
| `sendgrid-template-data` | Yes | JSON object. Use `{}` when not supplying SendGrid template variables. Do not leave blank — an empty JSON object is required. |
| `sendgrid-mail-send-configuration` | Yes | JSON object. Use `{}` when not using custom SendGrid mail send configuration. Do not leave blank. |
| `prevent-piping-identifiers` | Yes | `Y` or `N`. When `Y` (the default in the UI), REDCap strips identifier field values from piped content before sending. Set to `N` only when intentional identifier piping has been confirmed as appropriate with your IRB. |
| `file-upload-fields` | No | Comma-separated list of file upload field names. Files stored in these fields for the triggering record are attached to the alert email. Leave blank if no attachments are needed. |
| `phone-number-to` | Conditional | Phone number for SMS or voice call alerts. Leave blank for email. |
| `alert-deactivated` | Yes | `Y` — alert is inactive and will not fire. `N` — alert is active. |

### Annotated Example

The file below contains two alerts from a longitudinal project with two arms (`baseline_arm_1` and `3_month_arm_1`):

**Alert A-2482 — "Invite baseline"**
Fires immediately when the `screening` form is saved with Complete status. Sends once per record. Emails the participant at the address stored in `[baseline_arm_1][contact_email]`. The message body contains a survey link to the `demographics` instrument at the baseline event.

**Alert A-2483 — "Invite 3 months"**
Same trigger as A-2482 (screening form Complete), but scheduled to send 90 days later (`TIME_LAG`, 90 days, 0 hours, 0 minutes). The message links to the `phq9` instrument at the `3_month_arm_1` event. The event prefix on the survey link (`[3_month_arm_1][survey-link:phq9:Start here]`) ensures REDCap generates a link to the correct event, not the baseline event.

```csv
alert-unique-id,alert-title,alert-trigger,unique-form-name,unique-event-name,saved-with-form-status,alert-condition,ensure-logic-still-true,do-not-clear-recurrences,alert-stop-type,send-on,send-on-next-day-type,send-on-next-time,send-on-time-lag-days,send-on-time-lag-hours,send-on-time-lag-minutes,send-on-field-after,send-on-field,send-on-date,alert-send-how-many,every-time-type,repeat-for,repeat-for-units,repeat-for-max,alert-expiration,alert-type,email-from-display,email-from,email-to,email-cc,email-bcc,email-failed,email-subject,alert-message,sendgrid-template-id,sendgrid-template-data,sendgrid-mail-send-configuration,prevent-piping-identifiers,file-upload-fields,phone-number-to,alert-deactivated
A-2482,"Invite baseline",SUBMIT,screening,,COMPLETE,,N,N,RECORD,NOW,,,,,,,,,ONCE,,,,,,EMAIL,,study@institution.edu,[baseline_arm_1][contact_email],,,,"Invite for baseline","<p>Hi,</p><p>Please complete the baseline forms:</p><p>[baseline_arm_1][survey-link:demographics:Start here]</p><p>thanks,</p><p>Study team</p>",,{},{},N,,,N
A-2483,"Invite 3 months",SUBMIT,screening,,COMPLETE,,N,N,RECORD,TIME_LAG,,,90,0,0,after,,,ONCE,,,,,,EMAIL,,study@institution.edu,[baseline_arm_1][contact_email],,,,"Invite for 3 months","<p>Hi,</p><p>Please complete the 3-month forms:</p><p>[3_month_arm_1][survey-link:phq9:Start here]</p><p>thanks,</p><p>Study team</p>",,{},{},N,,,N
```

### Common Mistakes

**Leaving `sendgrid-template-data` and `sendgrid-mail-send-configuration` blank.** These columns must contain a JSON object. Use `{}` when not using SendGrid features. A blank cell here can cause import errors.

**Omitting the event prefix on `email-to` in a longitudinal project.** Writing `[contact_email]` without an event prefix may resolve to the wrong event or fail entirely if the field appears at multiple events. Always use `[event_name][field_name]` form for longitudinal recipients.

**Omitting the event prefix in `alert-message` survey links.** `[survey-link:phq9]` without an event prefix is ambiguous in a longitudinal project where the instrument appears at multiple events. Always write `[event_name][survey-link:instrument_name:Link text]`.

**Specifying only `send-on-time-lag-days` for a TIME_LAG send.** All three lag columns — days, hours, and minutes — must be present. Use `0` for the units you don't need; don't leave them blank.

**Leaving `alert-send-how-many` blank or omitting the repeat cap.** For recurring alerts, always set `repeat-for-max`. Without it, REDCap sends indefinitely.

---

## 7.2 Automated Survey Invitations (ASI)

**Location:** Online Designer → "Automated Survey Invitations" button (project-level, not per-instrument).

**What it does:** Exports all ASI configurations for the project as a CSV and allows re-importing them — useful for copying a complex invitation schedule from one project to another or for batch-editing invitation logic outside of REDCap.

**Upload behavior:** Additive/update.

**Rights required:** Project Design and Setup (at least one survey must be enabled in the project).

**Full details:** RC-SURV-06 — Automated Survey Invitations (ASI)

---

## 7.3 Survey Queue

**Location:** Online Designer → Survey Queue → "Upload or download survey queue" option.

**What it does:** Exports the survey queue configuration as a CSV and allows re-importing it. The survey queue defines the order and conditional logic governing which surveys are presented to a participant after completing a prior survey.

**Upload behavior:** Additive/update.

**Rights required:** Project Design and Setup.

**Columns (8):**

| Column | Notes |
|---|---|
| `form_name` | Instrument unique name |
| `event_name` | Event unique name (longitudinal only; blank for classic projects) |
| `active` | `1` = activated in queue; `0` = deactivated |
| `condition_surveycomplete_form_name` | Completion trigger — which survey must be completed first. Blank for logic-only triggers. |
| `condition_surveycomplete_event_name` | Event of the completing survey. May reference an event from a different arm. Blank for logic-only triggers. |
| `condition_andor` | `AND` or `OR`. **Always populate**, even when only one trigger type is used. |
| `condition_logic` | Branching logic expression. Cross-event format: `[event_name][field_name]`. Blank for completion-only triggers. |
| `auto_start` | `1` = auto-start to next survey; `0` = return to queue overview |

**Full details:** RC-SURV-07 — Survey Queue

---

## 7.4 Survey Settings

**Location:** Online Designer → "Survey Settings" button (project-level, not per-instrument).

**What it does:** Exports the survey settings for all survey-enabled instruments in the project as a CSV and allows re-importing them. This is useful for replicating settings (e.g., auto-continue, response limits, custom completion text) across projects without reconfiguring each instrument manually.

**Upload behavior:** Additive/update — imported settings overwrite the current settings for the instruments specified in the file.

**Rights required:** Project Design and Setup (at least one survey must be enabled in the project).

**Full details:** RC-SURV-02 — Survey Settings: Basic Options & Design

---

## 7.5 Form Display Logic

**Location:** Online Designer → Form Display Logic → "Upload or download form display logic" option.

**What it does:** Exports the Form Display Logic (FDL) configuration for a project as a CSV and allows re-importing it. FDL controls which entire instruments are enabled or disabled to users based on field values or user attributes — distinct from branching logic, which operates at the field level.

**Upload behavior:** Additive/update — imported rules replace or update the existing FDL configuration.

**Rights required:** Project Design and Setup.

**Full details:** RC-FDL-01 — Form Display Logic

### Column Reference

The FDL CSV always has exactly six columns in this order:

| Column | Required | Accepted Values | Notes |
|---|---|---|---|
| `form_name` | Yes | Any valid instrument name (internal name, no spaces) | Must match the instrument's `form_name` exactly as it appears in the Data Dictionary. |
| `event_name` | No | A valid unique event name, or blank | Leave blank to apply the condition to **all events** where the form appears. In classic (non-longitudinal) projects this column is always blank. |
| `control_condition` | Yes | Any valid REDCap logic expression | Same syntax as branching logic. When the expression evaluates to true the form is enabled; when false the form is disabled. |
| `apply_to_data_entry` | Yes | `y` or `n` (lowercase) | `y` — the condition controls whether the form is accessible in the standard data entry UI. |
| `apply_to_survey_autocontinue` | Yes | `y` or `n` (lowercase) | `y` — the condition also controls Survey Auto-Continue behavior for this instrument. |
| `apply_to_mycap_tasks` | Yes | `y` or `n` (lowercase) | `y` — the condition controls whether this instrument appears as a task in MyCap. |

> **Flag values are lowercase.** REDCap exports and expects `y`/`n`, not `Y`/`N`. Using uppercase will cause the import to fail.

> **Multiple rows for the same form use OR logic.** If the same instrument appears in two rows, the form is enabled when *either* condition is true. To require multiple simultaneous conditions, combine them with `and` in a single `control_condition` cell.

### Annotated Example

The file below comes from a classic project where two baseline forms are enrolled in FDL solely to suppress them as MyCap tasks, without restricting data entry access.

```csv
form_name,event_name,control_condition,apply_to_data_entry,apply_to_survey_autocontinue,apply_to_mycap_tasks
demographics,,"[record_id]<>""""",y,y,n
contact_info,,"[record_id]<>""""",y,y,n
```

**`demographics` row:**
- `event_name` is blank → the condition applies at every event where the form appears.
- `control_condition` is `[record_id]<>""` — always true for any saved record, so data entry is never blocked.
- `apply_to_data_entry=y`, `apply_to_survey_autocontinue=y` — the always-true condition keeps both enabled.
- `apply_to_mycap_tasks=n` — MyCap task visibility is excluded from FDL control; the form's MyCap task state is governed separately.

**`contact_info` row:** identical pattern applied to a second instrument.

**Why enroll a form in FDL with an always-true condition?** This pattern is used when you only want to set one or two flags (such as `apply_to_mycap_tasks=n`) without actually restricting data entry. It is also useful as a placeholder row you plan to tighten later.

**Note on the raw CSV escaping.** The condition `[record_id]<>""` (comparing against an empty string) exports as `"[record_id]<>""""`  in the raw file. The outer double-quotes delimit the CSV cell; the inner `""` is the CSV escape for a literal `"` character. Spreadsheet applications display this correctly as `[record_id]<>""`. If you edit the file in a plain text editor or parse it programmatically, account for standard CSV double-quote escaping — writing the wrong number of quotes will cause the import to fail or the logic to behave unexpectedly.

### Common Mistakes

**Using uppercase `Y`/`N` for flags.** REDCap exports lowercase `y`/`n` and expects the same on import. Uppercase values will cause the row to be rejected.

**Editing empty-string conditions in a plain text editor.** Conditions like `[record_id]<>""` are double-escaped in the raw CSV (`""""`). Editors that don't respect CSV quoting rules will corrupt the escaping and break the logic on re-import.

**Leaving `event_name` blank unintentionally.** A blank event_name applies the condition to *every* event where the form appears. If you only intended to restrict one event, specify the event name explicitly.

**Expecting AND behavior from multiple rows.** Two rows for the same form combine with OR — the form is enabled if either condition is true. To enforce multiple simultaneous requirements, write them as a single `control_condition` joined by `and`.

**Using `[user-role-id]` in conditions for projects that may be copied.** Role IDs are installation-wide and change when a project is duplicated. Use `[user-role-name]` instead; role names are preserved on copy.

---

## 7.7 Data Quality Rules

**Location:** Applications → Data Quality → "Upload or download rules" option.

**What it does:** Allows bulk management of custom Data Quality rule definitions. Rules can be exported from one project and imported into another, or edited outside REDCap and re-uploaded.

**Upload behavior:** Additive/update.

**Rights required:** Project Design and Setup.

**Full details:** RC-DQ-01 — Data Quality Module

---

## 7.8 Multi-Language Management (Language Setups)

**Location:** Applications → Multi-Language Management → upload/download controls per language.

**What it does:** Exports translated field labels, choices, and other text strings for a given language as a CSV file. The translated file can be edited externally and re-imported, making it practical to send translations to an external translator without giving them REDCap access.

**Upload behavior:** Updates the translation strings for the specified language.

**Rights required:** Project Design and Setup.

**Full details:** RC-MLM-01 — Multi-Language Management

---


## 7.10 Randomization Allocation Table

**Location:** Applications → Randomization → (select model) → Upload Allocation Table.

**What it does:** Uploads the randomization allocation table — the pre-generated schedule that defines which treatment arm each randomized subject receives. The allocation table is produced externally by a statistician and uploaded to REDCap before randomization begins.

**Upload behavior — Replace:** The uploaded file replaces the current allocation table for that model. Once randomization has begun, the table is locked and cannot be replaced without resetting randomization (which requires administrator involvement).

**Rights required:** Randomization Setup rights.

**Full details:** RC-RAND-02 — Randomization Setup Guide

---

# 8. What Cannot Be Uploaded via CSV

The following are download-only or not file-based:

- **Survey Participant List** — The participant list (Survey Distribution Tool) can be exported to CSV and supports copy-pasting a list of participants to add them, but there is no CSV file upload path for participants.
- **Logging** — Logging records can be downloaded as CSV for audit purposes, but there is no upload path.
- **Repeating Instruments/Events configuration** — Which instruments or events are set as repeatable is configured through the UI popup in Project Setup, not via CSV. This configuration can be managed via API (RC-API-51, RC-API-53) but not through a file upload in the UI.
- **Report definitions** — Custom reports are created and managed in the UI only. There is no CSV export/import for report configurations.

---

# 9. Common Questions

**Q: Which CSV uploads replace the existing configuration, and which just add to it?**

**A:** The table in Section 2 lists the behavior for every upload. The critical ones to remember are the two that **replace**: the Data Dictionary (replaces all instruments and fields) and the Instrument–Event Mapping (replaces the entire designation matrix). Every other CSV upload is additive or update-only. For the two replace-type uploads, always download the current version first so you can recover from an unintended change.

**Q: Can I use these CSV uploads to copy a project setup from one project to another?**

**A:** For most configuration areas, yes — download the CSV from the source project, then upload it into the target project. This works well for Arms, Events, Instrument–Event Mappings, Alerts, Data Quality Rules, User Roles, and DAG definitions. For the Data Dictionary, you can also download from one project and upload to another, but be aware that branching logic referencing specific event names or variable names will need to be validated after the upload. For a full project copy including all data, use the XML backup feature (Project Setup → Other Functionality → Copy or back up the project).

**Q: Is there a way to undo a CSV upload?**

**A:** There is no undo button. For replace-type uploads (Data Dictionary, Instrument–Event Mappings), the recovery path is to re-upload the version you downloaded before making changes — which is why downloading a backup first is essential. For additive uploads (Arms, Events, Users, DAGs), reverting means manually removing the items that were added.

**Q: Do CSV uploads go through the change review queue in Production mode?**

**A:** It depends on the feature. Data Dictionary uploads in Production mode go through the same change queue review process as Online Designer changes — they are not live until a project administrator approves them. Most other CSV uploads (Users, DAGs, Alerts, Data Quality Rules, etc.) take effect immediately regardless of project mode, because they do not modify instrument or field definitions.

**Q: What columns do I need in my CSV file for a record data import?**

**A:** The minimum required column is the Record ID. If your project is longitudinal, you must also include `redcap_event_name`. If you have repeating instruments or events, add `redcap_repeat_instrument` and `redcap_repeat_instance`. If you are assigned to a Data Access Group, add `redcap_data_access_group`. The Data Import Tool provides a download template with the correct column structure for your specific project — use that template as a starting point rather than building a CSV from scratch.

**Q: Can I import a file exported from REDCap directly back into the same project without any changes?**

**A:** Yes. Any CSV file exported from REDCap's data export feature can be re-imported directly into the same project without modification. The column structure will be correct, including all required fields and event names. This is useful for recovering from accidental deletions, sharing participant data with external analysts (who can make edits and return the file), or migrating records between projects with the same structure.

---

# 10. Common Mistakes & Gotchas

**Uploading instrument–event mappings without downloading first.** This upload replaces the entire mapping. Building a file from scratch and uploading it will uncheck every mapping not in the file — potentially deleting data for instrument–event combinations that had records. Always start from a downloaded export of the current mapping.

**Manually typing unique event names in instrument–event mapping files.** REDCap's unique event name generation algorithm removes hyphens rather than converting them to underscores. An event labeled "Follow-up" becomes `followup_arm_1`, not `follow_up_arm_1`. Hand-typed names that don't match exactly will cause the mapping to silently fail (the event simply won't be found). Always copy unique event names from a downloaded Events CSV or from the Define My Events page.

**Uploading events before arms in a multi-arm project.** Events reference arm numbers — if the arm doesn't exist yet, REDCap cannot assign the event correctly. For multi-arm projects, always upload in order: arms → events → instrument–event mappings.

**Uploading a Data Dictionary without a backup.** The Data Dictionary upload replaces your entire instrument configuration. If you accidentally omit rows (e.g., by filtering your spreadsheet), those variables and their data are deleted on upload. Always save a dated snapshot before editing.

**Assuming "Upload File" in the Data Import Tool saves the data.** The upload step only stages a preview. The data is committed only after you scroll down and click "Import Data" at the bottom of the results screen. If you navigate away after clicking "Upload File," nothing is saved.

**Including read-only system columns when re-importing an export.** REDCap data exports include several columns that cannot be written back via the Data Import Tool: `redcap_survey_identifier` (survey participant identifier) and any `*_timestamp` column (e.g., `screening_timestamp`, `demographics_timestamp`). These are auto-generated by REDCap and are silently ignored on import — they will not cause an error, but they also cannot be set or overwritten this way. When building an import file from a full export, it is safe to leave these columns in; just be aware their values have no effect.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic alternatives to the CSV uploads described in this article. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

Most CSV upload features in REDCap have a corresponding API method that achieves the same result without a file upload. The API is especially useful for automation, scripted project setup, and system-to-system integration.

| **Feature** | **Export** | **Import** | **Delete** |
|---|---|---|---|
| Data Dictionary | RC-API-07 | RC-API-08 | — |
| Arms | RC-API-16 | RC-API-17 | RC-API-18 |
| Events | RC-API-19 | RC-API-20 | RC-API-21 |
| Instrument–Event Mappings | RC-API-10 | RC-API-11 | — |
| Repeating Instruments/Events *(API only — no UI upload)* | RC-API-51 | RC-API-53 | — |
| Record Data | RC-API-02 | RC-API-03 | RC-API-04 |
| Users | RC-API-22 | RC-API-23 | RC-API-24 |
| User Roles | RC-API-25 | RC-API-26 | RC-API-27 |
| User–Role Assignments | RC-API-55 | RC-API-56 | — |
| DAGs | RC-API-28 | RC-API-29 | RC-API-30 |
| User–DAG Assignments | RC-API-31 | RC-API-32 | — |
| Survey Participants *(export only in UI)* | RC-API-43 | — | — |

> **No API equivalent:** Alerts & Notifications, Automated Survey Invitations, Survey Queue, Survey Settings, Form Display Logic, Data Quality Rules, Multi-Language Management, and Randomization Allocation Tables do not have dedicated API methods. These must be managed through the REDCap UI or CSV upload/download.

---

# 11. Related Articles

- RC-IMP-01 — Data Import Overview (overview of all import mechanisms including XML and zip files)
- RC-FD-03 — Data Dictionary (complete Data Dictionary reference)
- RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques (column-by-column DD format reference)
- RC-LONG-01 — Longitudinal Project Setup (arms, events, and instrument–event mapping uploads)
- RC-USER-02 — User Rights: Adding Users & Managing Roles (bulk user management)
- RC-DAG-01 — Data Access Groups (bulk DAG and user–DAG assignment management)
- RC-ALERT-01 — Alerts & Notifications: Setup (alert configuration and bulk upload)
- RC-DQ-01 — Data Quality Module (data quality rule upload/download)
- RC-MLM-01 — Multi-Language Management (language CSV upload workflow)
- RC-RAND-02 — Randomization Setup Guide (allocation table upload)
