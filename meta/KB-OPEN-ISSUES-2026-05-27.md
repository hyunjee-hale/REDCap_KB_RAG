# KB Open Issues — as of 2026-05-27

All items from the [KB Consistency Review](KB-CONSISTENCY-REVIEW-2026-05-27.md) that have not yet been fixed. Hard contradictions are all resolved. Remaining work is in inconsistencies/terminology drift and intra-article issues.

**Note:** Several section 1 and section 3 entries in the review doc still lack ✅ markers even though the underlying issues were fixed (they were tracked in the prioritization list, not back-marked in the source sections). This list reflects actual fix status, not marker status.

---

## Section 2 — Inconsistencies / Terminology Drift (17 open)

### Piping / Smart Variables

1. ✅ **Branching logic value of checkboxes** — `[RC-PIPE-04] §6` says REDCap uses "the raw coded value" with no qualification. `[RC-PIPE-02] §5.3` and `[RC-PIPE-01] §8` show checkbox piping returns "Checked"/"Unchecked" text. PIPE-04 needs a checkbox exception note. *(Fixed 2026-05-27: added checkbox exception callout to §6)*

### Longitudinal / Repeating

2. ✅ **Cross-event / cross-instance referencing** — `[RC-BL-05] §5.3` shows working examples and presents the feature positively. `[RC-LONG-02] §8.1` says cross-instance references "are not reliably supported" and tells designers not to depend on them. Same feature, opposite advice. *(Fixed 2026-05-27: RC-LONG-02 §8.1 updated to correctly describe cross-instance referencing as supported, referencing RC-BL-05 §5.3 for full syntax)*

3. ✅ **`format` parameter — Required vs. Optional** — `[RC-API-19] §2` and `[RC-API-20] §2` list `format` as **Required** while documenting a default. `[RC-API-16] §2` correctly marks it **Optional**. Inconsistent across sibling endpoints. *(Fixed 2026-05-27: changed `format` to Optional in RC-API-19 §2 and RC-API-20 §2)*

### Surveys

4. ✅ **Survey Access Code — shortcut vs. authentication gate** — `[RC-SURV-01]` / `[RC-SURV-04]` describe the Survey Access Code as an optional shortcut. `[RC-IMP-07] §3` describes `survey_auth_enabled_single` as a mandatory authentication requirement. The CSV reference conflates the two uses. *(Fixed 2026-05-27: RC-IMP-07 updated — `survey_auth_enabled_single` now correctly described as Survey Login, a per-participant password gate, distinct from the Survey Access Code URL shortcut)*

5. ✅ **Participant Identifier toggle** — `[RC-SURV-05] §3.3` says the identifier feature must be enabled via a column-header button. `[RC-SURV-04] §4.3` and `[RC-SURV-05] §3.1` describe setup with no mention of an enable toggle. *(Fixed 2026-05-27: added Enable button callout to RC-SURV-05 §3.1 and RC-SURV-04 §4.3, including warning about Disable wiping identifiers)*

6. **ASI Timing Modes coverage gap** — `[RC-SURV-06] §4.3` lists four delay options. `[RC-IMP-06] §3` exposes a fifth (`NEXT_OCCURRENCE`) that the UI article does not describe.

### Export

7. **De-identified rights description** — `[RC-EXPRT-03] §3` says the De-identified level removes "all free-form text fields, date/time fields, and identifier-flagged fields." `[RC-EXPRT-04] §3.2` clarifies that validated text fields (date, number, email) are still included. EXPRT-03 overstates what is removed.

8. **CSV delimiter options** — `[RC-API-02] §2` lists five delimiters (`,` `tab` `;` `|` `^`). `[RC-IMP-01] §8.1` lists only three. Neither article flags the difference.

### User Rights / DAGs

9. **`data_export` vs. `data_export_tool`** — `[RC-API-22]` (Users endpoint) uses `data_export`; `[RC-API-26]` (Roles endpoint) uses `data_export_tool`. RC-API-26 acknowledges the divergence in its own Common Mistakes note but the asymmetry between sibling endpoints is undocumented in RC-API-22.

10. **Logging — accepted `logtype` values** — `[RC-LOG-01] §5.2` lists one set of values. `[RC-API-39] §3` adds `'record'` and uses slightly different forms. API consumers cannot tell from either article whether `'record'` is a valid value.

11. **Users-export columns** — `[RC-USER-02] §7.1` documents `data_access_group_id` and `data_access_group_label`. `[RC-API-22] §5.1` lists only `data_access_group`. Same export, two different schemas.

