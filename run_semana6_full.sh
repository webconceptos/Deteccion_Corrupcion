# ==========================================================
# Script maestro PowerShell: run_semana6_full.ps1
# Proyecto: Detección de Riesgos de Corrupción en Obras Públicas
# Autor: Fernando García - Hilario Aradiel
# Objetivo: Ejecutar TODO el pipeline de la Semana 6
# ==========================================================

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " 🧠 Semana 6 – Pipeline completo de modelado predictivo" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan
Start-Sleep -Seconds 1

# === 1. Construcción de datasets ===
Write-Host "`n📦 [1/9] Construyendo datasets..." -ForegroundColor Green
python scripts/build_dataset_ml.py
python scripts/build_dataset_integrado.py
Start-Sleep -Seconds 1

# === 2. Entrenamiento de modelos ===
Write-Host "`n🤖 [2/9] Entrenando modelos..." -ForegroundColor Green
python scripts/train_models.py --folds 5
Start-Sleep -Seconds 1

# === 3. Análisis postentrenamiento ===
Write-Host "`n📈 [3/9] Analizando resultados y métricas..." -ForegroundColor Green
python scripts/plot_importance.py
python scripts/plot_calibration.py
python scripts/plot_learning_curves.py
Start-Sleep -Seconds 1

# === 4. Visualizaciones avanzadas ===
Write-Host "`n📊 [4/9] Creando visualizaciones adicionales..." -ForegroundColor Green
python scripts/plot_threshold_curve.py
python scripts/plot_correlation_target.py
python scripts/plot_validation_curve.py
python scripts/plot_radar_model.py
Start-Sleep -Seconds 1

# === 5. Interpretabilidad SHAP ===
Write-Host "`n🔍 [5/9] Interpretabilidad con SHAP..." -ForegroundColor Green
python scripts/plot_shap_summary.py
Start-Sleep -Seconds 1

# === 6. Evaluación de robustez y sesgo ===
Write-Host "`n🧩 [6/9] Evaluando robustez y sesgo..." -ForegroundColor Green
python scripts/robustness_analysis.py
python scripts/analyze_bias.py
Start-Sleep -Seconds 1

# === 7. Generación de reporte PDF ===
Write-Host "`n📄 [7/9] Generando reporte ejecutivo..." -ForegroundColor Green
python scripts/generar_reporte_semana6.py
Start-Sleep -Seconds 1

# === 8. Resumen final ===
Write-Host "`n✅ [8/9] Verificación de resultados:" -ForegroundColor Yellow
Write-Host "📁 Dataset:        data/processed/dataset_integrado.parquet"
Write-Host "📊 Figuras:        reports/figures/"
Write-Host "📘 Reporte PDF:    reports/Semana6_Reporte_Ejecutivo.pdf"
Start-Sleep -Seconds 1

# === 9. Subida opcional a GitHub ===
$resp = Read-Host "¿Deseas subir los resultados a GitHub? (s/n)"
if ($resp -eq "s" -or $resp -eq "S") {
    Write-Host "`n🚀 Subiendo cambios a GitHub..." -ForegroundColor Cyan
    git add .
    git commit -m "Semana 6 ✅ Pipeline completo ejecutado con análisis extendido"
    git push origin feat/semana6-modelado
} else {
    Write-Host "ℹ️  Cambios no subidos. Puedes ejecutar 'git push' manualmente más tarde." -ForegroundColor Gray
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "🏁 Proceso Semana 6 finalizado exitosamente." -ForegroundColor Green
Write-Host "Autor: Fernando García - Hilario Aradiel" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan
