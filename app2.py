# ===============
# Importar as bibliotecas
# ===============
import os
import time
import sys
from pathlib import Path
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ===============
# Função para obter caminhos corretos no .exe
# ===============
def recurso_absoluto(nome_arquivo):
    """Garante o caminho correto mesmo quando empacotado com PyInstaller"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, nome_arquivo)

# ===============
# Configurações
# ===============
PASTA_BASE = Path.home() / "D:/MeusProjetos/Fundo_Automatico"
PASTA_ENTRADA = str(PASTA_BASE / "entrada")
PASTA_SAIDA = str(PASTA_BASE / "saida")
FUNDO_PADRAO = recurso_absoluto('fundo_padrao.jpg')  # deve estar em 16:9

# ===============
# Funções de processamento
# ===============
def is_vertical(video_path):
    try:
        clip = VideoFileClip(video_path)
        w, h = clip.size
        clip.close()
        return h > w and round(h / w, 1) == round(16 / 9, 1)
    except Exception as e:
        print(f"Erro ao verificar formato do vídeo: {e}")
        return False

def processar_video(video_path):
    try:
        print(f"Processando vídeo: {video_path}")
        clip = VideoFileClip(video_path)
        
        fundo = ImageClip(FUNDO_PADRAO).with_duration(clip.duration)
        fundo = fundo.resized((1280, 720))
        
        video_resized = clip.resized(height=720)
        pos_x = int((1280 - video_resized.w) / 2)
        video_resized = video_resized.with_position((pos_x, 0))
        
        final = CompositeVideoClip([fundo, video_resized])
        nome_saida = os.path.basename(video_path)
        saida_path = os.path.join(PASTA_SAIDA, nome_saida)
        
        final.write_videofile(saida_path, codec="libx264", audio_codec="aac")
        clip.close()
        print(f"[✔] Vídeo salvo em: {saida_path}")
    except Exception as e:
        print(f"Erro no processamento do vídeo: {e}")

def processar_imagem(imagem_path):
    try:
        print(f"Processando imagem: {imagem_path}")
        
        img = Image.open(imagem_path).convert("RGBA")
        fundo = Image.open(FUNDO_PADRAO).convert("RGBA")

        img_w, img_h = img.size
        fundo_w, fundo_h = fundo.size

        proporcao = min(fundo_w / img_w, fundo_h / img_h)
        novo_tamanho = (int(img_w * proporcao), int(img_h * proporcao))
        img_redimensionada = img.resize(novo_tamanho, Image.Resampling.LANCZOS)

        offset_x = (fundo_w - novo_tamanho[0]) // 2
        offset_y = (fundo_h - novo_tamanho[1]) // 2

        fundo.paste(img_redimensionada, (offset_x, offset_y), img_redimensionada)
        fundo = fundo.convert("RGB")
        
        nome_saida = os.path.basename(imagem_path)
        saida_path = os.path.join(PASTA_SAIDA, nome_saida)
        
        os.makedirs(os.path.dirname(saida_path), exist_ok=True)
        fundo.save(saida_path)
        
        print(f"[✔] Imagem salva em: {saida_path}")
    except Exception as e:
        print(f"Erro no processamento da imagem: {e}")

# ===============
# Monitoramento de arquivos
# ===============
class MonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        caminho_arquivo = event.src_path.lower()
        time.sleep(2)

        if caminho_arquivo.endswith(('.mp4', '.mov', '.avi', '.mkv')):
            if is_vertical(event.src_path):
                processar_video(event.src_path)
            else:
                print(f"Vídeo '{os.path.basename(event.src_path)}' ignorado (não é 9:16).")
        elif caminho_arquivo.endswith(('.jpg', '.jpeg', '.png')):
            processar_imagem(event.src_path)
        else:
            print(f"Arquivo '{os.path.basename(event.src_path)}' ignorado (formato não suportado).")

# ===============
# Execução principal
# ===============
if __name__ == "__main__":
    os.makedirs(PASTA_ENTRADA, exist_ok=True)
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    print(f"[🔁] Monitorando a pasta:\n{PASTA_ENTRADA}\nPressione Ctrl+C para sair.")
    observer = Observer()
    observer.schedule(MonitorHandler(), path=PASTA_ENTRADA, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
