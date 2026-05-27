# KB Consistency Review — 2026-05-27

A balanced-strictness review of the REDCap KB for **logical inconsistencies and contradictions**, covering both intra-article and inter-article issues. The review was carried out by topic cluster across ~240 articles. Findings below are grouped by severity, then by topic.

- **Strictness:** Balanced — clear factual contradictions, mismatched definitions, conflicting guidance. Pure wording variation excluded.
- **Scope:** Intra-article and inter-article.
- **Verification:** Highest-impact items were spot-checked against the source text. A handful of agent-flagged items were re-read and dropped when they turned out to be wording, not contradiction.

---

## Summary

| Severity | Count |
|---|---|
| Hard contradictions (verified) | 14 |
| Inconsistencies / terminology drift | 16 |
| Intra-article issues | 17 |

Topic clusters with the densest issues: **Repeating instruments/events**, **User Rights + DAGs**, **Survey/e-Consent**, **Multi-Language Management**.

---

## 1. Hard contradictions

These are cases where two pieces of the KB make factually opposed claims about the same behavior. Reading one would lead a user to a different action than reading the other.

### Logic syntax

- **`[RC-BL-03] §3.5 "Always-True AND Statements"`** opens with "*a statement that is always true, causing the field to always show regardless of data values*" and gives `[age]>=35 and [age]<=35` as the example. The very next inline comment correctly notes "*Only true when age = exactly 35*". The section heading and intro describe an always-true result that the example does not produce. The corresponding **§4.4 "Always-True OR Statements"** uses the same expression with `or` and is correct. The AND example is logically wrong — it would need to be retitled or replaced with a tautological AND.

- ✅ **`[RC-AT-09] §4.4`** shows the example `@CALCDATE(today, 14, 'd')` (unquoted `today`) and calls `now`/`today` "**keywords**". **`[RC-CALC-01] §11`** states "*The literals `'today'` and `'now'` (in single quotes) can be used in `datediff()`, `dayoftheweek()`, `year()`, `month()`, and `day()`*". The two articles disagree on whether these literals must be single-quoted. *(Fixed 2026-05-27: RC-AT-09 §4.4 example updated to `@CALCDATE('today', 14, 'd')`; "keywords" changed to "literals (in single quotes)"; §7 gotcha updated to consistent quoted form.)*

### Piping / Smart Variables

- **`[RC-PIPE-02] §4.2`** says "*It is possible to pipe a value out of a repeated instrument or repeated event using two methods*" and provides full syntax. **`[RC-PIPE-02] §6 Common Questions`** then answers "*Q: Can I pipe a value from a repeated instrument into a regular instrument? A: No — this is not currently supported … The result will be blank or unpredictable*". The same article enables and forbids the same capability.

- **`[RC-PIPE-10] §3`** says `[next-instance]` "*Returns blank if this is the last existing instance and no future instances have been created*". **`[RC-PIPE-10] §4`** says "*If there is no next instance yet (the user is viewing the last instance), `[next-instance]` still returns a valid number but there may be no data in that instance.*" Blank vs. a valid number — direct intra-article contradiction.

- **`[RC-PIPE-10] §5 Q "How do I create a link to the next instance of a repeating survey?"`** uses `[survey-link:daily_log:Fill out tomorrow's log][next-instance]`. **`[RC-PIPE-10] §3 / §6`** reserve that use case for `[new-instance]` and explicitly say `[next-instance]` is only for existing instances. Mixed guidance on which smart variable to use for "link to upcoming instance".

### Longitudinal / Repeating

- **`[RC-LONG-02] §2 Key Concepts ("Instance")`** says "*Instance numbers are assigned sequentially **and do not reset between events***". **`[RC-LONG-02] §9`** answers "*Does the instance counter reset between events? … Instance numbering for repeated instruments is independent per instrument per event. **Each event's repeated instrument starts fresh at instance 1.***" The article defines the same behavior two opposite ways.

