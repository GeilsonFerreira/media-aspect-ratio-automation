from pathlib import Path
from PIL import Image

from src.logger import get_logger
from src.config import OUTPUT_RESOLUTION

logger = get_logger(__name__)


class ImageProcessor:
    """
    Processa imagens verticais (9:16), aplicando fundo horizontal (16:9)
    com centralização automática.
    """

    def __init__(self, background_path: Path):
        self.background_path = background_path

        if not self.background_path.exists():
            raise FileNotFoundError(
                f"Imagem de fundo não encontrada: {self.background_path}"
            )

    def process(self, input_path: Path, output_path: Path):
        """
        Processa uma imagem vertical e salva a versão final em 16:9.
        """
        try:
            logger.debug(f"Abrindo imagem: {input_path.name}")

            with Image.open(input_path).convert("RGBA") as img, \
                 Image.open(self.background_path).convert("RGBA") as background:

                background = background.resize(
                    OUTPUT_RESOLUTION, Image.Resampling.LANCZOS
                )

                img_resized = self._resize_to_fit(img, background)

                composed = self._compose_image(
                    background, img_resized
                )

                output_path.parent.mkdir(parents=True, exist_ok=True)
                composed.convert("RGB").save(output_path)

                logger.info(
                    f"Imagem processada com sucesso: {output_path.name}"
                )

        except Exception as e:
            logger.exception(
                f"Erro ao processar imagem {input_path.name}: {e}"
            )
            raise

    def _resize_to_fit(self, image: Image.Image, background: Image.Image) -> Image.Image:
        """
        Redimensiona a imagem mantendo proporção para caber no fundo.
        """
        img_w, img_h = image.size
        bg_w, bg_h = background.size

        scale = min(bg_w / img_w, bg_h / img_h)
        new_size = (int(img_w * scale), int(img_h * scale))

        logger.debug(
            f"Redimensionando imagem para {new_size}"
        )

        return image.resize(new_size, Image.Resampling.LANCZOS)

    def _compose_image(
        self, background: Image.Image, image: Image.Image
    ) -> Image.Image:
        """
        Centraliza a imagem redimensionada sobre o fundo.
        """
        bg_w, bg_h = background.size
        img_w, img_h = image.size

        offset_x = (bg_w - img_w) // 2
        offset_y = (bg_h - img_h) // 2

        logger.debug(
            f"Centralizando imagem em ({offset_x}, {offset_y})"
        )

        composed = background.copy()
        composed.paste(image, (offset_x, offset_y), image)

        return composed
