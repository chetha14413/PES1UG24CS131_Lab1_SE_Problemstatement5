"""Property-based fuzz tests for the blood donation screening processors."""

import pytest
from hypothesis import given, settings, strategies as st

from processor import (
    calculate_pulse_pressure,
    parse_donor_registry,
    validate_blood_type,
)


@settings(max_examples=300, deadline=None)
@given(st.one_of(st.text(), st.none(), st.integers(), st.floats(allow_nan=True, allow_infinity=True)))
def test_validate_blood_type_rejects_or_returns_a_valid_label(value):
    try:
        result = validate_blood_type(value)
    except ValueError:
        return
    assert isinstance(value, str)
    assert result in {
        "A Positive", "A Negative", "B Positive", "B Negative",
        "AB Positive", "AB Negative", "O Positive", "O Negative",
    }


@settings(max_examples=300, deadline=None)
@given(st.one_of(st.text(), st.none(), st.integers(), st.lists(st.text())))
def test_calculate_pulse_pressure_rejects_or_returns_consistent_metrics(value):
    try:
        result = calculate_pulse_pressure(value)
    except ValueError:
        return
    assert isinstance(value, str)
    assert result.startswith("Diff: ")
    diff_text, ratio_text = result.split(", Ratio: ")
    difference = int(diff_text[len("Diff: "):])
    ratio = float(ratio_text)
    assert difference > 0
    assert ratio > 1.0


@settings(max_examples=300, deadline=None)
@given(st.one_of(st.text(), st.none(), st.integers(), st.lists(st.text())))
def test_parse_donor_registry_rejects_or_returns_a_valid_status(value):
    try:
        result = parse_donor_registry(value)
    except ValueError:
        return
    assert isinstance(value, str)
    assert result.startswith("Donor ")
    assert result.endswith(": Eligible") or result.endswith(": Deferred")


@given(
    blood_group=st.sampled_from(["A", "B", "AB", "O"]),
    rh=st.sampled_from(["+", "-"]),
)
def test_all_supported_blood_groups_are_case_normalized(blood_group, rh):
    expected = "Positive" if rh == "+" else "Negative"
    assert validate_blood_type(f" {blood_group.lower()}{rh} ") == f"{blood_group} {expected}"


@given(
    systolic=st.integers(min_value=2, max_value=300),
    diastolic=st.integers(min_value=1, max_value=299),
)
def test_valid_blood_pressure_output_is_consistent(systolic, diastolic):
    if systolic <= diastolic:
        with pytest.raises(ValueError):
            calculate_pulse_pressure(f"{systolic}/{diastolic}")
    else:
        result = calculate_pulse_pressure(f"{systolic}/{diastolic}")
        assert f"Diff: {systolic - diastolic}" in result


@given(
    donor_id=st.text(min_size=1).filter(lambda value: bool(value.strip()) and "|" not in value and not any(ord(c) < 32 for c in value)),
    weight=st.floats(min_value=0.01, max_value=300, allow_nan=False, allow_infinity=False),
    hemoglobin=st.floats(min_value=0.01, max_value=30, allow_nan=False, allow_infinity=False),
)
def test_donor_eligibility_matches_thresholds(donor_id, weight, hemoglobin):
    result = parse_donor_registry(f"{donor_id}|{weight}|{hemoglobin}")
    expected = "Eligible" if weight >= 50 and hemoglobin >= 12.5 else "Deferred"
    assert result == f"Donor {donor_id.strip()}: {expected}"


@pytest.mark.parametrize("bad_value", [None, "", "A", "A++", "X+", "ABO+", 123, "A- " * 2])
def test_invalid_blood_types_raise_value_error(bad_value):
    with pytest.raises(ValueError):
        validate_blood_type(bad_value)


@pytest.mark.parametrize("bad_value", [None, "", "120", "120/80/70", "x/80", "120/0", "80/120", "120.5/80"])
def test_invalid_blood_pressure_raises_value_error(bad_value):
    with pytest.raises(ValueError):
        calculate_pulse_pressure(bad_value)


@pytest.mark.parametrize("bad_value", [None, "", "D1|70", "D1|70|13|extra", "|70|13", "D1|nan|13", "D1|70|inf", "D1|-1|13"])
def test_invalid_donor_registry_entries_raise_value_error(bad_value):
    with pytest.raises(ValueError):
        parse_donor_registry(bad_value)