- ✅ **`[RC-LONG-01] §5`** warns "*Unchecking an instrument-event combination that already contains saved data will permanently delete that data*". **`[RC-IMP-09] §4`** says "*If records exist for a removed combination, that data becomes inaccessible (though it is not deleted from the database)*". One says permanent deletion, the other says retained-but-inaccessible — different data-loss models. *(Fixed 2026-05-27: RC-LONG-01 §5 critical callout updated to "inaccessible but not deleted from the database"; added recovery note, collision warning for re-mapped combinations with new data, and advice to contact the local REDCap admin if unsure.)*

- ✅ **`[RC-LONG-01] §2 / §6.1 events CSV`** states `day_offset` is "Integer ≥ 0" and `offset_min`/`offset_max` are "Expressed as a positive number". **`[RC-API-19] §4 / §5`** shows `"offset_min": -3` in an example response and describes the window as "*±3 days*". The CSV doc forbids what the API doc shows. *(Fixed 2026-05-27: RC-LONG-01 §6.1 `offset_min` note updated to explain CSV uses positive numbers and API returns negative integers, with conversion guidance. RC-API-19 "What do the offset fields mean?" Q&A updated to flag the same format difference and instruct users to convert when building a CSV from API output.)*

- **`[RC-LONG-01] §2`** derives unique event names as "*lowercase the event label, remove hyphens entirely … replace all remaining non-alphanumeric characters with underscores*", giving "Follow-up 30 min" → `followup_30_min_arm_1`. **`[RC-LONG-01] §6.1`** describes the rule narrower: "*REDCap lowercases the event name, **replaces spaces with underscores**, removes hyphens … then appends `_arm_{N}`*" — with no general non-alphanumeric rule. The two algorithms produce different results for labels with commas, slashes, parentheses, etc.

- ✅ **`[RC-API-17] §1`** says Import Arms "*is only available for projects in **Development status**. It will not work on projects in Production or Analysis/Cleanup status*". **`[RC-LONG-01] §11`** says "*When the setting is enabled, project-level users with Project Design and Setup rights can add events and modify certain event properties directly on a Production project*". UI says yes (with admin toggle), API says no. *(Fixed 2026-05-27: clarified in both articles that the admin setting applies to UI editing only; Import Arms and Import Events API endpoints remain Development-only regardless. Note added in RC-API-17 §1, §5 Q&A, and RC-LONG-01 §11.)*

### Surveys / e-Consent

- ✅ **`[RC-SURV-03] §5.5`** says about the e-Consent Framework "*you must collect the participant's name and signature*" and treats signature as required. **`[RC-SURV-08] §4.1`** marks the **Signature** field as "**Optional** but strongly recommended". Direct contradiction on whether a signature field is required to use the e-Consent Framework. *(Fixed 2026-05-27: RC-SURV-03 §5.5 updated to say name is required and signature is "optional but strongly recommended"; added pointer to RC-SURV-08 for full field requirements.)*

### Form design / Data entry

