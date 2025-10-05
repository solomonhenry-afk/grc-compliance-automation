# collect_system_evidence.ps1
# Run on a domain-joined Windows host with appropriate privileges.
# Outputs CSV to ../data/collected_evidence.csv (path relative to repo root when run inside repo root)

Param(
    [string]$OutFile = ".\\data\\collected_evidence.csv"
)

# Ensure output folder exists
$dir = Split-Path $OutFile
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }

# Example checks - replace or extend with real checks in your lab
$results = @()

# Password policy
try {
    $pwPolicy = Get-ADDefaultDomainPasswordPolicy -ErrorAction Stop
    $minLen = $pwPolicy.MinPasswordLength
} catch {
    $minLen = "N/A"
}
$results += [pscustomobject]@{
    'Control ID' = 'AC-002'
    'ActualValue' = "MinLength:$minLen"
    'Status' = if (($minLen -ne "N/A") -and ($minLen -ge 12)) {'Compliant'} else {'Non-Compliant'}
}

# MFA for privileged accounts (placeholder - needs your AAD/Identity checks)
$results += [pscustomobject]@{
    'Control ID' = 'AC-001'
    'ActualValue' = 'Enabled' # change to real query for your environment
    'Status' = 'Compliant'
}

# Log retention (placeholder)
$results += [pscustomobject]@{
    'Control ID' = 'LG-001'
    'ActualValue' = '120'  # days
    'Status' = if (120 -ge 90) {'Compliant'} else {'Non-Compliant'}
}

# Patch compliance (placeholder)
$results += [pscustomobject]@{
    'Control ID' = 'PT-001'
    'ActualValue' = '97' # percent
    'Status' = if (97 -ge 95) {'Compliant'} else {'Non-Compliant'}
}

# Disk encryption (placeholder)
$results += [pscustomobject]@{
    'Control ID' = 'EN-001'
    'ActualValue' = 'Enabled'
    'Status' = 'Compliant'
}

$results | Export-Csv -Path $OutFile -NoTypeInformation -Force
Write-Host "Evidence exported to $OutFile"
