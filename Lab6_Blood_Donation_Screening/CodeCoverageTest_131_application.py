import pytest

from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge


def cohort(donors=(), **overrides):
    item = {"clinic_registered": True, "type": "standard", "fast_track": False, "donors": list(donors)}
    item.update(overrides)
    return item


def donor(age=25, weight=65, hb=14.0):
    return {"age": age, "weight_kg": weight, "hb": hb}


def test_invalid_cohort_argument():
    with pytest.raises(ValueError, match="Invalid cohort"):
        process_donor_cohort("not a list", 450)


def test_invalid_volume():
    with pytest.raises(ValueError):
        process_donor_cohort([], 0)


def test_unregistered_cohort_is_skipped():
    assert process_donor_cohort([cohort([donor()], clinic_registered=False)], 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_missing_donor_values_use_defaults_and_defer():
    assert process_donor_cohort([cohort([{}])], 450)["status"] == "ZERO_YIELD"


@pytest.mark.parametrize("candidate", [donor(age=16), donor(weight=49)])
def test_age_and_weight_below_minimum_defer(candidate):
    assert process_donor_cohort([cohort([candidate])], 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_age_weight_and_hemoglobin_boundaries_are_accepted():
    result = process_donor_cohort([cohort([donor(age=17, weight=50, hb=12.5), donor(hb=18.0)])], 450)
    assert result == {"collected_ml": 900, "status": "ACCEPTED"}


def test_low_hemoglobin_deferral_for_standard_cohort():
    result = process_donor_cohort([cohort([donor(hb=12.49)])], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_altitude_low_hemoglobin_resets_yield_and_stops_cohort():
    result = process_donor_cohort([cohort([donor(), donor(hb=12.4), donor()], type="high_altitude")], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_hemoglobin_deferral():
    result = process_donor_cohort([cohort([donor(hb=18.01)])], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_fast_track_adds_volume_even_when_donor_list_empty():
    assert process_donor_cohort([cohort(fast_track=True)], 450) == {"collected_ml": 50, "status": "ACCEPTED"}


def test_more_than_four_deferrals_returns_high_deferral():
    result = process_donor_cohort([cohort([donor(age=16)] * 5)], 450)
    assert result == {"collected_ml": 0, "status": "HIGH_DEFERRAL"}


def test_registered_empty_input_returns_zero_yield():
    assert process_donor_cohort([], 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_centrifuge_no_data_values():
    assert verify_storage_centrifuge(None) == "NO_DATA"
    assert verify_storage_centrifuge([]) == "NO_DATA"


def test_centrifuge_stable_and_streak_reset():
    assert verify_storage_centrifuge([[3000, 2999, 3000, 2500, 3000]]) == "STABLE"


def test_centrifuge_aborts_on_second_consecutive_drop():
    assert verify_storage_centrifuge([[3000, 2999, 2500]]) == "ABORT_SPIN"


def test_centrifuge_streak_resets_between_runs():
    assert verify_storage_centrifuge([[2500], [2500, 3000]]) == "STABLE"