- ⚠️ **`[RC-FD-02] §4.1`** says you can "*Delete an instrument (only if it contains no data).*" **`[RC-FD-06] §5.4`** says "*Deleting an instrument permanently deletes the instrument itself and all data collected for any records in that instrument. This action cannot be undone.*" One says blocked when data exists, the other says allowed and destructive. *(Deferred 2026-05-27: instrument deletion blocking behavior could not be confirmed from KB sources alone — RC-FD-02's "only if no data" phrasing is ambiguous (guideline vs. hard block). Needs manual verification against REDCap before editing RC-FD-06 §5.4.)*

- ✅ **`[RC-FD-06] §6.3`** says of field delete: "*Permanently deletes the field and all data collected in records for that field. Use with caution when real data exists.*" **`[RC-FD-11] §2.3`** and **`[RC-FD-02] §4.2`** say "*Irreversible; fields with data in Production cannot be deleted*" and "*(only if the project is in Development mode, or if the field contains no data)*". One says you can delete fields-with-data in Production; the other two say REDCap blocks it. *(Fixed 2026-05-27: RC-FD-06 §6.3 Delete table row updated to explicitly state Production blocks deletion of fields with data; Development allows immediate permanent deletion.)*

- ✅ **`[RC-DE-02] §7`** says "*Every instrument has four save options at the bottom of the page*" and lists four. **`[RC-DE-11] §4`** documents **nine** save buttons (incl. Save & Go To Next Form, Save & Mark Survey as Complete, Save & Go To Next Instance, Save & Add New Instance, Cancel). `[RC-DE-04] §3.1 / §5.3` repeats the "four options" framing. Users following the basic article will look for four buttons and overlook the rest. *(Fixed 2026-05-27: RC-DE-02 table heading changed from "four save options" to "core save options"; note added below the table pointing to RC-DE-11 for the full reference and naming the additional context-specific buttons; inline "four save buttons" mentions changed to "save buttons". RC-DE-04 both instances of "four save options" changed to "available save options".)*

### User Rights / DAGs

- ✅ **`[RC-DAG-01] §2`** says "*A user can be in at most one DAG at a time as their primary assignment. Users with the DAG Switcher feature enabled can also be granted access to multiple DAGs*", and **`[RC-DE-09] §4`** describes multi-DAG users as a normal scenario. **`[RC-API-31] §6`** and **`[RC-API-32] §7`** flatly say "*Can a user be assigned to multiple DAGs? **A: No.** Each user can be assigned to at most one DAG. If a user needs multi-DAG access, they must be assigned no DAG (empty value) to gain all-DAG view permissions*". The UI articles describe DAG Switcher as the supported multi-DAG mechanism; the API articles deny multi-DAG assignment exists and recommend the opposite workaround. *(Fixed 2026-05-27: RC-API-31 §6 and RC-API-32 §7 Q&A updated to acknowledge the DAG Switcher as the UI-based multi-DAG mechanism, clarify that this endpoint manages primary assignments only and does not expose Switcher assignments, and retain the empty-value workaround for all-DAG access.)*

- ✅ **`[RC-LOCK-01] §6.4`** says e-signature "*is not compatible with institutions using Shibboleth (SAML) or OAuth2 … the e-signature option will not be available to your users*" (hard unavailable). **`[RC-USER-03] §3.5`** describes it as "*known compatibility issues with certain SSO authentication methods. Confirm compatibility …*" (test it). Categorically different system behavior — hard-blocked vs. unreliable. *(Fixed 2026-05-27: RC-USER-03 §3.5 and gotchas updated to name Shibboleth/OAuth2 as hard-incompatible, explain the technical reason, and note that external modules exist that provide alternative e-signature workflows compatible with federated authentication.)*

### Multi-Language Management

- **`[RC-MLM-01] §1`** says "*MLM covers field labels, choice labels … but it does **not** translate content automatically. All translations must be provided by the project team.*" The same article's **§5.9** then documents a "**Translate using AI**" button that fills in translations automatically, and **`[RC-AI-03] §1`** describes the same feature. The overview denies a capability the article itself documents.

- **`[RC-CC-20] §2.1 / §5`** treats **Base Language** and **Fallback Language** as one and the same ("*the fallback language*"). **`[RC-MLM-01] §2`** defines them as distinct layers: the **Base Language** is the UI source; the **Fallback Language** is what shows when an active language is missing a translation; if the fallback is also missing, REDCap falls back to the base. CC-20 collapses two layers the per-project article keeps separate.

- **`[RC-MLM-01] §2 Active Language`** says "*only active languages appear in language selectors*". **`[RC-CC-20] §5`** says "*A language can be active but not visible (users cannot see it to select), or visible but not active (users can select it but it will not work)*" — i.e., Active and Visible are orthogonal. The two articles describe different models.

---

## 2. Inconsistencies and terminology drift

Clear mismatches that aren't full contradictions but will cause confusion.

### Logic syntax

- **Checkbox comparison style.** `[RC-BL-04] §5.2 / §7` insists "*it must be `[conditions(1)]='1'`. Without the parentheses and raw value, the logic will not reference any checkbox sub-variable.*" `[RC-BL-01] §9.1` uses the unquoted form `[gate_field(1)]=1`, `[join_checkbox(1)] = 1`. Both work per `[RC-BL-02] §3.3`, but the design-pattern article diverges from the form taught as canonical.

- **`@NONEOFTHEABOVE` quoting.** `[RC-AT-04] §2` documents `@NONEOFTHEABOVE='99'` and `@NONEOFTHEABOVE=99` side by side. The rest of the AT series treats quoting raw values as required. Only AT-04 documents the unquoted alternative.

### Piping / Smart Variables

- **Modifier vs. qualifier.** `[RC-PIPE-03] §6` says "*piping modifiers (`:value`, `:label`, `:checked`, …) are suffixes appended to a regular variable name … Some smart variables are used as qualifiers (prefixed before a variable name…) but are still distinct from modifiers*". `[RC-PIPE-10] §2` defines "**Instance Qualifier** — A smart variable used as a **suffix or modifier** …". Terms used inconsistently across articles.

- **"Smart Functions / Smart Charts" vs. "Aggregate Functions".** `[RC-PIPE-11]` uses "Smart Functions / Charts" framing; `[RC-PIPE-03] §3.7` and `[RC-PIPE-15] §4` use "Aggregate Functions, Charts, and Tables". Same family, two umbrella terms.

- **Branching logic value of checkboxes.** `[RC-PIPE-04] §6` says "*REDCap uses the **raw coded value** — not the display label*" with no qualification. `[RC-PIPE-02] §5.3` and `[RC-PIPE-01] §8` show checkbox piping returns "Checked"/"Unchecked" text — the no-modifier branching value for checkboxes is not a raw coded value. PIPE-04 should flag the checkbox exception.

### Longitudinal / Repeating

- **Cross-event / cross-instance referencing — "supported" vs. "not reliable".** `[RC-BL-05] §5.3` introduces the instance-qualified form `[event_name][variable_name][instance_number]` and shows working examples. `[RC-LONG-02] §8.1` says "*cross-instance and cross-event references from within a repeated instrument are not reliably supported*" and tells designers not to depend on them. Same feature, opposite advice.

- **`format` parameter — "Required" vs. "Optional".** `[RC-API-19] §2` and `[RC-API-20] §2` list `format` as "**Required**" with "*Default is `'xml'`*" in the same row. `[RC-API-16] §2` correctly marks it "**Optional**". Inconsistent across sibling endpoints.

### Surveys

- **Survey Access Code — shortcut or authentication token?** `[RC-SURV-01] / [RC-SURV-04]` describe the Survey Access Code as an optional shortcut alternative to the URL. `[RC-IMP-07] §3` describes `survey_auth_enabled_single` as "*Require participants to enter a survey access code before viewing the survey. Access codes are generated per-participant via the Participant List*" — turning it into a mandatory authentication gate. CSV reference conflates the concept.

- **Participant Identifier — toggle or not?** `[RC-SURV-05] §3.3` says the identifier feature must be turned on via an **Enable** button in the column header. `[RC-SURV-04] §4.3` and `[RC-SURV-05] §3.1` describe identifier setup as "add a participant identifier or designate an email field" with no mention of an enable toggle.

- **ASI Timing Modes coverage gap.** `[RC-SURV-06] §4.3` lists four delay options; `[RC-IMP-06] §3` exposes a fifth, `NEXT_OCCURRENCE`, that the UI article does not describe.

### Export

- **De-identified rights description.** `[RC-EXPRT-03] §3` says the De-identified rights level removes "*all free-form text fields, date/time fields, and identifier-flagged fields automatically*". `[RC-EXPRT-04] §3.2` clarifies the actual rule is "*Remove unvalidated Text fields … Validated text fields (e.g., those with date, number, or email validation) are still included.*" EXPRT-03 overstates what is removed.

- **Export-rights level naming.** `[RC-EXPRT-03] §3` calls the third level **"Remove All Identifier Fields"**. `[RC-USER-03] §5` calls the same level **"Remove Identifier Fields Only"**. Same menu item, two different display names across articles.

- **CSV delimiter options.** `[RC-API-02] §2` lists five CSV delimiters (`,`, `tab`, `;`, `|`, `^`). `[RC-IMP-01] §8.1` lists only three (Comma / Tab / Semicolon). The API supports more than the UI, but neither article flags the difference.

### User Rights / DAGs

- **`data_export` vs `data_export_tool`.** `[RC-API-22]` (Users) uses `data_export`; `[RC-API-26]` (Roles) uses `data_export_tool`. RC-API-26's own Common Mistakes note acknowledges the divergence ("*roles use `data_export_tool` while users use `data_export`*") — so this is a documented quirk in REDCap itself, but the inconsistency between sibling endpoints is real and a common source of import errors.

- **Logging — accepted `logtype` values.** `[RC-LOG-01] §5.2` lists one set (`record_add`, `record_edit`, `record_delete`, `lock_record`, `page_view`, …). `[RC-API-39] §3` adds `'record'` and uses slightly different forms. API consumers can't tell whether `'record'` is valid from either article alone.

- **Users-export columns.** `[RC-USER-02] §7.1` documents `data_access_group_id` and `data_access_group_label` columns. `[RC-API-22] §5.1` lists only `data_access_group`. Same export, two different column schemas.

### MyCap / Mobile

- **Push notification time — configurable or not?** `[RC-MYCAP-01] §7` lists "Push notification scheduling" under "MyCap Limitations" / unsupported. `[RC-MYCAP-03] §6` and `[RC-MYCAP-05] §3.5` say the notification time can be configured project-wide. The limitations table conflates "per-participant configurability" (unsupported) with "configurability at all" (supported project-wide).

- **App Link domain.** `[RC-MYCAP-04] §2` uses `app.projectmycap.org`. `[RC-PIPE-16] §3` example output uses `https://mycap.link/join/…`. Two different domains documented for the same `[mycap-participant-url]` output.

- **Mobile App action tag count.** `[RC-AT-11] §1` says "REDCap provides **three** action tags designed exclusively for use in the REDCap Mobile App" (`@APPUSERNAME-APP`, `@BARCODE-APP`, `@SYNC-APP`). `[RC-MOB-01] §15` lists five, adding `@HIDDEN-APP` and `@READONLY-APP`.

### Control Center

- **System-wide upload size default.** `[RC-CC-05]` says "*The server default is typically 1024 MB unless changed*". `[RC-CC-24] §9` gives the "*Typical global default*" of **128 MB** for the same setting. Order-of-magnitude disagreement on the effective default.

- **`0` semantics for Record Limit.** `[RC-CC-02]` says "*A value of `0` means no limit*" (global). `[RC-CC-24] §9` says project-level `0` means "*use global default*". Same sentinel, two definitions; combining both descriptions gives a contradictory cascade.

### Miscellaneous

- **Calendar export apps.** `[RC-CAL-01] §6` lists Google Calendar, Outlook, Office 365, Zoho, Apple Calendar. `[RC-CAL-01] §7 Q` drops Zoho. Minor intra-article list mismatch.

- **DET vs. ASI/Alert API triggering.** `[RC-API-01] §8` says flatly "*Can the API trigger the Data Entry Trigger (DET)? A: No.*" `[RC-API-01] §9` hedges for alerts: "*not triggered by API imports in the same way*". The hedge is harder to act on than the flat "No".

---

## 3. Intra-article issues (single-article inconsistencies)

Issues that live inside a single article and don't depend on cross-referencing.

- **`[RC-BL-03] §3.5`** — Heading and intro promise an always-true AND; example is not always-true. (See Hard Contradictions for detail.)
- **`[RC-AT-09] §4.4`** — Quoting convention for `today`/`now` is inconsistent inside the article and with `[RC-CALC-01]`.
- **`[RC-BL-05] §3 / §3.1`** — Defines cross-event prefix as a "different event" construct, then says the current event's name can also be used as a prefix. Needs a clarifying note.
- **`[RC-PIPE-02]`** — §4.2 documents piping out of repeated instruments; §6 denies it.
- **`[RC-PIPE-10]`** — §3 vs. §4 on `[next-instance]` return value; §5 Q recommends `[next-instance]` for "link to upcoming instance", §6 reserves that for `[new-instance]`.
- **`[RC-PIPE-16] §5`** — One Q&A answer ends mid-sentence: "*See [RC-INST-01 …]*" — the answer is truncated.
- **`[RC-LONG-02] §2 vs §9`** — Instance counter "does not reset between events" vs. "Each event's repeated instrument starts fresh at instance 1".
- **`[RC-LONG-03]`** — Section numbering is broken: `# 11 …` followed by `## 10.1`, `## 10.2`; `# 13 …` followed by `## 12.1`, `## 12.2`; `# 14 …` followed by `## 13.1`. Multiple heading-number/subsection-number mismatches.
- **`[RC-API-03] §2`** — Parameters table marks `type`, `overwriteBehavior`, `forceAutoNumber`, `backgroundProcess` as **Required** while documenting defaults for each. A required parameter does not have a default.
- **`[RC-API-23] §3.1 vs §5.1`** — Attribute reference uses canonical names (`lock_records_all_forms`, `lock_records`, `lock_records_customization`, `data_quality_create`, `logging`); code examples use different field names (`lock_record_multiform`, `lock_record`, `lock_record_customize`, `data_quality_design`, `data_logging`, `graphical`). Copy-pasted code will not match the documented schema.
- **`[RC-API-26] §2.1 vs §3.1`** — Python example sets `'data_access_group': 1`, contradicting the article's own claim (and `[RC-USER-02]`'s) that roles cannot carry a DAG.
- **`[RC-DAG-01] §6 vs [RC-DE-09] §4`** — DAG-01 says the Switcher does not override the primary DAG for record attribution; DE-09 says records created after switching are attributed to the active (switched-to) DAG.
- **`[RC-DDE-01] §4 vs §8`** — §4 defines deterministic visibility for DDE roles; §8 says visibility for unassigned users is "non-deterministic depending on REDCap version and configuration."
- **`[RC-NAV-REC-01] §4`** — Uses "Incomplete" to label both Grey (no data saved) and Red (saved but status not updated). `[RC-DE-02] §6` reserves "Incomplete" for Red only. Same article also overloads status codes 1 and 2 across form-status and survey-completion systems without distinguishing them.
- **`[RC-DE-02] §3.2 vs [RC-DE-05] §2 / §5`** — DE-02 implies min/max field validation is enforced ("REDCap enforces the format on save and shows an error"); DE-05 and FD-06 say min/max are "soft" warnings by default.
- **`[RC-DE-11] §3 vs §8`** — §3: floating save menu is "always visible while scrolling"; §8: floating menu "may not display every available option depending on screen size and context".
- **`[RC-RAND-03] §5.1`** — Note says "*A project with 2 cohorts and 2 stratification levels will have **4 rows per cohort combination, not 2***". Math is incoherent — 2 × 2 = 4 rows total, not "4 rows per cohort combination."
- **`[RC-PLUS-01] §6`** — Site-specific reference: "*Upon completing these steps, Vanderbilt generates a special license key*". Project convention is to keep KB content site-neutral; this should use a generic placeholder.

