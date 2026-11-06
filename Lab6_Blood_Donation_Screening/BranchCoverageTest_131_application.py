import pytest

from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge


def donor(age=25, weight=65, hb=14.0):
    return {"age": age, "weight_kg": weight, "hb": hb}


def cohort(donors, **kwargs):
    entry = {"clinic_registered": True, "donors": donors}
    entry.update(kwargs)
    return entry


@pytest.mark.parametrize("cohorts,volume", [(None, 450), ([], -1)])
def test_guard_rejects_each_invalid_input_dimension(cohorts, volume):
    with pytest.raises(ValueError):
        process_donor_cohort(cohorts, volume)


def test_registration_true_and_false_edges():
    result = process_donor_cohort([
        cohort([donor()], clinic_registered=False),
        cohort([donor()], clinic_registered=True),
    ], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


@pytest.mark.parametrize("d", [donor(age=16), donor(age=17, weight=49), donor(age=17, weight=50)])
def test_age_and_weight_decision_edges(d):
    result = process_donor_cohort([cohort([d])], 450)
    if d["age"] < 17 or d["weight_kg"] < 50:
        assert result["collected_ml"] == 0
    else:
        assert result["collected_ml"] == 450


def test_hemoglobin_lower_equal_and_upper_edges():
    donors = [donor(hb=12.49), donor(hb=12.5), donor(hb=18.0), donor(hb=18.01)]
    assert process_donor_cohort([cohort(donors)], 450) == {"collected_ml": 900, "status": "ACCEPTED"}


def test_high_altitude_true_resets_then_fast_track_readds_and_continues():
    result = process_donor_cohort([
        cohort([donor(), donor(hb=12.0), donor()], type="high_altitude", fast_track=True),
        cohort([donor()]),
    ], 450)
    assert result == {"collected_ml": 500, "status": "ACCEPTED"}


def test_high_altitude_false_and_standard_low_hb_continues():
    result = process_donor_cohort([cohort([donor(hb=12.0), donor()], type="standard")], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_fast_track_true_false_and_deferral_result_edges():
    assert process_donor_cohort([cohort([], fast_track=True)], 450)["status"] == "ACCEPTED"
    assert process_donor_cohort([cohort([])], 450)["status"] == "ZERO_YIELD"
    assert process_donor_cohort([cohort([donor(age=16)] * 5)], 450)["status"] == "HIGH_DEFERRAL"


def test_centrifuge_empty_and_nonempty_edges():
    assert verify_storage_centrifuge([]) == "NO_DATA"
    assert verify_storage_centrifuge([[3000]]) == "STABLE"


def test_centrifuge_below_threshold_streak_abort_and_reset_edges():
    assert verify_storage_centrifuge([[2999, 2999]]) == "ABORT_SPIN"
    assert verify_storage_centrifuge([[2999, 3000, 2999]]) == "STABLE"
    assert verify_storage_centrifuge([[2999], [2999]]) == "STABLE"
