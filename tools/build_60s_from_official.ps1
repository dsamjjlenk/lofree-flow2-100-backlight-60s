param(
    [string]$OfficialFirmwarePath
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoDir = Split-Path -Parent $scriptDir
$builder = Join-Path $scriptDir 'flow2_60s_builder.py'
$outDir = Join-Path $repoDir 'dist'

if (-not $OfficialFirmwarePath) {
    Add-Type -AssemblyName System.Windows.Forms
    $dialog = New-Object System.Windows.Forms.OpenFileDialog
    $dialog.Title = 'Select official Lofree Flow2 100 / OE926 v14 firmware'
    $dialog.Filter = 'Firmware files (*.hex;*.bin)|*.hex;*.bin|All files (*.*)|*.*'
    $dialog.Multiselect = $false
    $result = $dialog.ShowDialog()
    if ($result -ne [System.Windows.Forms.DialogResult]::OK) {
        throw 'No firmware file selected.'
    }
    $OfficialFirmwarePath = $dialog.FileName
}

New-Item -ItemType Directory -Force -Path $outDir | Out-Null

py -3 $builder $OfficialFirmwarePath --out-dir $outDir
if ($LASTEXITCODE -ne 0) {
    throw "Builder failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Done. Built files are in:"
Write-Host "  $outDir"
