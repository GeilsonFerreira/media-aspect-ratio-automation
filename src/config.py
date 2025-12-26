from pathlib import Path

PASTA_ENTRADA = Path("entrada")
PASTA_SAIDA = Path("saida")

PASTA_IMAGENS = PASTA_SAIDA / "imagens"
PASTA_VIDEOS = PASTA_SAIDA / "videos"

FUNDO_PADRAO = Path("fundo_padrao.jpg")

FORMATOS_VIDEO = (".mp4", ".mov", ".avi", ".mkv", ".webm")
FORMATOS_IMAGEM = (".jpg", ".jpeg", ".png", ".webp")

OUTPUT_RESOLUTION = (1280, 720)  # 16:9 padrão
