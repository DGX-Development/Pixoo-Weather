param(
    [string]$PiHost = "pi@pixoo64.local",
    [string]$KeyPath = "$env:USERPROFILE\.ssh\id_ed25519"
)

$ErrorActionPreference = "Stop"

foreach ($command in @("ssh", "ssh-keygen")) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $command"
    }
}

$sshDir = Split-Path -Parent $KeyPath
if (-not (Test-Path $sshDir)) {
    New-Item -ItemType Directory -Path $sshDir | Out-Null
}

if (-not (Test-Path $KeyPath)) {
    Write-Host "Creating SSH key: $KeyPath"
    $keygenCommand = 'ssh-keygen -t ed25519 -f "' + $KeyPath + '" -N "" -C "pixoo64-weather"'
    cmd.exe /c $keygenCommand
    if ($LASTEXITCODE -ne 0) {
        throw "ssh-keygen failed with exit code $LASTEXITCODE"
    }
} else {
    Write-Host "SSH key already exists: $KeyPath"
}

if (-not (Test-Path "$KeyPath.pub")) {
    throw "SSH public key was not created: $KeyPath.pub"
}

$publicKey = Get-Content "$KeyPath.pub" -Raw
$escapedPublicKey = $publicKey.Replace("'", "'\''").Trim()

Write-Host "Installing public key on $PiHost"
Write-Host "You should only be prompted for the Pi password once."

$remoteCommand = @"
mkdir -p ~/.ssh
chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys
grep -qxF '$escapedPublicKey' ~/.ssh/authorized_keys || echo '$escapedPublicKey' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
"@

ssh $PiHost $remoteCommand

Write-Host "Testing key login..."
ssh -i $KeyPath $PiHost "echo SSH key login works"

Write-Host ""
Write-Host "To use this key explicitly:"
Write-Host "ssh -i `"$KeyPath`" $PiHost"
Write-Host ""
Write-Host "The deploy/start scripts should now use this key automatically."