### MyCap / Mobile

12. **MyCap app link domain** — `[RC-MYCAP-04] §2` uses `app.projectmycap.org`. `[RC-PIPE-16] §3` example output uses `https://mycap.link/join/…`. Two different domains for the same `[mycap-participant-url]` output.

13. **Mobile App action tag count** — `[RC-AT-11] §1` says REDCap provides **three** mobile-exclusive action tags. `[RC-MOB-01] §15` lists five, adding `@HIDDEN-APP` and `@READONLY-APP`.

### Control Center

14. **System-wide upload size default** — `[RC-CC-05]` says the server default is typically **1024 MB**. `[RC-CC-24] §9` gives the typical global default as **128 MB**. Order-of-magnitude disagreement.

15. **`0` semantics for Record Limit** — `[RC-CC-02]` says a value of `0` means **no limit** (global setting). `[RC-CC-24] §9` says project-level `0` means **use global default**. Same sentinel, two definitions.

### Miscellaneous

16. **Calendar export apps** — `[RC-CAL-01] §6` lists Zoho Calendar; `[RC-CAL-01] §7 Q` drops it. Minor intra-article list mismatch.

17. **DET vs. ASI/Alert API triggering** — `[RC-API-01] §8` flatly says the API cannot trigger the Data Entry Trigger (DET). `[RC-API-01] §9` hedges for alerts: "not triggered by API imports in the same way." The hedge leaves API users without clear guidance.

---

## Section 3 — Intra-article Issues (10 open)

18. **`[RC-BL-05] §3 / §3.1`** — Defines cross-event prefix as a "different event" construct, then states the current event's own name can also be used as a prefix. Needs a clarifying note.

19. **`[RC-PIPE-16] §5`** — One Q&A answer ends mid-sentence: "*See [RC-INST-01 …]*" — the answer is truncated.

20. **`[RC-LONG-03]`** — Section numbering is broken throughout: `# 11` followed by `## 10.1`, `## 10.2`; `# 13` followed by `## 12.1`, `## 12.2`; `# 14` followed by `## 13.1`. Multiple heading/subsection number mismatches.

21. **`[RC-API-23] §3.1 vs §5.1`** — Attribute reference uses canonical field names (`lock_records_all_forms`, `data_quality_create`, `logging`); code examples use different names (`lock_record_multiform`, `data_quality_design`, `data_logging`, `graphical`). Copy-pasted code will not match the documented schema.

22. **`[RC-API-26] §2.1 vs §3.1`** — Python example sets `'data_access_group': 1`, contradicting the article's own claim (and `[RC-USER-02]`'s) that roles cannot carry a DAG assignment.

23. **`[RC-DAG-01] §6 vs [RC-DE-09] §4`** — DAG-01 says the Switcher does not override the primary DAG for record attribution (new records still go to the primary DAG). DE-09 says records created after switching are attributed to the switched-to DAG.

24. **`[RC-DDE-01] §4 vs §8`** — §4 defines deterministic visibility for DDE roles. §8 says visibility for unassigned users is "non-deterministic depending on REDCap version and configuration."

25. **`[RC-NAV-REC-01] §4`** — Uses "Incomplete" to label both Grey (no data saved) and Red (saved but status not updated). `[RC-DE-02] §6` reserves "Incomplete" for Red only. Also overloads status codes 1 and 2 across form-status and survey-completion systems without distinguishing them.

26. **`[RC-DE-02] §3.2 vs [RC-DE-05] §2 / §5`** — DE-02 implies min/max validation is enforced on save ("REDCap enforces the format on save and shows an error"). DE-05 and FD-06 say min/max are soft warnings by default.

27. **`[RC-DE-11] §3 vs §8`** — §3 says the floating save menu is "always visible while scrolling." §8 says it "may not display every available option depending on screen size and context."

---

## Housekeeping — ✅ markers missing in sections 1 and 3

These items were fixed (tracked in the prioritization list) but the corresponding entries in sections 1 and 3 of the review doc were not back-marked. Low priority but worth tidying in a future pass:

- Section 1: RC-BL-03, RC-PIPE-02, RC-PIPE-10 (×2), RC-LONG-02, RC-LONG-01 §2 derivation rule, RC-MLM-01 §1
- Section 2: Export-rights level naming (fixed via item 5), Push notification (fixed via item 10)
- Section 3: RC-BL-03, RC-AT-09, RC-PIPE-02, RC-PIPE-10, RC-LONG-02, RC-API-03, RC-RAND-03
