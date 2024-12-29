from flask import Flask, render_template, request, jsonify
import yt_dlp as youtube_dl

app = Flask(__name__)

def descargar_contenido(url, modo):
    try:
        # Limpiar la URL eliminando parámetros de lista de reproducción si existen
        if '&list=' in url:
            url = url.split('&list=')[0]

        # Configuración según el modo seleccionado (video o audio)
        if modo == "video":
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'descargas/%(title)s.%(ext)s',  # Guardar con título del video
            }
        elif modo == "audio":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'descargas/%(title)s.%(ext)s',
                'postprocessors': [{  # Procesador para extraer audio
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',  # Calidad de audio
                }],
                'ffmpeg_location': r'C:\Users\Joseluis\Desktop\web\DESCARGA-YT\ffmpeg\bin\ffmpeg.exe'
            }
        else:
            return "Modo no válido"

        # Descargar usando yt_dlp
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return f"Descarga completada ({modo})"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url', '')
    modo = data.get('modo', 'video')
    
    # Validar URL
    if not url:
        return jsonify({'error': 'URL no proporcionada'}), 400

    # Llamar a la función de descarga
    mensaje = descargar_contenido(url, modo)
    return jsonify({'message': mensaje})

if __name__ == '__main__':
    app.run(debug=True)