---

## 4. Suggested prioritization for fixes

Quick wins (low-effort, high impact):

1. ✅ **`[RC-BL-03] §3.5`** — Replace the broken AND example or retitle the section. *(Fixed 2026-05-27: section now leads with a correct OR tautology as the always-true example; the accidentally-equality AND pattern moved to a ⚠️ counterexample callout.)*
2. ✅ **`[RC-LONG-02] §2`** — Remove the "do not reset between events" sentence; it contradicts §9 and §9 is correct. *(Fixed 2026-05-27: sentence replaced with correct per-instrument-per-event wording.)*
3. ✅ **`[RC-PIPE-10] §3 vs §4`** — Reconcile `[next-instance]` return value (blank vs. valid number). *(Fixed 2026-05-27: table description updated to match §4 — returns a calculated number, not blank; Q&A updated to distinguish `[next-instance]` for existing instances vs. `[new-instance]` for not-yet-created instances.)*
4. ✅ **`[RC-API-03] §2`** — Mark `type`, `overwriteBehavior`, `forceAutoNumber`, `backgroundProcess` as Optional (they have defaults). *(Fixed 2026-05-27.)*
5. ✅ **`[RC-USER-03] §5`** — Rename "Remove Identifier Fields Only" to "Remove All Identifier Fields" to match the rest of the KB and the actual REDCap menu wording. *(Fixed 2026-05-27: all occurrences updated including table and Q&A.)*
6. ✅ **`[RC-RAND-03] §5.1`** — Fix the row-count math note. *(Fixed 2026-05-27: "4 rows per cohort combination" → "4 rows total (2 cohorts × 2 strata)".)*
7. **`[RC-PLUS-01] §6`** — ~~Replace "Vanderbilt" with a generic site placeholder.~~ *Not a fix — Vanderbilt owns REDCap and is the correct entity for license key generation.*

