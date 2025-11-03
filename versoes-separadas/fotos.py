import os
import time
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Caminhos
PASTA_ENTRADA = "entrada"
PASTA_SAIDA = "saida"
FUNDO_16_9 = "fundo_padrao.jpg"  # Fundo 16:9 personalizado

def processar_imagem(imagem_vertical_path, output_path, fundo_path):
    img = Image.open(imagem_vertical_path).convert("RGBA")
    fundo = Image.open(fundo_path).convert("RGBA")

    # Redimensiona imagem vertical proporcionalmente (sem distorcer)
    img_w, img_h = img.size
    fundo_w, fundo_h = fundo.size

    proporcao = min(fundo_w / img_w, fundo_h / img_h)
    novo_tamanho = (int(img_w * proporcao), int(img_h * proporcao))
    img_redimensionada = img.resize(novo_tamanho, Image.Resampling.LANCZOS)

    # Centralizar a imagem vertical no fundo
    offset_x = (fundo_w - novo_tamanho[0]) // 2
    offset_y = (fundo_h - novo_tamanho[1]) // 2

    fundo.paste(img_redimensionada, (offset_x, offset_y), img_redimensionada)
    fundo = fundo.convert("RGB")  # Remove transparência para salvar em .jpg

    # Salvar imagem
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fundo.save(output_path)
    print(f"[✔] Imagem processada: {output_path}")

class MonitorPasta(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if not event.src_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            return

        time.sleep(1)  # Aguarda arquivo ser salvo por completo
        nome_arquivo = os.path.basename(event.src_path)
        caminho_saida = os.path.join(PASTA_SAIDA, nome_arquivo)
        processar_imagem(event.src_path, caminho_saida, FUNDO_16_9)

if __name__ == "__main__":
    print(f"[🔁] Monitorando pasta '{PASTA_ENTRADA}'... Pressione Ctrl+C para sair.")
    observer = Observer()
    observer.schedule(MonitorPasta(), path=PASTA_ENTRADA, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()