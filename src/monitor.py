import time
from pathlib import Path

from moviepy import VideoFileClip
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from video_processor import VideoProcessor
from image_processor import ImageProcessor
from logger import get_logger

from config import (
    PASTA_ENTRADA,
    PASTA_SAIDA,
    FUNDO_PADRAO,
    FORMATOS_VIDEO,
    FORMATOS_IMAGEM,
)

logger = get_logger(__name__)


class MediaMonitorHandler(FileSystemEventHandler):
    """
    Monitora a pasta de entrada e converte qualquer mídia
    (imagem ou vídeo) para MP4 em 16:9.
    """

    def __init__(self):
        self.video_processor = VideoProcessor(
            background_path=Path(FUNDO_PADRAO)
        )

        self.image_processor = ImageProcessor(
            background_path=Path(FUNDO_PADRAO)
        )

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Aguarda finalização da cópia
        time.sleep(2)

        extension = file_path.suffix.lower()

        if extension in FORMATOS_VIDEO:
            self._handle_video(file_path)

        elif extension in FORMATOS_IMAGEM:
            self._handle_image(file_path)

        else:
            logger.info(f"Arquivo ignorado: {file_path.name}")

    def _handle_video(self, file_path: Path):
        try:
            clip = VideoFileClip(str(file_path))
            w, h = clip.w, clip.h
            clip.close()

            output_path = PASTA_SAIDA / f"{file_path.stem}.mp4"

            if output_path.exists():
                logger.info(f"Vídeo já processado: {output_path.name}")
                return

            logger.info(
                f"Processando vídeo: {file_path.name} ({w}x{h})"
            )

            self.video_processor.process(file_path, output_path)

            logger.info(f"Vídeo finalizado: {output_path.name}")

        except Exception as e:
            logger.exception(
                f"Erro ao processar vídeo {file_path.name}: {e}",
                exc_info=True
            )

    def _handle_image(self, file_path: Path):
        try:
            output_path = PASTA_SAIDA / f"{file_path.stem}.mp4"

            if output_path.exists():
                logger.info(f"Imagem já processada: {output_path.name}")
                return

            logger.info(f"Processando imagem: {file_path.name}")

            # Imagem vira vídeo MP4
            self.image_processor.process(file_path, output_path)

            logger.info(f"Imagem finalizada: {output_path.name}")

        except Exception as e:
            logger.exception(
                f"Erro ao processar imagem {file_path.name}: {e}",
                exc_info=True
            )


def start_monitoring():
    PASTA_ENTRADA.mkdir(parents=True, exist_ok=True)
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

    observer = Observer()
    handler = MediaMonitorHandler()

    observer.schedule(handler, str(PASTA_ENTRADA), recursive=False)
    observer.start()

    logger.info(
        f"Monitorando pasta '{PASTA_ENTRADA.resolve()}' — Ctrl+C para sair"
    )

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Monitoramento encerrado.")

    observer.join()
