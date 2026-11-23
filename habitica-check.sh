#!/bin/bash
# Si la daily <alias> de Habitica toca hoy y no está marcada, reclama por WhatsApp. Uso: habitica-check.sh alias "mensaje"
set -euo pipefail
. "$(dirname "$0")/.habitica"
J=$(curl -sf "https://habitica.com/api/v3/tasks/$1" -H "x-api-user: $HAB_USER" -H "x-api-key: $HAB_KEY" -H "x-client: $HAB_USER-RutaPro")
P=$(python3 -c "import json,sys;t=json.loads(sys.argv[1])[\"data\"];print(int(t[\"isDue\"] and not t[\"completed\"]))" "$J")
[ "$P" = 1 ] || exit 0
[ "${DRY:-}" = 1 ] && { echo "PENDIENTE: $2"; exit 0; }
exec "$HOME/bin/wa-yo.sh" "$2"
