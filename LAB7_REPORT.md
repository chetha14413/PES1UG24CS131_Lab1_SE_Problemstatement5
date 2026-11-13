# Lab 7 Report — Fuzz Testing for Input Validation Bugs

**Name:** Chetha Samrutha V  
**SRN:** PES1UG24CS131  
**Topic:** Blood Donation Screening  
**Technique:** Property-based fuzz testing with Hypothesis

## 1. Objective

The objective is to use fuzz testing to discover input-validation defects in three processors and then harden them against malformed and unexpected inputs.

## 2. Target functions

- `validate_blood_type`: normalizes and validates ABO/Rh codes.
- `calculate_pulse_pressure`: parses systolic/diastolic pressure and calculates pulse difference and ratio.
- `parse_donor_registry`: parses donor ID, weight, and hemoglobin and classifies the donor.

## 3. Fuzzing approach

Hypothesis strategies generate arbitrary strings, `None`, integers, lists, and structured valid values. The tests check that each processor either returns a result consistent with its contract or rejects malformed input using `ValueError`. Additional property tests check blood-group normalization, pressure arithmetic, and donor threshold decisions.

## 4. Defects addressed

| Function | Input risks in supplied starter | Defensive change |
|---|---|---|
| Blood type | `None`, empty text, missing/invalid Rh marker, unsupported antigen, extra characters | Type check and full-match validation against the eight supported ABO/Rh codes |
| Blood pressure | Missing or extra separators, non-numeric tokens, zero denominator, negative values, impossible ordering | Exact two-field parse, decimal integer validation, positive values, systolic greater than diastolic |
| Donor record | Missing/extra fields, empty ID, malformed numbers, NaN/infinity, non-positive values | Exact field count, ID validation, finite positive numeric checks |

## 5. Fix summary

The `before/` folder preserves the original buggy starter and includes dedicated Hypothesis tests that are expected to fail against it. The final implementation converts incidental parsing failures into predictable `ValueError` exceptions. The interactive application catches these validation errors and displays a useful message rather than terminating unexpectedly.

## 6. Execution and evidence

Run the following commands from this folder after installing dependencies:

```powershell
python processor.py
python -m pytest test_processor.py -v
```

Required screenshots:
1. Original starter program execution.
2. Failing tests against the original buggy implementation.
3. Hardened program execution.
4. Passing Hypothesis and regression tests against the hardened implementation.

**Evidence status:** The source files and test suite are prepared. Screenshots must be captured from actual terminal execution on the student's machine; no screenshots are claimed as generated here. Record the actual pytest pass/fail summary below after running it.

### Test execution record

- Python version: ____________________
- Hypothesis version: ____________________
- Pytest version: ____________________
- Initial failing test count: ____________________
- Final passing test count: ____________________
- Date run: ____________________

## 7. Conclusion

Property-based fuzzing expands test coverage beyond manually selected examples and helps expose parser assumptions around malformed values, boundary conditions, and special numeric values. The final processors validate inputs explicitly and give predictable feedback for invalid records.
