@"
Write-Host '== Verificando ubicación actual ==' -ForegroundColor Cyan
git status
Write-Host "`n== Remotos configurados ==" -ForegroundColor Cyan
git remote -v
Write-Host "`n== Actualizando desde remoto ==" -ForegroundColor Cyan
git fetch --all --prune
\$backupBranch = 'backup/local-' + (Get-Date -Format 'yyyyMMdd-HHmm')
Write-Host "`n== Creando respaldo temporal: \$backupBranch ==" -ForegroundColor Yellow
git branch \$backupBranch
Write-Host "`n== Cambiando a rama main ==" -ForegroundColor Cyan
git checkout main
Write-Host "`n== Sincronizando con origin/main ==" -ForegroundColor Cyan
git reset --hard origin/main
Write-Host "`n== Limpiando archivos no rastreados ==" -ForegroundColor Cyan
git clean -fd
Write-Host "`n== Estado final del repositorio ==" -ForegroundColor Green
git status
Write-Host "`nÚltimo commit remoto:" -ForegroundColor Green
git log -1 --oneline --decorate
Write-Host "`n== Verificando .env ==" -ForegroundColor Cyan
if (Test-Path '.env') {
  if (-not (Select-String -Path '.gitignore' -Pattern '^\s*\.env\s*$' -SimpleMatch -Quiet)) {
    Add-Content .gitignore '.env'
  }
  git rm --cached .env 2>\$null
  Write-Host 'Archivo .env excluido del versionado.' -ForegroundColor Yellow
} else {
  Write-Host 'No se encontró .env (ok).' -ForegroundColor Green
}
Write-Host "`n✅ Sincronización completa. Tu copia local ahora coincide con origin/main" -ForegroundColor Green
"@ | Out-File -FilePath ".\sync_repo.ps1" -Encoding UTF8 -Force
