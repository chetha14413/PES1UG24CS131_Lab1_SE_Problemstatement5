# Lab 7 — Fuzz Testing for Input Validation Bugs

**Student:** Chetha Samrutha V  
**SRN:** PES1UG24CS131  
**Course repository:** `PES1UG24CS131_Lab1_SE_Problemstatement5`

## Objective

Use Hypothesis property-based fuzzing to discover edge-case input failures and harden the three functions supplied in the assigned blood-donation screening topic repository.

## Topic and functions

The supplied starter's Lab 7 files target:
1. `validate_blood_type` — ABO group and Rh factor parsing.
2. `calculate_pulse_pressure` — systolic/diastolic parsing and derived metrics.
3. `parse_donor_registry` — pipe-delimited donor data and eligibility classification.

## Files

| File | Purpose |
|---|---|
| `processor.py` | Hardened implementation of all three processors |
| `test_processor.py` | Hypothesis property-based tests and deterministic regression cases |
| `requirements.txt` | Python test dependencies |
| `LAB7_REPORT.md` | Method, findings, fixes, and execution record |
| `before/` | Original buggy starter and expected-to-fail fuzz tests for baseline comparison |\n| `RUN_LAB7.ps1` | PowerShell script to install dependencies and run before/after tests and the app |\n| `screenshots/` | Evidence screenshots to be captured from the student's terminal |

## Setup (Windows PowerShell)

From this folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run

```powershell
python processor.py
python -m pytest test_processor.py -v
```

For the interactive application, use valid demonstration entries such as `O+`, `120/80`, and `D001|65|13.2`. Try malformed values too, to see the defensive error messages.

## Validation rules implemented

- Only the eight standard ABO/Rh labels are accepted; whitespace and case are normalized.
- Blood pressure must have exactly two positive whole-number components, and systolic must exceed diastolic.
- Donor entries must contain exactly three fields, a non-empty ID, and finite positive numeric weight and hemoglobin values.
- Invalid input raises a consistent `ValueError`; the interactive runner catches it and continues to the next prompt.

## Evidence requirement

The lab handout asks for screenshots of (1) the starter run, (2) failing fuzz tests against the buggy starter, (3) the fixed program run, and (4) passing tests against the fixed program. The reference starter is retained in the topic repository. To produce genuine before-fix evidence, copy its original `processor.py` and starter `test_processor.py` into a temporary folder, complete tests there so they assert valid outcomes, then run pytest and capture its failures. Do not label fabricated output as a real run.

The current repository package includes a screenshot checklist and report template. Add actual terminal captures to `screenshots/` before final academic submission. Screenshots are not fabricated or represented as executed in this environment.
