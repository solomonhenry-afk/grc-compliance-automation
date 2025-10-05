#!/usr/bin/env python3
"""
compliance_scoring.py
Generates compliance reports (HTML + CSV) from control scan data.
Adds visual charts and trend tracking.
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
import os

# Paths
root = Path(__file__).resolve().parents[1]
data_dir = root / "data"
report_dir = root / "reports"
trend_csv = report_dir / "compliance_trend.csv"
html_report = report_dir / "compliance_report.html"

# Ensure directories exist
report_dir.mkdir(parents=True, exist_ok=True)
data_dir.mkdir(parents=True, exist_ok=True)

# Simulated compliance data (replace with AD scan results)
data = {
    "Control": [
        "SOX-1 Access Control",
        "SOX-2 Audit Logging",
        "PCI-1 Firewall Rules",
        "PCI-2 Encryption Policy",
        "ISO-1 Asset Inventory",
        "ISO-2 Patch Management"
    ],
    "Compliant": [95, 90, 100, 85, 80, 88],
    "Owner": [
        "IT Security",
        "Audit",
        "Network",
        "Infrastructure",
        "GRC",
        "SysAdmin"
    ],
}
df = pd.DataFrame(data)

# Compute summary metrics
overall = df["Compliant"].mean()
now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

# Append to trend CSV
trend_df = pd.DataFrame([[now, overall]], columns=["Timestamp", "OverallCompliance"])
if trend_csv.exists():
    existing = pd.read_csv(trend_csv)
    trend_df = pd.concat([existing, trend_df], ignore_index=True)
trend_df.to_csv(trend_csv, index=False)

# Plot bar chart
plt.figure(figsize=(8, 5))
plt.barh(df["Control"], df["Compliant"], color="#4CAF50")
plt.title(f"Compliance Scores by Control ({now})")
plt.xlabel("Compliance %")
plt.xlim(0, 100)
bar_chart_path = report_dir / "bar_chart.png"
plt.tight_layout()
plt.savefig(bar_chart_path)
plt.close()

# Plot trend chart
plt.figure(figsize=(8, 4))
plt.plot(trend_df["Timestamp"], trend_df["OverallCompliance"], marker="o", color="#2196F3")
plt.xticks(rotation=45, ha="right")
plt.title("Compliance Trend Over Time")
plt.ylabel("Overall Compliance %")
trend_chart_path = report_dir / "trend_chart.png"
plt.tight_layout()
plt.savefig(trend_chart_path)
plt.close()

# Generate HTML Report
html = f"""
<html>
<head>
<meta charset="utf-8">
<title>Regulatory Compliance Dashboard</title>
<style>
body {{
  font-family: Arial, sans-serif;
  margin: 40px;
  background: #f5f7fa;
  color: #333;
}}
h1, h2 {{ color: #004080; }}
table {{
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 30px;
}}
th, td {{
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}}
th {{
  background: #004080;
  color: #fff;
}}
.metric {{
  background: #e8f4fc;
  padding: 10px;
  border-radius: 6px;
  font-weight: bold;
}}
</style>
</head>
<body>
<h1>Regulatory Compliance Dashboard</h1>
<p><b>Generated:</b> {now}</p>
<div class="metric">Overall Compliance: {overall:.1f}%</div>
<h2>Control Scores</h2>
{df.to_html(index=False, border=0)}
<h2>Visual Summary</h2>
<img src="bar_chart.png" width="600">
<h2>Compliance Trend Over Time</h2>
<img src="trend_chart.png" width="600">
</body>
</html>
"""

html_report.write_text(html, encoding="utf-8")
print(f"✅ Report generated: {html_report}")
print(f"✅ Trend updated: {trend_csv}")
