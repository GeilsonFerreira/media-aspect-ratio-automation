# src/video_processor.py
import os
from pathlib import Path

from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
from logger import get_logger

log = get_logger(__name__)


class VideoProcessor:
    """
    Processa vídeos e adapta para 16:9 com fundo.
    """

    def __init__(self, background_path: Path, output_resolution=(1280, 720)):
        self.background_path = background_path
        self.output_width, self.output_height = output_resolution

        if not self.background_path.exists():
            raise FileNotFoundError(
                f"Imagem de fundo não encontrada: {self.background_path}"
            )

    def is_16x9(self, file_path: Path) -> bool:
        clip = VideoFileClip(str(file_path))
        w, h = clip.w, clip.h
        clip.close()

        return abs((w / h) - (16 / 9)) < 0.02


    def process(self, input_path: Path, output_path: Path) -> None:
        clip = VideoFileClip(str(input_path))

        background = (
            ImageClip(str(self.background_path))
            .with_duration(clip.duration)
            .resized((self.output_width, self.output_height))
        )

        resized_video = clip.resized(height=self.output_height)

        pos_x = (self.output_width - resized_video.w) // 2
        resized_video = resized_video.with_position((pos_x, 0))

        final_clip = CompositeVideoClip([background, resized_video])

        output_path.parent.mkdir(parents=True, exist_ok=True)

        final_clip.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp_audio.m4a",
            remove_temp=True,
            threads=4
        )

        final_clip.close()
        clip.close()

        log.info(
            f"Vídeo processado com sucesso: {os.path.basename(input_path)}"
        )
