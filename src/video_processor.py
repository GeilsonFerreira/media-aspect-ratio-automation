from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
from pathlib import Path


class VideoProcessor:
    """
    Responsável por processar vídeos verticais (9:16),
    aplicando fundo horizontal (16:9) conforme padrão de TV.
    """

    def __init__(self, background_path: Path, output_resolution=(1280, 720)):
        self.background_path = background_path
        self.output_width, self.output_height = output_resolution

    def is_vertical_9x16(self, video_path: Path) -> bool:
        """Verifica se o vídeo está em proporção 9:16."""
        clip = VideoFileClip(str(video_path))
        width, height = clip.size
        clip.close()

        return height > width and round(height / width, 2) == round(16 / 9, 2)

    def process(self, input_path: Path, output_path: Path) -> None:
        """
        Processa o vídeo aplicando fundo 16:9 e centralizando o conteúdo.
        """
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
            audio_codec="aac"
        )

        clip.close()
