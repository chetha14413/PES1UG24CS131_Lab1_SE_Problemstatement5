# Before-fix baseline

These files preserve the original buggy Lab 7 starter code from the assigned blood-donation-screening repository.

From the Lab 7 folder, run:

```powershell
python before/processor_buggy.py
python -m pytest before/test_processor_before.py -v
```

The baseline fuzz tests are expected to fail because the original functions assume well-formed strings and fields. This is intentional evidence of defects, not a failing final test suite.