Medium-effort:

8. ✅ **`[RC-PIPE-02] §4.2 / §6`** — Reconcile piping-out-of-repeated guidance. *(Fixed 2026-05-27: removed the contradictory "No — not currently supported" Q&A from §6; the correct Q&A documenting Methods 1 and 2 was already present lower in the same section.)*
9. ✅ **`[RC-LONG-01] §2 / §6.1`** — Decide on one unique-event-name derivation rule and use it in both sections. *(Fixed 2026-05-27: §6.1 derivation rule updated to match §2 — "replaces spaces with underscores" expanded to "replaces all remaining non-alphanumeric characters with underscores, collapses consecutive underscores"; added a parenthetical example with special characters.)*
10. ✅ **`[RC-MYCAP-01] §7`** — Split "push notification scheduling" into "project-level (supported)" vs. "per-participant (unsupported)" rather than calling the whole feature unsupported. *(Fixed 2026-05-27: row label changed from "Push notification scheduling" to "Per-participant push notification time"; Notes updated to clarify project-wide time is configurable in App Settings.)*
11. ✅ **`[RC-MLM-01] §1`** — Drop the "all translations must be provided by the project team" line, since §5.9 documents AI-assisted translation. *(Fixed 2026-05-27: §1 overview and the "Does MLM auto-translate?" Q&A both updated to say "not by default" and to acknowledge the AI-assisted translation option when enabled by an administrator.)*

