#!/usr/bin/env python3
import pandas as pd
from pathlib import Path
import os
import datetime
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

baseline_fp = DATA / "baseline_controls.csv"
evidence_fp = DATA / "collected_evidence.csv"
out_html = REPORTS / "compliance_report.html"
out_csv_summary = REPORTS / "compliance_summary.csv"

# Load baseline
baseline = pd.read_csv(baseline_fp)

# Load evidence if present
if evidence_fp.exists():
    evidence = pd.read_csv(evidence_fp)
else:
    evidence = pd.DataFrame(columns=['Control ID','ActualValue','Status'])

# Normalize columns
evidence_columns = evidence.columns.str.strip().tolist()
if 'Control ID' not in evidence_columns and 'ControlID' in evidence_columns:
    evidence = evidence.rename(columns={'ControlID':'Control ID'})

# Merge baseline <-> evidence
merged = baseline.merge(evidence, how='left', left_on='Control ID', right_on='Control ID')
merged['Status'] = merged['Status'].fillna('Not Checked')

# Compute score: weight * (1 if Compliant else 0)
merged['CompliantFlag'] = merged['Status'].apply(lambda s: 1 if str(s).strip().lower()=='compliant' else 0)
merged['Score'] = merged['CompliantFlag'] * merged['Weight']

total_weight = merged['Weight'].sum()
achieved = merged['Score'].sum()
overall_pct = round((achieved / total_weight) * 100, 2) if total_weight>0 else 0.0

# Per-framework summary
framework_summary = merged.groupby('Framework').apply(lambda df: pd.Series({
    'Controls': len(df),
    'Compliant': int(df['CompliantFlag'].sum()),
    'WeightTotal': int(df['Weight'].sum()),
    'Pct': round((df['Score'].sum()/df['Weight'].sum()*100) if df['Weight'].sum()>0 else 0,2)
})).reset_index()

# Save a CSV summary
framework_summary.to_csv(out_csv_summary, index=False)

# Build HTML report
now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
html_parts = []
html_parts.append(f"<html><head><meta charset='utf-8'><title>Compliance Report</title>")
html_parts.append("<style>body{font-family:Segoe UI,Arial;padding:18px;color:#0b1220}table{border-collapse:collapse;width:100%}th,td{padding:8px;border:1px solid #ddd;text-align:left}h1{color:#0d47a1}</style>")
html_parts.append("</head><body>")
html_parts.append(f"<h1>Regulatory Compliance Automation Report</h1>")
html_parts.append(f"<p><strong>Generated:</strong> {now}</p>")
html_parts.append(f"<h2>Overall Compliance Score: {overall_pct}%</h2>")

# Insert framework summary table
html_parts.append("<h3>By Framework</h3>")
html_parts.append(framework_summary.to_html(index=False, classes='summary-table', escape=False))

# Add plotly bar (framework compliance pct)
fig = px.bar(framework_summary, x='Framework', y='Pct', text='Pct', title='Compliance % by Framework', labels={'Pct':'Compliance %'})
fig.update_traces(texttemplate='%{text}%', textposition='outside')
fig.update_layout(margin=dict(l=20,r=20,t=40,b=20), yaxis=dict(range=[0,100]))
fig_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
html_parts.append(fig_html)

# Detailed merged table (first 200 rows)
html_parts.append("<h3>Controls Detail</h3>")
html_parts.append(merged.head(200).to_html(index=False, escape=False))

html_parts.append("</body></html>")

out_html.write_text("\n".join(html_parts), encoding="utf-8")
print(f"✅ Report generated: {out_html}")
