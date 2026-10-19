param(
    [string]$PiHost = "",
    [string]$RemotePath = "/home/pi/pixoo-weather"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) {
    throw "Required command not found: ssh"
}

function Resolve-PiHost {
    if ($PiHost) {
        return $PiHost
    }

    $candidates = @(
        "pi@pixoo64.local",
        "pi@pixoo64"
    )

    foreach ($candidate in $candidates) {
        Write-Host "Checking SSH connection to $candidate..."
        & ssh -o BatchMode=yes -o ConnectTimeout=5 $candidate "echo ok" 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            return $candidate
        }
    }

    throw "Could not resolve/connect to the Pi. Try: .\scripts\start-on-pi.ps1 -PiHost <user>@<PI_IP_ADDRESS>"
}

$PiHost = Resolve-PiHost

Write-Host "Starting pixoo-rest and pixoo-weather on $PiHost"
Write-Host "Press CTRL+C in this window to stop both remote processes."

$remoteCommand = @"
cd '$RemotePath'
chmod +x scripts/start-pixoo-weather.sh
./scripts/start-pixoo-weather.sh
"@

ssh $PiHost $remoteCommand
