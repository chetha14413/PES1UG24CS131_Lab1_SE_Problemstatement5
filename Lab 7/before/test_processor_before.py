"""Expected-to-fail Hypothesis fuzz tests for the original buggy starter."""
import pytest
from hypothesis import given, settings, strategies as st

from processor_buggy import (
    validate_blood_type,
    calculate_pulse_pressure,
    parse_donor_registry,
)


@settings(max_examples=100, deadline=None)
@given(st.one_of(st.text(), st.none()))
def test_original_blood_type_does_not_crash(value):
    try:
        validate_blood_type(value)
    except Exception as exc:
        pytest.fail(f"Original validate_blood_type crashed for {value!r}: {type(exc).__name__}: {exc}")


@settings(max_examples=100, deadline=None)
@given(st.one_of(st.text(), st.none()))
def test_original_blood_pressure_does_not_crash(value):
    try:
        calculate_pulse_pressure(value)
    except Exception as exc:
        pytest.fail(f"Original calculate_pulse_pressure crashed for {value!r}: {type(exc).__name__}: {exc}")


@settings(max_examples=100, deadline=None)
@given(st.one_of(st.text(), st.none()))
def test_original_donor_registry_does_not_crash(value):
    try:
        parse_donor_registry(value)
    except Exception as exc:
        pytest.fail(f"Original parse_donor_registry crashed for {value!r}: {type(exc).__name__}: {exc}")
