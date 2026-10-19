param(
    [string]$PiHost = "",
    [string]$RemotePath = "/home/pi/pixoo-weather",
    [switch]$Restart
)

$ErrorActionPreference = "Stop"

function Invoke-Step {
    param(
        [string]$Name,
        [scriptblock]$Action
    )

    Write-Host "==> $Name"
    & $Action
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

    throw "Could not resolve/connect to the Pi. Try: .\scripts\deploy-to-pi.ps1 -PiHost <user>@<PI_IP_ADDRESS>"
}

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Invoke-Step "Checking required commands" {
    foreach ($command in @("scp", "ssh")) {
        if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
            throw "Required command not found: $command"
        }
    }
}

$PiHost = Resolve-PiHost
Write-Host "Using Pi host: $PiHost"

$runtimeFiles = @(
    'app.py',
    'colors.py',
    'functions.py',
    'renderer.py',
    'weatherresponse.py',
    'requirements.txt',
    '3x5pixel.ttf',
    'icon_sets/__init__.py',
    'icon_sets/legacy_functions.py',
    'icon_sets/legacy_pixel.py',
    'icon_sets/premium_pixel.py',
    'scripts/deploy-to-pi.ps1',
    'scripts/install-systemd-services.sh',
    'scripts/setup-ssh-key.ps1',
    'scripts/start-on-pi.ps1',
    'scripts/start-pixoo-weather.sh',
    'systemd/pixoo-rest.service',
    'systemd/pixoo-weather.service'
)

Invoke-Step "Copying application files" {
    ssh $PiHost "mkdir -p '$RemotePath' '$RemotePath/icon_sets' '$RemotePath/scripts' '$RemotePath/systemd'"
    if ($LASTEXITCODE -ne 0) { throw "Could not prepare application folders" }
    foreach ($file in $runtimeFiles) {
        scp (Join-Path $projectRoot $file) "${PiHost}:${RemotePath}/$file"
        if ($LASTEXITCODE -ne 0) { throw "Transfer failed: $file" }
    }
}

if ($Restart) {
    Invoke-Step "Restarting pixoo-weather on Raspberry Pi" {
        $remoteCommand = @"
cd '$RemotePath'
pkill -f 'python.*app.py' || true
if [ -x .venv/bin/python ]; then
    nohup .venv/bin/python app.py > pixoo-weather.log 2>&1 < /dev/null &
else
    nohup python3 app.py > pixoo-weather.log 2>&1 < /dev/null &
fi
"@

        ssh $PiHost $remoteCommand
    }

    Write-Host "pixoo-weather restart requested. Check logs with:"
    Write-Host "ssh $PiHost `"tail -f ${RemotePath}/pixoo-weather.log`""
} else {
    Write-Host "Deploy complete. To restart manually on the Pi:"
    Write-Host "cd $RemotePath"
    Write-Host "source .venv/bin/activate"
    Write-Host "python app.py"
}
