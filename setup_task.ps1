# PowerShell script to create scheduled task
$taskName = "FarmIQ - Model Training"
$taskDescription = "Runs FarmIQ's ML model training daily"
$workingDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$batchFile = Join-Path $workingDir "run_training.bat"

# Validate environment setup
$envFile = Join-Path $workingDir ".env"
if (-not (Test-Path $envFile)) {
    Write-Error "Missing .env file. Please create it with SUPABASE_URL and SUPABASE_KEY"
    exit 1
}

# Validate Python environment
$venvPath = Join-Path $workingDir ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Error "Python virtual environment not found. Please set up the environment first"
    exit 1
}

# Create task action
$action = New-ScheduledTaskAction `
    -Execute $batchFile `
    -WorkingDirectory $workingDir

# Create daily trigger (2 AM)
$trigger = New-ScheduledTaskTrigger `
    -Daily `
    -At 2am

# Create additional trigger (2 PM)
$trigger2 = New-ScheduledTaskTrigger `
    -Daily `
    -At 2pm

# Set task settings
$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5) `
    -RunOnlyIfNetworkAvailable `
    -WakeToRun

# Set principal (run with highest privileges)
$principal = New-ScheduledTaskPrincipal `
    -UserId "SYSTEM" `
    -LogonType ServiceAccount `
    -RunLevel Highest

# Register the task
Register-ScheduledTask `
    -TaskName $taskName `
    -Description $taskDescription `
    -Action $action `
    -Trigger $trigger, $trigger2 `
    -Settings $settings `
    -Principal $principal `
    -Force