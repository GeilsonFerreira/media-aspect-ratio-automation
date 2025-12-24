import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.video_processor import VideoProcessor
from src.logger import get_logger
from src.config import (
    PASTA_ENTRADA,
    PASTA_SAIDA,
    FUNDO_PADRAO,
    FORMATOS_VIDEO,
    FORMATOS_IMAGEM,
)

logger = get_logger(__name__)


class MediaMonitorHandler(FileSystemEventHandler):
    """
    Monitora a pasta de entrada e encaminha arquivos
    para o processador adequado.
    """

    def __init__(self):
        self.video_processor = VideoProcessor(
            background_path=FORMATOS_IMAGEM
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
        else:
            logger.info(f"Arquivo ignorado: {file_path.name}")

    def _handle_video(self, file_path: Path):
        try:
            if not self.video_processor.is_vertical_9x16(file_path):
                logger.info(
                    f"Vídeo ignorado (não é 9:16): {file_path.name}"
                )
                return

            output_path = PASTA_SAIDA / file_path.name

            if output_path.exists():
                logger.info(
                    f"Arquivo já processado: {output_path.name}"
                )
                return

            logger.info(f"Processando vídeo: {file_path.name}")
            self.video_processor.process(file_path, output_path)
            logger.info(f"Vídeo finalizado: {output_path.name}")

        except Exception as e:
            logger.exception(
                f"Erro ao processar vídeo {file_path.name}: {e}"
            )


def start_monitoring():
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
        observer.join()
        logger.info("Monitoramento encerrado")
