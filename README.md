# YouTube Downloader Pro

Aplicación local con Python, Flask, HTML y yt-dlp para descargar contenido propio o autorizado de YouTube.

## Requisitos
- Python 3.10+
- FFmpeg instalado y disponible en PATH

## Iniciar
```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```
Abre http://127.0.0.1:5000

El modo video intenta descargar la mejor combinación de video y audio; la calidad depende de la fuente y de los formatos disponibles. El MP3 de 320 kbps es una conversión: no mejora la calidad original. El servidor es para uso local; no lo publiques directamente sin controles de acceso, límites y endurecimiento de seguridad. Descarga solo contenido sobre el que tengas derechos o permiso y respeta las condiciones del servicio.
