# Lab 6 – Blood Donation Screening

## Project introduction and objective

This project applies code coverage and branch coverage testing to a blood donation screening application. The objective is to exercise the application’s functions and decision paths and report the measured test and coverage results.

The application code is from the Lab 6 folder of the assigned [`L6_L7_05_blood_donation_screening` repository](https://github.com/SETAPESU26/L6_L7_05_blood_donation_screening). Its application logic is preserved.

## Student details

- **Student Name:** Chetha Samrutha V
- **SRN:** PES1UG24CS131

## Application functionality

- `process_donor_cohort(cohorts, standard_volume_ml)` validates the cohort input, screens donors by clinic registration, age, weight, and hemoglobin, applies high-altitude and fast-track handling, and returns the collected volume and screening status.
- `verify_storage_centrifuge(centrifuge_runs)` checks centrifuge RPM readings and reports an abort after two consecutive readings below 3000; otherwise, it reports stable operation or no data.

## Project folder structure

```text
Lab6_Blood_Donation_Screening/
├── blood_donation_screening.py
├── CodeCoverageTest_131_application.py
├── BranchCoverageTest_131_application.py
├── README.md
├── requirements.txt
├── reports/
│   ├── code_coverage.txt
│   └── branch_coverage.txt
└── screenshots/
    ├── code_coverage.png
    └── branch_coverage.png
```

## Installation

From this project folder, create and activate a virtual environment, then install the listed dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run code coverage tests

The code coverage suite contains 17 tests for normal and exceptional inputs, defaults, boundary values, screening conditions, return statuses, and centrifuge outcomes.

```powershell
coverage run --source=blood_donation_screening -m pytest -q CodeCoverageTest_131_application.py
coverage report -m | Tee-Object reports\code_coverage.txt
```

## Run branch coverage tests

The branch coverage suite contains 12 tests focused on the true and false outcomes of the application’s conditions, including donor eligibility, hemoglobin thresholds, high-altitude behavior, fast-track handling, final statuses, and centrifuge RPM streaks.

```powershell
coverage erase
coverage run --branch --source=blood_donation_screening -m pytest -q BranchCoverageTest_131_application.py
coverage report -m | Tee-Object reports\branch_coverage.txt
```

## Verified coverage results

| Measure | Code coverage run | Branch coverage run |
|---|---:|---:|
| Tests passed | 17 | 12 |
| Statements | 45 | 45 |
| Missed statements | 0 | 0 |
| Branches | — | 32 |
| Partial branches | — | 0 |
| Coverage | 100% | 100% |

**Total tests passed:** 29.

## Coverage screenshots

- [Code coverage terminal screenshot](screenshots/code_coverage.png)
- [Branch coverage terminal screenshot](screenshots/branch_coverage.png)
