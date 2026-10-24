from flask import Flask, render_template, request, jsonify, send_file, after_this_request
from pathlib import Path
from urllib.parse import urlparse
import tempfile
import shutil
import subprocess
import yt_dlp
import imageio_ffmpeg

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4096

def valid_url(url):
    p = urlparse(url)
    return p.scheme == "https" and (p.hostname or "").lower() in {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be", "music.youtube.com"}

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/download")
def download():
    url = request.form.get("url", "").strip()
    mode = request.form.get("mode", "video")
    if not valid_url(url) or mode not in {"video", "audio"}:
        return jsonify(error="Enlace o formato no válido."), 400
    directory = Path(tempfile.mkdtemp(prefix="ytapp_"))
    options = {
        "ffmpeg_location": imageio_ffmpeg.get_ffmpeg_exe(),
        "outtmpl": str(directory / "%(title).100s-%(id)s.%(ext)s"),
        "noplaylist": True,
        "restrictfilenames": True,
        "quiet": True,
        "max_filesize": 2 * 1024**3,
    }
    if mode == "audio":
        options.update({"format": "bestaudio/best", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "320"}]})
    else:
        options.update({"format": "bestvideo*+bestaudio/best", "merge_output_format": "mp4"})
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        candidates = [p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in {".mp3", ".mp4", ".mkv", ".webm"}]
        if not candidates:
            raise RuntimeError("No se generó un archivo.")
        output = max(candidates, key=lambda p: p.stat().st_size)
        @after_this_request
        def cleanup(response):
            response.call_on_close(lambda: shutil.rmtree(directory, ignore_errors=True))
            return response
        return send_file(output, as_attachment=True, download_name=output.name)
    except Exception as exc:
        shutil.rmtree(directory, ignore_errors=True)
        return jsonify(error=f"No se pudo descargar el contenido: {str(exc)[:180]}"), 400

if __name__ == "__main__":
    app.run(debug=False)
