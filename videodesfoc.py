import os
import time
from moviepy import VideoFileClip, CompositeVideoClip
from PIL import Image, ImageFilter
import numpy as np

# Pastas
PASTA_ENTRADA = "entrada"
PASTA_SAIDA = "saida"

# Cria as pastas, se não existirem
os.makedirs(PASTA_ENTRADA, exist_ok=True)
os.makedirs(PASTA_SAIDA, exist_ok=True)

def gaussian_blur_frame(frame, sigma=20):
    """Aplica desfoque gaussiano em um frame usando Pillow."""
    img = Image.fromarray(frame)
    img = img.filter(ImageFilter.GaussianBlur(radius=sigma))
    return np.array(img)

def converter_para_16x9_com_desfoque(caminho_video, caminho_saida):
    """Converte qualquer vídeo não 16:9 para 16:9 com fundo desfocado."""
    try:
        with VideoFileClip(caminho_video) as video:
            largura, altura = video.size
            proporcao = largura / altura

            # Proporção 16:9 = 1.777...
            if abs(proporcao - 16/9) < 0.01:
                print(f"[✔] {os.path.basename(caminho_video)} já está em 16:9. Pulando...")
                return

            print(f"[i] {os.path.basename(caminho_video)} não está em 16:9. Criando fundo desfocado...")

            # Define dimensões finais
            final_width = largura if largura > altura else int(altura * 16 / 9)
            final_height = altura if altura > largura else int(largura * 9 / 16)

            # Cria vídeo de fundo desfocado
            fundo = video.resized(width=final_width, height=final_height).image_transform(
                lambda frame: gaussian_blur_frame(frame, sigma=50)
            )

            # Redimensiona vídeo original proporcionalmente para caber no 16:9
            if proporcao > 16/9:
                video_redimensionado = video.resized(width=final_width)
            else:
                video_redimensionado = video.resized(height=final_height)

            # Centraliza vídeo no fundo
            video_centralizado = video_redimensionado.with_position("center")

            # Combina vídeo original com fundo desfocado e centralizado
            final = CompositeVideoClip([
                fundo,
                video_redimensionado.with_position("center")
            ])


            # Exporta
            final.write_videofile(
                caminho_saida,
                codec="libx264",
                audio_codec="aac"
            )

            print(f"[✔] Vídeo salvo em: {caminho_saida}")

    except Exception as e:
        print(f"[❗] Erro ao processar {os.path.basename(caminho_video)}: {e}")

def monitorar_pasta():
    """Fica observando a pasta e processa novos vídeos."""
    print(f"[🚀] Monitorando '{PASTA_ENTRADA}' (aguarde).")
    arquivos_processados = set()

    while True:
        for arquivo in os.listdir(PASTA_ENTRADA):
            caminho_arquivo = os.path.join(PASTA_ENTRADA, arquivo)
            if arquivo.lower().endswith((".mp4", ".mov", ".avi", ".mkv")) and caminho_arquivo not in arquivos_processados:
                arquivos_processados.add(caminho_arquivo)

                print(f"[➤] Abrindo: {arquivo}")
                caminho_saida = os.path.join(PASTA_SAIDA, arquivo)

                converter_para_16x9_com_desfoque(caminho_arquivo, caminho_saida)

        time.sleep(2)

if __name__ == "__main__":
    monitorar_pasta()
