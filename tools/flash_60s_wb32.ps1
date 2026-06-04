param(
    [string]$FirmwarePath,
    [string]$Wb32Path,
    [switch]$SkipReadback
)

$ErrorActionPreference = 'Stop'

$expectedHash = 'FC7C6CEFE8284075EC427689CD2B213C844B538A5FCB96DFFCA30E0442B61D07'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoDir = Split-Path -Parent $scriptDir

if (-not $FirmwarePath) {
    $FirmwarePath = Join-Path $repoDir 'firmware\oe926_via_v14_backlight_timeout_60s.bin'
}

if (-not (Test-Path -LiteralPath $FirmwarePath)) {
    throw "Firmware file not found: $FirmwarePath"
}

$actualHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $FirmwarePath).Hash
if ($actualHash -ne $expectedHash) {
    throw "Firmware SHA256 mismatch. Got $actualHash, expected $expectedHash"
}

function Find-Wb32Tool {
    param([string]$ExplicitPath)

    $candidates = @()
    if ($ExplicitPath) { $candidates += $ExplicitPath }
    $candidates += 'C:\msys64\mingw64\bin\wb32-dfu-updater_cli.exe'
    $candidates += 'C:\QMK_MSYS\mingw64\bin\wb32-dfu-updater_cli.exe'

    $cmd = Get-Command wb32-dfu-updater_cli.exe -ErrorAction SilentlyContinue
    if ($cmd) { $candidates += $cmd.Source }

    foreach ($candidate in $candidates) {
        if ($candidate -and (Test-Path -LiteralPath $candidate)) {
            return $candidate
        }
    }

    throw @"
wb32-dfu-updater_cli.exe was not found.

Install QMK MSYS:
  https://msys.qmk.fm/

Or pass the path manually:
  powershell -ExecutionPolicy Bypass -File .\tools\flash_60s_wb32.ps1 -Wb32Path "C:\path\to\wb32-dfu-updater_cli.exe"
"@
}

$wb32 = Find-Wb32Tool -ExplicitPath $Wb32Path
$verify = Join-Path $repoDir 'dist\verify_readback_0x08000000_61828.bin'

Write-Host "Using firmware: $FirmwarePath"
Write-Host "Firmware SHA256 verified: $actualHash"
Write-Host "Using WB32 tool: $wb32"
Write-Host ""

Write-Host "Checking DFU device..."
& $wb32 -l

Write-Host ""
Write-Host "Flashing 60-second firmware..."
& $wb32 -s 0x08000000 -D $FirmwarePath
if ($LASTEXITCODE -ne 0) {
    throw "Flash failed with exit code $LASTEXITCODE"
}

if (-not $SkipReadback) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $verify) | Out-Null
    if (Test-Path -LiteralPath $verify) {
        Remove-Item -LiteralPath $verify -Force
    }

    Write-Host ""
    Write-Host "Reading firmware back for verification..."
    & $wb32 -s 0x08000000 -Z 61828 -U $verify
    if ($LASTEXITCODE -ne 0) {
        throw "Readback failed with exit code $LASTEXITCODE"
    }

    $verifyHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $verify).Hash
    if ($verifyHash -ne $expectedHash) {
        throw "Readback SHA256 mismatch. Got $verifyHash, expected $expectedHash"
    }

    Write-Host "Readback verified: $verifyHash"
}

Write-Host ""
Write-Host "Resetting keyboard out of DFU..."
& $wb32 -R
if ($LASTEXITCODE -ne 0) {
    throw "Reset failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Done. Keyboard should return as VID_388D PID_0003."
