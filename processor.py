"""Hardened input processors for the blood donation screening lab.

The functions reject malformed data with ValueError and never leak incidental
IndexError, TypeError, KeyError, or ZeroDivisionError exceptions.
"""

import math
import re


_VALID_BLOOD_TYPES = {"A", "B", "AB", "O"}
_BLOOD_CODE_RE = re.compile(r"^(A|B|AB|O)([+-])$", re.IGNORECASE)


def validate_blood_type(blood_code):
    """Return a readable ABO/Rh label for a valid code (for example, 'O+')."""
    if not isinstance(blood_code, str):
        raise ValueError("Blood type must be a string.")

    cleaned = blood_code.strip().upper()
    match = _BLOOD_CODE_RE.fullmatch(cleaned)
    if not match:
        raise ValueError("Blood type must be one of A+, A-, B+, B-, AB+, AB-, O+, or O-.")

    antigen, rh_char = match.groups()
    rh_label = "Positive" if rh_char == "+" else "Negative"
    return f"{antigen} {rh_label}"


def calculate_pulse_pressure(bp_string):
    """Calculate pulse pressure and systolic/diastolic ratio.

    The input must contain exactly two positive integer values separated by
    one slash. Systolic pressure must be greater than diastolic pressure.
    """
    if not isinstance(bp_string, str):
        raise ValueError("Blood pressure must be supplied as text.")

    cleaned = bp_string.strip()
    parts = cleaned.split("/")
    if len(parts) != 2:
        raise ValueError("Blood pressure must use the format systolic/diastolic.")

    sys_str, dia_str = (part.strip() for part in parts)
    if not sys_str.isdecimal() or not dia_str.isdecimal():
        raise ValueError("Systolic and diastolic values must be positive whole numbers.")

    systolic = int(sys_str)
    diastolic = int(dia_str)
    if systolic <= 0 or diastolic <= 0:
        raise ValueError("Blood pressure values must be greater than zero.")
    if systolic <= diastolic:
        raise ValueError("Systolic pressure must be greater than diastolic pressure.")

    pulse_diff = systolic - diastolic
    ratio = round(systolic / diastolic, 2)
    return f"Diff: {pulse_diff}, Ratio: {ratio}"


def parse_donor_registry(donor_entry):
    """Parse 'DonorID|WeightKg|Hemoglobin' and classify the record.

    Weight and hemoglobin must be finite positive numeric values. Donor IDs
    must be non-empty and cannot contain the field delimiter.
    """
    if not isinstance(donor_entry, str):
        raise ValueError("Donor record must be supplied as text.")

    fields = donor_entry.split("|")
    if len(fields) != 3:
        raise ValueError("Donor record must contain exactly three pipe-delimited fields.")

    donor_id = fields[0].strip()
    if not donor_id:
        raise ValueError("Donor ID cannot be empty.")
    if any(ord(char) < 32 for char in donor_id):
        raise ValueError("Donor ID cannot contain control characters.")

    try:
        weight = float(fields[1].strip())
        hemoglobin = float(fields[2].strip())
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("Weight and hemoglobin must be numeric values.") from exc

    if not math.isfinite(weight) or not math.isfinite(hemoglobin):
        raise ValueError("Weight and hemoglobin must be finite numbers.")
    if weight <= 0 or hemoglobin <= 0:
        raise ValueError("Weight and hemoglobin must be greater than zero.")

    eligible = weight >= 50.0 and hemoglobin >= 12.5
    return f"Donor {donor_id}: {'Eligible' if eligible else 'Deferred'}"


def main():
    """Run an interactive demonstration of the three input processors."""
    print("==== Running validate_blood_type ====")
    b_input = input("Enter blood type (e.g. A+, O-, AB+): ")
    try:
        print("Validated:", validate_blood_type(b_input))
    except ValueError as exc:
        print("Invalid blood type:", exc)

    print("\n==== Running calculate_pulse_pressure ====")
    bp_input = input("Enter BP (e.g. 120/80): ")
    try:
        print("BP Metrics:", calculate_pulse_pressure(bp_input))
    except ValueError as exc:
        print("Invalid blood pressure:", exc)

    print("\n==== Running parse_donor_registry ====")
    d_input = input("Enter record (ID|Weight|Hemoglobin): ")
    try:
        print("Status:", parse_donor_registry(d_input))
    except ValueError as exc:
        print("Invalid donor record:", exc)


if __name__ == "__main__":
    main()
