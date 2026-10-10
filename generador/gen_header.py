"""Genera header.svg para el README de perfil de GitHub (SMIL, sin JavaScript).
Entrada: un cabezal de reproducción recorre la tarjeta de izquierda a derecha dibujando
una onda que nace senoidal y se transforma en forma de onda de audio. Luego sigue en bucle.
"""
import numpy as np

W, H = 1000, 300
CY = 118                     # eje de la onda
X0, X1 = 40, 960
N = 260
INTRO = 2.8                  # segundos de la entrada
LOOP = 4.0

BG, CARD, LINE = "#0E0809", "#140B0D", "#2B181B"
TEXT, MUTED = "#F5ECEA", "#9A8784"
RED, RED2, CORAL = "#C81E2E", "#FF3D3D", "#FF8A5C"
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'Cascadia Code','SFMono-Regular',Consolas,'DejaVu Sans Mono',monospace"

xs = np.linspace(X0, X1, N)
t = np.linspace(0, 1, N)
edge = np.clip(np.minimum(t, 1 - t) / 0.04, 0, 1)                 # extremos suaves
blend = np.clip((t - 0.22) / 0.5, 0, 1); blend = blend * blend * (3 - 2 * blend)  # 0 = seno, 1 = audio

rng = np.random.default_rng(11)
noise_bank = rng.normal(size=N * 6)


def frame(k):
    ph = k * 2 * np.pi / 6
    sine = 0.55 * np.sin(2 * np.pi * 7 * t - ph)
    sig = (0.50 * np.sin(2 * np.pi * 23 * t + 1.3 * ph)
           + 0.28 * np.sin(2 * np.pi * 41 * t - 2.1 * ph)
           + 0.20 * np.sin(2 * np.pi * 67 * t + 0.7 * ph))
    nz = np.roll(noise_bank, k * 53)[:N]
    sig = sig + 0.45 * np.convolve(nz, [0.5, 0.5], mode="same")
    centers = (np.array([0.42, 0.58, 0.71, 0.86]) + 0.045 * k) % 1.0
    env = 0.25 + sum(np.exp(-((t - c) ** 2) / 0.0012) for c in centers)
    raw = sig * env
    raw = raw / np.percentile(np.abs(raw[t > 0.5]), 97)
    audio = np.tanh(1.5 * raw) / np.tanh(1.5)          # compresión suave: onda más "llena"
    y = (1 - blend) * sine + blend * audio * 0.95
    return 70 * y * edge


def d(ys):
    return "M" + " L".join(f"{x:.1f},{CY - y:.1f}" for x, y in zip(xs, ys))


FR = 6
frames = [frame(k) for k in range(FR)]
loop_vals = ";".join(d(f) for f in frames + [frames[0]])
splines = ";".join(["0.42 0 0.58 1"] * FR)

# barras de la forma de onda (solo donde ya es audio)
NB = 92
bx = np.linspace(X0, X1, NB)
idx = [np.argmin(abs(xs - x)) for x in bx]


def bars(f):
    return [max(3.0, 1.9 * np.abs(f[max(0, i - 2):i + 3]).max()) for i in idx]


bar_frames = [bars(f) for f in frames]

o = []
a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Simone Bariola — Mechatronics · Audio Hardware">')
a('<defs>')
a(f'<linearGradient id="wg" x1="{X0}" x2="{X1}" gradientUnits="userSpaceOnUse">'
  f'<stop offset="0" stop-color="{RED}" stop-opacity="0.55"/><stop offset="0.35" stop-color="{RED2}"/>'
  f'<stop offset="0.75" stop-color="{CORAL}"/><stop offset="1" stop-color="{RED2}" stop-opacity="0.7"/></linearGradient>')
a(f'<linearGradient id="bg" x1="{X0}" x2="{X1}" gradientUnits="userSpaceOnUse">'
  f'<stop offset="0.2" stop-color="{RED}" stop-opacity="0"/><stop offset="0.6" stop-color="{RED}" stop-opacity="0.55"/>'
  f'<stop offset="1" stop-color="{RED2}" stop-opacity="0.35"/></linearGradient>')
a(f'<radialGradient id="heat" cx="0.72" cy="0.38" r="0.55"><stop offset="0" stop-color="{RED}" stop-opacity="0.22"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>')
a('<filter id="blur" x="-5%" y="-60%" width="110%" height="220%"><feGaussianBlur stdDeviation="4"/></filter>')
# máscara que se "graba" de izquierda a derecha, al ritmo del cabezal
a(f'<clipPath id="rec"><rect x="0" y="0" width="0" height="{H}">'
  f'<animate attributeName="width" begin="0.2s" dur="{INTRO}s" from="0" to="{W}" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.5 0 0.4 1"/></rect></clipPath>')
a(f'<clipPath id="card"><rect x="8" y="8" width="{W-16}" height="{H-16}" rx="16"/></clipPath>')
a('</defs>')

