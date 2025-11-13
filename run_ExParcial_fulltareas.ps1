# ==========================================================
# ExParcial Multi-Thread Pipeline (CLEAN FINAL VERSION)
# ==========================================================

$ErrorActionPreference = "Stop"

# -----------------------------
# Logs
# -----------------------------
$LOG_DIR = "reports/logs"
if (!(Test-Path $LOG_DIR)) { New-Item -ItemType Directory -Path $LOG_DIR | Out-Null }

$STAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$MASTER_LOG = "$LOG_DIR/run_ExParcial_$STAMP.log"

function LogMaster {
    param([string]$Text)
    $line = "[" + (Get-Date) + "] " + $Text
    Add-Content -Path $MASTER_LOG -Value $line
}

# -----------------------------
# Output
# -----------------------------
function Sec {
    param([string]$t)
    Write-Host ""
    Write-Host "=========================================================="
    Write-Host $t
    Write-Host "=========================================================="
}

function Info { param([string]$t) Write-Host ("[INFO] " + $t) }
function Warn { param([string]$t) Write-Host ("[WARN] " + $t) }
function ErrMsg { param([string]$t) Write-Host ("[ERR ] " + $t) }

# -----------------------------
# Inicio
# -----------------------------
Sec "ExParcial Multi-Thread Pipeline"
LogMaster "Inicio pipeline"

# -----------------------------
# Verificacion papermill
# -----------------------------
& papermill --version *> $null
if ($LASTEXITCODE -ne 0) {
    ErrMsg "papermill no esta instalado"
    exit 1
}
Info "papermill OK"
LogMaster "papermill OK"

# -----------------------------
# Lista de notebooks
# -----------------------------
$Tasks = @(
    @{ Name="ExParcial_IngAtributos";         In="notebooks/ExParcial_IngAtributos.ipynb";         Out="notebooks/out_ExParcial_IngAtributos.ipynb" },
    @{ Name="ExParcial_Experimentos";         In="notebooks/ExParcial_Experimentos.ipynb";         Out="notebooks/out_ExParcial_Experimentos.ipynb" },
    @{ Name="ExParcial_ValidacionResultados"; In="notebooks/ExParcial_ValidacionResultados.ipynb"; Out="notebooks/out_ExParcial_ValidacionResultados.ipynb" },
    @{ Name="ExParcial_AblationStudy";        In="notebooks/ExParcial_AblationStudy.ipynb";        Out="notebooks/out_ExParcial_AblationStudy.ipynb" },
    @{ Name="ExParcial_XAI";                  In="notebooks/ExParcial_XAI.ipynb";                  Out="notebooks/out_ExParcial_XAI.ipynb" },
    @{ Name="ExParcial_EDA_Profesional";      In="notebooks/ExParcial_EDA_Profesional.ipynb";      Out="notebooks/out_ExParcial_EDA_Profesional.ipynb" }
)

$Jobs = @()

# -----------------------------
# Lanzar hilos
# -----------------------------
foreach ($task in $Tasks) {

    $name = $task.Name
    $input = $task.In
    $output = $task.Out

    Sec ("Lanzando hilo: " + $name)
    LogMaster ("Lanzando hilo para " + $name)

    $job = Start-Job -ScriptBlock {
        param($name, $input, $output, $MASTER_LOG)

        $logFile = "reports/logs/log_" + $name + ".log"
        $cmd = "papermill """ + $input + """ """ + $output + """ >> """ + $logFile + """ 2>&1"

        Start-Process -FilePath "cmd.exe" -ArgumentList "/c " + $cmd -NoNewWindow -Wait

        if ($LASTEXITCODE -ne 0) {
            Add-Content -Path $MASTER_LOG -Value ("[ERROR] " + $name)
            exit 1
        } else {
            Add-Content -Path $MASTER_LOG -Value ("[OK] " + $name)
            exit 0
        }

    } -ArgumentList $name, $input, $output, $MASTER_LOG

    $Jobs += $job
}

# -----------------------------
# Esperar hilos
# -----------------------------
Sec "Esperando finalizacion de hilos..."

Wait-Job -Job $Jobs | Out-Null

$Failures = @()

foreach ($job in $Jobs) {
    if ($job.State -ne "Completed") {
        $Failures += $job.Command
    }
}

# -----------------------------
# Resumen Final
# -----------------------------
Sec "Resumen Final"

if ($Failures.Count -eq 0) {
    Info "Todos los notebooks completados"
    LogMaster "Pipeline OK"
} else {
    ErrMsg "Tareas con error:"
    foreach ($f in $Failures) {
        ErrMsg (" - " + $f)
    }
    LogMaster "Pipeline finalizado con errores"
}

Info ("Log maestro: " + $MASTER_LOG)
Info "Pipeline finalizado"
