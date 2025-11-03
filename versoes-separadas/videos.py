# ===============
# Importar as bibliotecas
# ===============
import os
import time
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PASTA_ENTRADA = 'entrada'
PASTA_SAIDA = 'saida'
FUNDO_IMAGEM = 'fundo_padrao.jpg'  # deve estar em 16:9

def is_vertical(video_path):
    try:
        clip = VideoFileClip(video_path)
        w, h = clip.size
        clip.close()
        return h > w and round(h/w, 1) == round(16/9, 1)
    except Exception as e:
        print(f"Erro ao verificar formato: {e}")
        return False

def processar_video(video_path):
    try:
        print(f"Processando: {video_path}")
        clip = VideoFileClip(video_path)
        
        fundo = ImageClip(FUNDO_IMAGEM).with_duration(clip.duration)
        fundo = fundo.resized((1280, 720))
        
        video_resized = clip.resized(height=720)
        pos_x = int((1280 - video_resized.w) / 2)
        video_resized = video_resized.with_position((pos_x, 0))
        
        final = CompositeVideoClip([fundo, video_resized])
        nome_saida = os.path.basename(video_path)
        saida_path = os.path.join(PASTA_SAIDA, nome_saida)
        
        final.write_videofile(saida_path, codec="libx264", audio_codec="aac")
        clip.close()
        print(f"Salvo em: {saida_path}")
    except Exception as e:
        print(f"Erro no processamento: {e}")

class MonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            time.sleep(2)
            if is_vertical(event.src_path):
                processar_video(event.src_path)
            else:
                print("Vídeo ignorado (não é 9:16)")

if __name__ == "__main__":
    os.makedirs(PASTA_ENTRADA, exist_ok=True)
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    print(f"Monitorando pasta: {PASTA_ENTRADA}")
    observer = Observer()
    observer.schedule(MonitorHandler(), path=PASTA_ENTRADA, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
