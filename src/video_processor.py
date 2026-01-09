# src/video_processor.py
from pathlib import Path

from moviepy import (
    VideoFileClip,
    ImageClip,
    CompositeVideoClip,
)

from logger import get_logger

log = get_logger(__name__)


class VideoProcessor:
    """
    Converte vídeos de qualquer proporção para 16:9 (MP4),
    aplicando fundo e centralização automática.
    """

    def __init__(
        self,
        background_path: Path,
        output_resolution=(1280, 720),
    ):
        self.background_path = background_path
        self.output_width, self.output_height = output_resolution

        if not self.background_path.exists():
            raise FileNotFoundError(
                f"Imagem de fundo não encontrada: {self.background_path}"
            )

    def process(self, input_path: Path, output_path: Path) -> None:
        log.info(f"Processando vídeo: {input_path.name}")

        clip = None
        final_clip = None

        try:
            clip = VideoFileClip(str(input_path))

            # --- Corrige rotação automaticamente ---
            if clip.rotation:
                clip = clip.rotate(-clip.rotation)

            video_w, video_h = clip.w, clip.h

            # --- Cria fundo 16:9 ---
            background = (
                ImageClip(str(self.background_path))
                .with_duration(clip.duration)
                .resized((self.output_width, self.output_height))
            )

            # --- Redimensiona vídeo mantendo proporção ---
            scale = min(
                self.output_width / video_w,
                self.output_height / video_h,
            )

            resized_video = clip.resized(scale)

            pos_x = (self.output_width - resized_video.w) // 2
            pos_y = (self.output_height - resized_video.h) // 2

            # ✅ MoviePy 2.x
            resized_video = resized_video.with_position((pos_x, pos_y))

            # --- Composição final ---
            final_clip = CompositeVideoClip(
                [background, resized_video],
                size=(self.output_width, self.output_height),
            )

            output_path.parent.mkdir(parents=True, exist_ok=True)

            final_clip.write_videofile(
                str(output_path),
                codec="libx264",
                audio_codec="aac",
                fps=30,
                preset="medium",
                threads=4,
                ffmpeg_params=["-pix_fmt", "yuv420p"],
                temp_audiofile="temp_audio.m4a",
                remove_temp=True,
            )

            log.info(
                f"Vídeo processado com sucesso: {output_path.name}"
            )

        except Exception as e:
            log.exception(
                f"Erro ao processar vídeo {input_path.name}: {e}"
            )
            raise

        finally:
            if final_clip:
                final_clip.close()
            if clip:
                clip.close()
