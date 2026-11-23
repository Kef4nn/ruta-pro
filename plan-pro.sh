#!/bin/bash
# Recordatorio diario del plan profesional (5-7 AM L-V, domingo 7-11 AM). Uso: plan-pro.sh   (HOY=AAAA-MM-DD DRY=1 para probar)
set -euo pipefail
DIR="$(dirname "$0")"
HOY="${HOY:-$(TZ=America/Santo_Domingo date +%F)}"
DOW=$(date -d "$HOY" +%u)   # 1=lunes ... 7=domingo
FILA=$(awk -F'\t' -v h="$HOY" '!/^#/ && $1<=h {f=$0} END{print f}' "$DIR/semanas.tsv")
[ -n "$FILA" ] || exit 0
IFS=$'\t' read -r INI SEM TEMA DOM REC <<<"$FILA"
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
6) exit 0 ;;
7) M="Bloque de proyecto (7-11 AM): $DOM. Al terminar, súbelo a GitHub y marca la semana como hecha" ;;
esac
TXT="📈 Plan pro - semana $SEM de 24
$M"
[ "$REC" != "-" ] && [ "$DOW" != 5 ] && TXT="$TXT
Recurso: $REC"
if [ "${DRY:-}" = 1 ]; then echo "$TXT"; else exec "$HOME/bin/wa-yo.sh" "$TXT"; fi
