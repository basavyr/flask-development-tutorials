# SPS Auth Workflow - Issue Tracker

This file tracks bugs, issues, and feature requests for the SPS Auth Workflow application. The agent will automatically check this file at the start of each session and address any items marked as NOT COMPLETE.

---

## How to Add Issues

When adding a new issue, use the following format:

```
### [ISSUE-XXX] Brief title
**Status:** NOT COMPLETE
**Priority:** HIGH | MEDIUM | LOW
**Reported:** YYYY-MM-DD

Description of the issue, including steps to reproduce if applicable.
```

When an issue is resolved, the agent will update the status to COMPLETE and add resolution notes.

---

## Active Issues

*No active issues at this time.*

---

## Completed Issues

### [ISSUE-001] Password strength meter not shrinking on character deletion
**Status:** COMPLETE
**Priority:** HIGH
**Reported:** 2026-01-21
**Resolved:** 2026-01-21

The password strength meter bar was not shrinking when users deleted characters. Additionally, the bar was jumping between fixed widths (33%, 66%, 100%) instead of growing progressively.

**Resolution:** Updated `frontend/static/js/app.js` to calculate width dynamically based on character count (0-32 chars maps to 0-100%). Removed fixed widths from CSS classes in `frontend/static/css/style.css`. The bar now grows and shrinks smoothly with each keystroke.

---
