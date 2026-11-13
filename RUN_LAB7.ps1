$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    py -m venv .venv
}
& .\.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }

Write-Host "`n=== BEFORE FIX: the original starter should fail fuzz tests ===" -ForegroundColor Yellow
python -m pytest before/test_processor_before.py -v
$beforeExit = $LASTEXITCODE
if ($beforeExit -eq 0) {
    Write-Warning "The baseline tests passed unexpectedly; inspect the original starter and test environment."
} else {
    Write-Host "Expected: original starter exposed one or more fuzzing failures." -ForegroundColor Green
}

Write-Host "`n=== AFTER FIX: the hardened implementation should pass ===" -ForegroundColor Cyan
python -m pytest test_processor.py -v
if ($LASTEXITCODE -ne 0) { throw "Final tests did not pass." }

Write-Host "`n=== Fixed application demonstration ===" -ForegroundColor Cyan
python processor.py