a(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
a(f'<rect x="8" y="8" width="{W-16}" height="{H-16}" rx="16" fill="{CARD}" stroke="{LINE}"/>')
a('<g clip-path="url(#card)">')
a(f'<rect width="{W}" height="{H}" fill="url(#heat)"/>')

# regla de tiempo tipo DAW
a(f'<g stroke="{LINE}">')
for i, x in enumerate(np.arange(X0, X1 + 1, 23)):
    h = 9 if i % 8 == 0 else 4
    a(f'<line x1="{x:.0f}" y1="26" x2="{x:.0f}" y2="{26+h}"/>')
a('</g>')
for i, x in enumerate(np.arange(X0, X1 - 40, 23 * 8)):
    a(f'<text x="{x+4:.0f}" y="34" font-family="{MONO}" font-size="8.5" fill="{MUTED}" opacity="0.8">{i}:00</text>')
a(f'<line x1="{X0}" y1="{CY}" x2="{X1}" y2="{CY}" stroke="{LINE}" stroke-dasharray="2 6"/>')

# todo lo "grabado" queda dentro del clip que avanza
a('<g clip-path="url(#rec)">')
a('<g>')
for i, x in enumerate(bx):
    hs = [bf[i] for bf in bar_frames] + [bar_frames[0][i]]
    a(f'<rect x="{x-2:.1f}" y="{CY-hs[0]/2:.1f}" width="4" height="{hs[0]:.1f}" rx="2" fill="url(#bg)">'
      f'<animate attributeName="height" begin="{INTRO}s" dur="{LOOP}s" repeatCount="indefinite" calcMode="spline" keySplines="{splines}" values="{";".join(f"{h:.1f}" for h in hs)}"/>'
      f'<animate attributeName="y" begin="{INTRO}s" dur="{LOOP}s" repeatCount="indefinite" calcMode="spline" keySplines="{splines}" values="{";".join(f"{CY-h/2:.1f}" for h in hs)}"/></rect>')
a('</g>')
for stroke, width, extra, op in ((RED2, 7, 'filter="url(#blur)"', 0.5), ("url(#wg)", 2.2, "", 1)):
    a(f'<path d="{d(frames[0])}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round" opacity="{op}" {extra}>'
      f'<animate attributeName="d" begin="{INTRO}s" dur="{LOOP}s" repeatCount="indefinite" calcMode="spline" keySplines="{splines}" values="{loop_vals}"/></path>')
a('</g>')

# cabezal de reproducción
a(f'<g opacity="1"><line x1="0" y1="22" x2="0" y2="214" stroke="{RED2}" stroke-width="1.5"/>'
  f'<path d="M-6,18 L6,18 L0,26 Z" fill="{RED2}"/>'
  f'<animateTransform attributeName="transform" type="translate" begin="0.2s" dur="{INTRO}s" from="0 0" to="{W} 0" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.5 0 0.4 1"/>'
  f'<animate attributeName="opacity" begin="{INTRO}s" dur="0.4s" from="1" to="0" fill="freeze"/></g>')

# etiquetas de inicio/fin de la transformación
a(f'<text x="{X0}" y="206" font-family="{MONO}" font-size="9" letter-spacing="2" fill="{MUTED}" opacity="0">SINE'
  f'<animate attributeName="opacity" begin="0.6s" dur="0.6s" to="1" fill="freeze"/></text>')
a(f'<text x="{X1}" y="206" text-anchor="end" font-family="{MONO}" font-size="9" letter-spacing="2" fill="{CORAL}" opacity="0">AUDIO'
  f'<animate attributeName="opacity" begin="{INTRO}s" dur="0.6s" to="1" fill="freeze"/></text>')

# bloque de texto inferior
a(f'<line x1="{X0}" y1="222" x2="{X1}" y2="222" stroke="{LINE}"/>')


def fade(delay):
    return (f'<animate attributeName="opacity" begin="{delay}s" dur="0.8s" from="0" to="1" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" begin="{delay}s" dur="0.8s" from="0 10" to="0 0" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.2 0.7 0.3 1"/>')


a(f'<g opacity="0">{fade(INTRO - 0.4)}<text x="{X0-2}" y="268" font-family="{SANS}" font-size="44" font-weight="800" letter-spacing="-1.5" fill="{TEXT}">Simone Bariola</text></g>')
a(f'<g opacity="0">{fade(INTRO - 0.1)}'
  f'<text x="{X1}" y="249" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="2.5" fill="{CORAL}">MECHATRONICS · AUDIO HARDWARE</text>'
  f'<text x="{X1}" y="268" text-anchor="end" font-family="{SANS}" font-size="13.5" fill="{MUTED}">Hardware that sounds. Software that automates.</text></g>')
a('</g></svg>')

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "header.svg")
open(OUT, "w", encoding="utf-8").write("\n".join(o))
print("ok", sum(map(len, o)) // 1024, "KB")
