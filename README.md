# Project 2 — Regulatory Compliance Automation

Objective:
Automate Active Directory & Server compliance validation and reporting against SOX, PCI-DSS, ISO 27001, and NIST CSF controls.

Components:
- data/baseline_controls.csv — baseline control definitions
- scripts/collect_system_evidence.ps1 — PowerShell evidence collector (run in AD)
- scripts/compliance_scoring.py — Python scoring + HTML report generator
- reports/compliance_report.html — generated output
- .github/workflows/compliance-ci.yml — CI pipeline (daily + manual)

How to run locally:
1. (On Windows AD host) run: PowerShell -> `.\scripts\collect_system_evidence.ps1 -OutFile .\data\collected_evidence.csv`
2. (Linux/macOS or local) run: `python3 scripts/compliance_scoring.py`
3. Open `reports/compliance_report.html`

Notes:
- Replace placeholder checks in the PowerShell with lab-specific AD/AzureAD/SCCM queries for full fidelity.
- Do not commit sensitive evidence (ad user lists, logs) to public repos. Sanitize if necessary.
