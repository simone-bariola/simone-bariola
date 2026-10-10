# Generador de la cabecera animada

`gen_header.py` genera `../header.svg`, la cabecera de mi perfil.

## Cómo funciona

- **La onda:** 260 puntos a lo ancho de la tarjeta. Cada punto mezcla una **senoidal pura** con una **señal tipo audio** según su posición: a la izquierda pesa la senoidal y hacia la derecha pesa el audio (interpolación *smoothstep*).
- **La señal de audio:** suma de armónicos (23, 41 y 67 ciclos), ruido filtrado y una envolvente con transitorios gaussianos, y por último una compresión suave con `tanh` para que la forma de onda se vea "llena", como en un DAW.
- **El movimiento:** se calculan 6 fotogramas con la fase desplazada y SVG los interpola con SMIL (`<animate>`). No usa JavaScript, por eso funciona dentro de un README de GitHub.
- **La entrada:** un cabezal de reproducción recorre la tarjeta y una máscara (`clipPath`) que crece de izquierda a derecha va "grabando" la onda.

## Regenerar

Requiere Python 3 y NumPy.

```bash
pip install numpy
python generador/gen_header.py
```

Los colores, textos y tiempos están en las constantes al inicio del script (`RED`, `CORAL`, `INTRO`, `LOOP`…).
