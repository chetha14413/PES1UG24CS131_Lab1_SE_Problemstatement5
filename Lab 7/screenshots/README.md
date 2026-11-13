# Screenshot evidence checklist

Capture real screenshots from PowerShell or VS Code terminal and save them here:

1. `01_original_processor_run.png` — run the assigned starter `processor.py`.
2. `02_fuzz_tests_fail_before_fix.png` — run completed tests against the original buggy starter.
3. `03_fixed_processor_run.png` — run the hardened `processor.py` using sample valid entries.
4. `04_fuzz_tests_pass_after_fix.png` — run `python -m pytest test_processor.py -v` and show the summary.

Do not create screenshots by typing expected output into an editor. The evidence must show actual command execution.
