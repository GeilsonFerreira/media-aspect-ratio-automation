import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PASTA_ENTRADA = "entrada"
PASTA_SAIDA = "saida"

LARGURA = 1920
ALTURA = 1080
BLUR = 30

EXTENSOES_VIDEO = {".mp4", ".mov", ".mkv", ".avi", ".wmv", ".flv", ".webm"}

os.makedirs(PASTA_ENTRADA, exist_ok=True)
os.makedirs(PASTA_SAIDA, exist_ok=True)

def converter_para_16x9_blur(caminho_entrada):
    nome_arquivo = os.path.basename(caminho_entrada)
    nome_sem_ext, _ = os.path.splitext(nome_arquivo)
    caminho_saida = os.path.join(PASTA_SAIDA, f"{nome_sem_ext}_16x9.mp4")

    comando = [
        "ffmpeg", "-y", "-i", caminho_entrada,
        "-filter_complex",
        (
            f"[0:v]scale={LARGURA}:{ALTURA}:force_original_aspect_ratio=increase,"
            f"crop={LARGURA}:{ALTURA},boxblur={BLUR}:{BLUR}[bg];"
            f"[0:v]scale={LARGURA}:{ALTURA}:force_original_aspect_ratio=decrease[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2"
        ),
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        caminho_saida
    ]

    print(f"\n[🎬] Convertendo: {nome_arquivo}")
    proc = subprocess.run(comando)
    
    # Verifica se o arquivo de saída foi criado e tem tamanho
    if os.path.isfile(caminho_saida) and os.path.getsize(caminho_saida) > 1000:
        print(f"[✅] Salvo em: {caminho_saida}")
    else:
        print(f"[❌] Falha na conversão de: {nome_arquivo}")

def processar_existentes():
    print("[🔍] Verificando vídeos já existentes...")
    for arquivo in os.listdir(PASTA_ENTRADA):
        caminho = os.path.join(PASTA_ENTRADA, arquivo)
        if os.path.isfile(caminho):
            _, ext = os.path.splitext(arquivo)
            if ext.lower() in EXTENSOES_VIDEO:
                time.sleep(5)  # espera 5s para garantir arquivo completo
                converter_para_16x9_blur(caminho)

class MonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            _, ext = os.path.splitext(event.src_path)
            if ext.lower() in EXTENSOES_VIDEO:
                time.sleep(5)  # espera 5s para garantir arquivo completo
                converter_para_16x9_blur(event.src_path)

if __name__ == "__main__":
    print(f"[🚀] Monitorando pasta '{PASTA_ENTRADA}' para novos vídeos...")
    processar_existentes()

    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, PASTA_ENTRADA, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
