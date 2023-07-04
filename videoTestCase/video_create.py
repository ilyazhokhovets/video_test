import io
import json

import cv2
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np

VIDEO_WIDTH = 100
VIDEO_HEIGHT = 100
VIDEO_FPS = 60
VIDEO_DURATION = 3

BG_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)





def get_font(query_font, query_size):
    print(os.getcwd())
    with open('videoTestCase/fonts.json', 'r') as f:
        settings = json.load(f)
        font = query_font or settings['font']
        size = query_size or settings['size']

    with open(f'videoTestCase/templates/videoTestCase/fonts/{font}.ttf', 'rb') as f:
        file = f.read()
    file = io.BytesIO(file)
    return file, size


def create_video(text: str, query_font: str, query_size:float) -> str:

    font, size = get_font(query_font, query_size)
    text_size = int(VIDEO_HEIGHT*size)
    font = ImageFont.truetype(font, text_size )

    left, top, right, bottom = font.getbbox(text)
    print(text_size, bottom-top)
    text_height = bottom - top
    text_width = right - left
    n_frames = VIDEO_FPS*VIDEO_DURATION

    step_size = (text_width+VIDEO_WIDTH) / n_frames
    video_name = 'test.mp4'
    print(n_frames, text_width, step_size)
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), VIDEO_FPS, (VIDEO_WIDTH, VIDEO_HEIGHT))

    for step in range(n_frames):

        pil_image = Image.new(mode="RGB", size=(VIDEO_WIDTH, VIDEO_HEIGHT), color=BG_COLOR)
        draw = ImageDraw.Draw(pil_image)

        draw.text(text=text,
                  xy=(int(VIDEO_WIDTH - step * step_size), (VIDEO_HEIGHT - text_height) // 2),
                  font=font,
                  fill=TEXT_COLOR)

        open_cv_image = np.array(pil_image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        video.write(open_cv_image)

    cv2.destroyAllWindows()
    video.release()

    return video_name