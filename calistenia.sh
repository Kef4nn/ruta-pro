#!/bin/bash
# Calistenia en casa 52 semanas, 7-8 AM L-S. Uso: calistenia.sh   (HOY=AAAA-MM-DD DRY=1 para probar)
set -euo pipefail
DIR="$(dirname "$0")"
HOY="${HOY:-$(TZ=America/Santo_Domingo date +%F)}"
DOW=$(date -d "$HOY" +%u)
D=$(( ( $(date -d "$HOY" +%s) - $(date -d 2026-11-23 +%s) ) / 86400 ))
[ "$D" -ge 1 ] && [ "$DOW" != 7 ] || exit 0          # empieza el martes 24/11; domingo descanso
S=$(( D / 7 + 1 )); [ "$S" -le 52 ] || exit 0
# semana 1 arranca en martes: fuerza mar/jue, cardio mié/vie, sin dos días de fuerza seguidos
case $HOY in 2026-11-24) DOW=1 ;; 2026-11-25) DOW=2 ;; 2026-11-26) DOW=3 ;; 2026-11-27) DOW=4 ;; esac
IFS=$'\t' read -r _ F SER EMP TIR PIE COR CAR SAB < <(awk -F'\t' -v s="$S" '!/^#/ && s<=$1 {print; exit}' "$DIR/calistenia.tsv")
case $DOW in
1|3|5) B="Fuerza, cuerpo completo · $SER:
• $EMP
• $TIR
• $PIE
• $COR" ;;
2|4) B="Cardio en casa: $CAR" ;;
6) B="Sábado: $SAB" ;;
esac
TXT="💪 Calistenia - semana $S de 52 · fase $F
7-8 AM: 10 min calentamiento
$B
10 min estirar"
[ $(( S % 4 )) = 0 ] || [ "$S" = 1 ] && [ "$DOW" = 6 ] && TXT="$TXT
📏 Test de nivel: máximo de flexiones (tu variante), sentadillas en 1 min y plancha. Anótalo en Obsidian"
[ "$DOW" = 1 ] && TXT="$TXT
⬆️ Si haces todas las series limpias 2 sesiones seguidas, sube al ejercicio de la siguiente fase sin esperar"
if [ "${DRY:-}" = 1 ]; then echo "$TXT"; else exec "$HOME/bin/wa-yo.sh" "$TXT"; fi
