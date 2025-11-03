import os
import time
import sys
from datetime import datetime
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# =============== CONFIGURAÇÕES ===============
PASTA_ENTRADA = 'entrada'
PASTA_SAIDA = 'saida'
FUNDO_PADRAO = 'fundo_padrao.jpg'  # deve estar em 16:9
FORMATOS_VIDEO = ('.mp4', '.mov', '.avi', '.mkv')
FORMATOS_IMAGEM = ('.jpg', '.jpeg', '.png')

# =============== UTILITÁRIOS ===============
def log(msg):
    """Imprime mensagens com timestamp."""
    print(f"[{datetime.now():%H:%M:%S}] {msg}")

# =============== FUNÇÕES DE PROCESSAMENTO ===============
def is_vertical(video_path):
    """Verifica se o vídeo tem proporção 9:16."""
    try:
        clip = VideoFileClip(video_path)
        w, h = clip.size
        clip.close()
        return h > w and round(h/w, 1) == round(16/9, 1)
    except Exception as e:
        log(f"Erro ao verificar formato do vídeo: {e}")
        return False

def processar_video(video_path):
    """Adiciona fundo horizontal a vídeo vertical."""
    try:
        nome_saida = os.path.basename(video_path)
        saida_path = os.path.join(PASTA_SAIDA, nome_saida)

        if os.path.exists(saida_path):
            log(f"[⏩] Já existe: {saida_path} — ignorado.")
            return

        log(f"Processando vídeo: {video_path}")
        clip = VideoFileClip(video_path)

        fundo = ImageClip(FUNDO_PADRAO).with_duration(clip.duration).resized((1280, 720))
        video_redimensionado = clip.resized(height=720)

        pos_x = int((1280 - video_redimensionado.w) / 2)
        video_redimensionado = video_redimensionado.with_position((pos_x, 0))

        final = CompositeVideoClip([fundo, video_redimensionado])

        final.write_videofile(saida_path, codec="libx264", audio_codec="aac")
        clip.close()
        log(f"[✔] Vídeo salvo em: {saida_path}")
    except Exception as e:
        log(f"Erro no processamento do vídeo: {e}")

def processar_imagem(imagem_path):
    """Adiciona fundo horizontal a imagem vertical."""
    try:
        nome_saida = os.path.basename(imagem_path)
        saida_path = os.path.join(PASTA_SAIDA, nome_saida)

        if os.path.exists(saida_path):
            log(f"[⏩] Já existe: {saida_path} — ignorada.")
            return

        log(f"Processando imagem: {imagem_path}")

        with Image.open(imagem_path).convert("RGBA") as img, \
             Image.open(FUNDO_PADRAO).convert("RGBA") as fundo:

            img_w, img_h = img.size
            fundo_w, fundo_h = fundo.size

            proporcao = min(fundo_w / img_w, fundo_h / img_h)
            novo_tamanho = (int(img_w * proporcao), int(img_h * proporcao))
            img_redimensionada = img.resize(novo_tamanho, Image.Resampling.LANCZOS)

            offset_x = (fundo_w - novo_tamanho[0]) // 2
            offset_y = (fundo_h - novo_tamanho[1]) // 2
            fundo.paste(img_redimensionada, (offset_x, offset_y), img_redimensionada)

            fundo = fundo.convert("RGB")
            os.makedirs(os.path.dirname(saida_path), exist_ok=True)
            fundo.save(saida_path)

        log(f"[✔] Imagem salva em: {saida_path}")
    except Exception as e:
        log(f"Erro no processamento da imagem: {e}")

# =============== MONITORAMENTO ===============
class MonitorHandler(FileSystemEventHandler):
    """Classe para lidar com novos arquivos criados."""
    def on_created(self, event):
        if event.is_directory:
            return

        time.sleep(2)  # aguarda a cópia finalizar
        caminho_arquivo = event.src_path
        _, ext = os.path.splitext(caminho_arquivo)
        ext = ext.lower()

        if ext in FORMATOS_VIDEO:
            if is_vertical(caminho_arquivo):
                processar_video(caminho_arquivo)
            else:
                log(f"Vídeo '{os.path.basename(caminho_arquivo)}' ignorado (não é 9:16).")
        elif ext in FORMATOS_IMAGEM:
            processar_imagem(caminho_arquivo)
        else:
            log(f"Arquivo '{os.path.basename(caminho_arquivo)}' ignorado (formato não suportado).")

# =============== EXECUÇÃO PRINCIPAL ===============
if __name__ == "__main__":
    os.makedirs(PASTA_ENTRADA, exist_ok=True)
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    log(f"[🔁] Monitorando a pasta '{PASTA_ENTRADA}'... Pressione Ctrl+C para sair.")
    observer = Observer()
    observer.schedule(MonitorHandler(), path=PASTA_ENTRADA, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        log("[⛔] Monitoramento encerrado.")
