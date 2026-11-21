#!/bin/bash
# RECEITA KLING — validada no poa2 16:9 (doc/receita-kling.md).
#
#   ./render_kling.sh <kf_a.png> <saida.mp4> <arquivo-de-prompt.md> [duracao] [resolucao]
#
# kf_a.png  = a MAQUETE ja montada no rig (scripts/kf_a.py). NAO a foto de referencia.
# prompt    = arquivo de texto com o prompt integral, em ingles (prompts/*.md).
#
# SEM --tailImage e SEM --prefer_multi_shots: plano unico continuo.
#   - tailImage faz o modelo MORFAR A->B em vez de simular. Foi a causa de "a destruicao
#     veio por tras" e "os predios se dissolveram".
#   - multi-shot introduz cortes, proibidos pelo guia AVCC.
# O ratio do video vem do ratio do kf_a: o kling-video-v3_0 nao tem argumento de aspect ratio.
set -u
KF="$1"; DEST="$2"; PROMPT_FILE="$3"; DUR="${4:-15}"; RES="${5:-1080p}"
[ -f "$KF" ] || { echo "keyframe nao encontrado: $KF"; exit 1; }
[ -f "$PROMPT_FILE" ] || { echo "prompt nao encontrado: $PROMPT_FILE"; exit 1; }
mkdir -p "$(dirname "$DEST")"
P=$(cat "$PROMPT_FILE")

# --poll 0 na submissao + query_tasks: o poll longo do CLI cai (MCP -32001 / fetch failed)
# enquanto o job termina normal. O job e pago e nao cancela, entao a resposta crua e gravada
# ANTES de qualquer parse — perder o generation_id e perder o job.
kling image_to_video --image "$KF" --model kling-video-v3_0 --duration "$DUR" \
  --resolution "$RES" --enable_audio true --prefer_multi_shots false \
  --poll 0 "$P" > "$DEST.submit.json" 2>&1
GID=$(grep -oE 'A[A-Za-z0-9_-]{40,}' "$DEST.submit.json" | head -1)
[ -n "$GID" ] || { echo "SEM generation_id"; tail -5 "$DEST.submit.json"; exit 1; }
echo "generation_id: $GID"

kling query_tasks --poll 900 "$GID" > "$DEST.json" 2>&1
u=$(grep -o 'https://[^"]*output\.mp4[^"]*' "$DEST.json" | tail -1)
if [ -n "$u" ]; then
  curl -s -o "$DEST" "$u" && echo "OK $DEST"
else
  echo "SEM URL — reconsulte (URLs do Kling expiram em 24h):"
  echo "  kling query_tasks --poll 900 $GID"
  tail -3 "$DEST.json"
fi
