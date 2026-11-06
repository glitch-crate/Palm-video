#!/usr/bin/env bash
# Uso: encode.sh <cartella_png> <clip_sotto|-> <uscita_base> <secondo_fotogramma_png>
# Produce: <base>-alpha.mov (ProRes 4444 + alpha), <base>-anteprima.mp4 (grafica sopra la clip), <base>.png (fotogramma chiave)
set -euo pipefail
PNG="$1"; CLIP="$2"; BASE="$3"; KEY="$4"; N="${5:-99999}"
ffmpeg -v error -y -framerate 24 -i "$PNG/f_%05d.png" -frames:v "$N" \
  -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le -alpha_bits 16 -vendor apl0 "$BASE-alpha.mov"
if [ "$CLIP" != "-" ]; then
  ffmpeg -v error -y -i "$CLIP" -framerate 24 -i "$PNG/f_%05d.png" \
    -filter_complex "[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p" -an \
    -c:v libx264 -crf 17 -preset medium -movflags +faststart "$BASE-anteprima.mp4"
else
  ffmpeg -v error -y -f lavfi -i "color=c=0x6b6b6b:s=1920x1080:r=24" -framerate 24 -i "$PNG/f_%05d.png" \
    -filter_complex "[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p" \
    -c:v libx264 -crf 17 -preset medium -movflags +faststart "$BASE-anteprima.mp4"
fi
cp "$PNG/f_$(printf %05d "$KEY").png" "$BASE.png"
