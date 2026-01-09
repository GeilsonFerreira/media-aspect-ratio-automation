# src/image_processor.py
from pathlib import Path

from PIL import Image
from moviepy import ImageClip

from config import OUTPUT_RESOLUTION
from logger import get_logger

logger = get_logger(__name__)


class ImageProcessor:
    """
    Converte imagens de qualquer proporção em vídeo MP4 (16:9),
    aplicando fundo e centralização automática.
    """

    def __init__(self, background_path: Path, duration: int = 7):
        self.background_path = background_path
        self.duration = duration

        if not self.background_path.exists():
            raise FileNotFoundError(
                f"Imagem de fundo não encontrada: {self.background_path}"
            )

    def process(self, image_path: Path, output_path: Path) -> None:
        """
        Processa uma imagem e gera um vídeo MP4 em 16:9.
        """
        clip = None
        temp_image = None

        try:
            logger.info(f"Processando imagem: {image_path.name}")

            # --- Abre imagem e fundo ---
            with Image.open(image_path).convert("RGBA") as img, \
                 Image.open(self.background_path).convert("RGBA") as background:

                background = background.resize(
                    OUTPUT_RESOLUTION, Image.Resampling.LANCZOS
                )

                img_resized = self._resize_to_fit(img, background)
                composed = self._compose_image(background, img_resized)

                # --- Salva imagem temporária ---
                temp_image = output_path.with_suffix(".tmp.png")
                composed.convert("RGB").save(temp_image)

            logger.debug(
                f"Gerando vídeo {OUTPUT_RESOLUTION} por {self.duration}s"
            )

            # --- Cria vídeo MP4 ---
            clip = (
                ImageClip(str(temp_image))
                .with_duration(self.duration)
            )

            output_path.parent.mkdir(parents=True, exist_ok=True)

            clip.write_videofile(
                str(output_path),
                fps=30,
                codec="libx264",
                audio=False,
                preset="medium",
                threads=4,
                ffmpeg_params=["-pix_fmt", "yuv420p"],
            )

            logger.info(f"Imagem convertida para vídeo: {output_path.name}")

        except Exception as e:
            logger.exception(
                f"Erro ao processar imagem {image_path.name}: {e}"
            )
            raise

        finally:
            if clip:
                clip.close()
            if temp_image and temp_image.exists():
                temp_image.unlink()

    def _resize_to_fit(
        self, image: Image.Image, background: Image.Image
    ) -> Image.Image:
        """
        Redimensiona a imagem mantendo proporção.
        """
        img_w, img_h = image.size
        bg_w, bg_h = background.size

        scale = min(bg_w / img_w, bg_h / img_h)
        new_size = (int(img_w * scale), int(img_h * scale))

        logger.debug(f"Redimensionando imagem para {new_size}")

        return image.resize(new_size, Image.Resampling.LANCZOS)

    def _compose_image(
        self, background: Image.Image, image: Image.Image
    ) -> Image.Image:
        """
        Centraliza a imagem sobre o fundo.
        """
        bg_w, bg_h = background.size
        img_w, img_h = image.size

        offset_x = (bg_w - img_w) // 2
        offset_y = (bg_h - img_h) // 2

        composed = background.copy()
        composed.paste(image, (offset_x, offset_y), image)

        return composed
