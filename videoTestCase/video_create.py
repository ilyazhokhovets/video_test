
import cv2

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np

VIDEO_WIDTH = 100
VIDEO_HEIGHT = 100
VIDEO_FPS = 24
TEXT_SIZE_RATIO = 0.4
VIDEO_DURATION = 3
FONT = 'Arial'
BG_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)


def create_video(text: str = 'Hello World') -> str:
    text_size = int(VIDEO_HEIGHT*TEXT_SIZE_RATIO)

    font = ImageFont.truetype(f"{FONT}.ttf", text_size)
    left, top, right, bottom = font.getbbox(text)
    text_height = bottom - top
    text_width = right - left
    n_frames = VIDEO_FPS*VIDEO_DURATION

    step_size = int(round((text_width+VIDEO_WIDTH) / n_frames, 0))
    video_name = 'test.mp4'

    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), VIDEO_FPS, (VIDEO_WIDTH, VIDEO_HEIGHT))

    for step in range(n_frames):

        pil_image = Image.new(mode="RGB", size=(VIDEO_WIDTH, VIDEO_HEIGHT), color=BG_COLOR)
        draw = ImageDraw.Draw(pil_image)

        draw.text(text=text,
                  xy=(VIDEO_WIDTH - step * step_size, (VIDEO_HEIGHT - text_height) // 2),
                  font=font,
                  fill=TEXT_COLOR)

        open_cv_image = np.array(pil_image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        video.write(open_cv_image)

    cv2.destroyAllWindows()
    video.release()

    return video_name