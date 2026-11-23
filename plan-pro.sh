#!/bin/bash
# Recordatorio diario del plan profesional (5-7 AM L-V + ejercicio 7-8 AM L-S, domingo 7-11 AM). Uso: plan-pro.sh   (HOY=AAAA-MM-DD DRY=1 para probar)
set -euo pipefail
DIR="$(dirname "$0")"
HOY="${HOY:-$(TZ=America/Santo_Domingo date +%F)}"
DOW=$(date -d "$HOY" +%u)   # 1=lunes ... 7=domingo
FILA=$(awk -F'\t' -v h="$HOY" '!/^#/ && $1<=h {f=$0} END{print f}' "$DIR/semanas.tsv")
[ -n "$FILA" ] || exit 0
IFS=$'\t' read -r INI SEM TEMA DOM REC <<<"$FILA"
# el primer día del plan (martes 24/11) arranca con teoría, no con "lo de ayer"
[ "$HOY" = "$INI" ] && [ "$SEM" = 1 ] && DOW=1
# pasadas 7 días de la última semana, el plan terminó
[ $(( ( $(date -d "$HOY" +%s) - $(date -d "$INI" +%s) ) / 86400 )) -lt 7 ] || exit 0
case $DOW in
1) M="Teoría (5-6:30 AM): $TEMA
🇺🇸 6:30-7:00: escucha 6 Minute English (BBC) y anota 5 frases" ;;
2) M="Práctica (5-6:30 AM): ejercicios de lo de ayer. Tema: $TEMA
🇺🇸 6:30-7:00: graba 2 min explicando en inglés lo que practicaste" ;;
3) M="Teoría 2 (5-6:30 AM): sigue con $TEMA
🇺🇸 6:30-7:00: 6 Minute English repitiendo en voz alta (shadowing)" ;;
4) M="Práctica 2 (5-6:30 AM): cierra el tema y prepara lo del domingo: $DOM
🇺🇸 6:30-7:00: graba 2 min explicando en inglés el tema de la semana" ;;
5) M="Viernes 🇺🇸 5-6 AM: conversación de 30 min en inglés (voz con IA o Tandem) + repasa tus errores
6-7 AM: escribe y publica tu post semanal de LinkedIn" ;;
6) M="Sábado: solo ejercicio, el resto del día es de la familia" ;;
7) M="Bloque de proyecto (7-11 AM): $DOM. Al terminar, súbelo a GitHub y marca la semana como hecha" ;;
esac
# ejercicio 7-8 AM L-S, en casa sin equipo; sube cada 8 semanas
if   [ "$SEM" -le 8 ];  then R="3 rondas x 10 reps"; C="caminata rápida 40 min"
elif [ "$SEM" -le 16 ]; then R="4 rondas x 12-15 reps"; C="intervalos: 2 min trote + 1 min caminar, 40 min"
else                         R="5 rondas x 15-20 reps"; C="trote continuo 30-40 min"; fi
case $DOW in
1) E="Tren superior ($R): flexiones, fondos en silla, remo bajo la mesa, pike push-ups, plancha 40 s" ;;
2|5) E="Piernas y core ($R): sentadillas, zancadas, puente de glúteos, elevación de talones, plancha lateral 30 s" ;;
3) E="Cardio: $C" ;;
4) E="Cuerpo completo ($R): burpees, sentadillas, flexiones, mountain climbers, superman" ;;
6) E="Cardio largo: $C" ;;
*) E="" ;;
esac
TXT="📈 Plan pro - semana $SEM de 24
$M"
[ -n "$E" ] && TXT="$TXT
💪 7-8 AM: 10 min calentamiento + $E + 10 min estirar"
case "$SEM-$DOW" in 1-6|8-6|16-6|24-6) TXT="$TXT
📏 Test: máximo de flexiones seguidas y de sentadillas en 1 min. Anótalo en Obsidian" ;; esac
[ "$REC" != "-" ] && [ "$DOW" != 5 ] && [ "$DOW" != 6 ] && TXT="$TXT
Recurso: $REC"
if [ "${DRY:-}" = 1 ]; then echo "$TXT"; else exec "$HOME/bin/wa-yo.sh" "$TXT"; fi
