# Lab 5: Static Code Analysis deliverables

- `delivery_system.py`: corrected implementation.
- `issues.md`: issue log with severity and fixes.
- `before/delivery_system.py`: original starter preserved for before-analysis evidence.
- `reports/before/`: analysis output for the original source.
- `reports/after/`: analysis output for the corrected source.
- `reflection.md`: intentionally left unanswered.

Run from this directory in Windows PowerShell after installing the tools:

```powershell
py -m pip install pylint bandit flake8
py -m pylint before/delivery_system.py > reports/before/pylint_report.txt
py -m bandit before/delivery_system.py > reports/before/bandit_report.txt
py -m flake8 before/delivery_system.py > reports/before/flake8_report.txt
py -m pylint delivery_system.py > reports/after/pylint_report.txt
py -m bandit delivery_system.py > reports/after/bandit_report.txt
py -m flake8 delivery_system.py > reports/after/flake8_report.txt
```

Use `py` when the Python launcher is the working command in PowerShell.
