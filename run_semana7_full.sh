#!/bin/bash
# ==========================================================
# Semana 7 – Optimización y Experimentos Comparables
# ==========================================================
timestamp=$(date +"%Y%m%d_%H%M%S")
log_dir="reports/logs"
mkdir -p "$log_dir"
log_file="$log_dir/semana7_run_${timestamp}.log"

echo "==========================================================" | tee -a "$log_file"
echo " 🚀 Semana 7 – Experimentos de optimización de hiperparámetros" | tee -a "$log_file"
echo " Log: $log_file" | tee -a "$log_file"
echo "==========================================================" | tee -a "$log_file"

run_cmd() {
    echo -e "\n[$(date '+%H:%M:%S')] ▶️  $1" | tee -a "$log_file"
    eval "$2" >> "$log_file" 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ $1 completado" | tee -a "$log_file"
    else
        echo "❌ Error en $1" | tee -a "$log_file"
    fi
}

run_cmd "Random Search" "python scripts/opt_random_search.py"
run_cmd "Bayesian Optimization" "python scripts/opt_bayes_opt.py"
run_cmd "Resumen de resultados" "python scripts/opt_summary.py"
run_cmd "Gráfico de evolución" "python scripts/opt_plot_evolution.py"

echo "==========================================================" | tee -a "$log_file"
echo "🏁 Semana 7 finalizada. Revisa reports/tuning/ para resultados." | tee -a "$log_file"
echo "==========================================================" | tee -a "$log_file"