Cross-article reconciliation needed:

12. **DAG multi-assignment** — Decide whether DAG Switcher counts as multi-DAG; update `[RC-API-31]` and `[RC-API-32]` to match `[RC-DAG-01]` and `[RC-DE-09]`.
13. **e-Signature + SSO** — Pick "hard-blocked" or "known issues" and use that wording in both `[RC-LOCK-01]` and `[RC-USER-03]`.
14. **e-Consent signature requirement** — `[RC-SURV-03] §5.5` and `[RC-SURV-08] §4.1` need to agree on whether the Signature field is mandatory.
15. **Field/instrument deletion in Production** — `[RC-FD-02]`, `[RC-FD-06]`, `[RC-FD-11]` need a single, consistent description.
16. **Save button count** — `[RC-DE-02]` and `[RC-DE-04]` should defer to `[RC-DE-11]`'s nine-option reference rather than repeating "four save options".

---

## Notes on methodology

The review fanned out across 10 topic clusters (logic syntax; piping / smart variables; longitudinal / repeating; surveys / ASI / alerts; data import/export; user rights / DAGs / locking / logging; MyCap / mobile; Control Center / admin / external modules; form design / data entry / data quality; and miscellaneous including AI, MCP, randomization, texting, CDIS, DDP, MLM, calendar, ops, file repository). Each cluster was reviewed for both intra- and inter-article issues at balanced strictness. The highest-impact items were verified against the source text before inclusion. A handful of agent-flagged items were re-read and dropped when they turned out to be wording-only or self-corrected on closer reading (e.g., a flagged SPSS export-format issue, a `data_access_group` retention claim already addressed in the article's own Common Mistakes note).

Not reviewed in depth (low contradiction risk):
- Per-endpoint API articles (API-01..56) were scanned but treated as a single cluster for cross-article comparison rather than per-endpoint deep review.
- Template-scaffold articles (`RC-INST-01..03`, `RC-EM-02..04`) are placeholder content and were excluded from inter-article comparison.
