# Paco · Padel Coach powered by AI

Landing de validación: el usuario se apunta (nombre, apellido, email), y si ya tiene el video de un partido lo sube; si no, tiene 10 días para grabarlo y subirlo gratis.

## Estructura
- `public/index.html` — la landing (HTML estático, sin build). `demo.mp4` y `poster.jpg` son el video demo y su portada.
- `tools/render_demo.py` — genera el video demo (PIL + ffmpeg) a partir del clip 3D original.
- `firebase.json`, `firestore.rules`, `storage.rules` — Firebase Hosting + Firestore (`signups`) + Storage (`uploads/`).

## Modo demo vs. producción
En `public/index.html`, `FIREBASE_CONFIG = null` → modo demo (no envía nada, simula la subida). Para producción, pegar ahí el objeto de configuración web del proyecto Firebase.

## Desplegar
```bash
npm i -g firebase-tools
firebase login
firebase use --add            # elegir el proyecto
firebase deploy               # hosting + reglas
```
DNS en Cloudflare: registros en modo **DNS only** (nube gris), nunca Proxied.

## Desarrollo local
```bash
python3 -m http.server 8790 --directory public
```
