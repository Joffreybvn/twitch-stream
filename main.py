
from os import environ
import subprocess as sp
import numpy as np
import cv2


TWITCH_STREAM_KEY = environ.get('TWITCH_STREAM_KEY')

frame_width = 1920
frame_height = 1080
FPS = 30

# Load image
img = cv2.imread('assets/images/001.jpg')
# resized = cv2.resize(img, (frame_width, frame_height))


def get_slided_frame(image: np.array) -> np.array:
    index = 0
    height, width, _ = image.shape

    while True:
        index += 1

        x = 0 + index % (width - frame_width)
        y = 700
        x_max = x + frame_width
        y_max = y + frame_height

        yield image[y: y_max, x: x_max]


CBR = '3000k'
command = [
    'ffmpeg',
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-s', str(frame_width)+'x'+str(frame_height),
    '-pix_fmt', 'bgr24',
    '-r', str(FPS),
    '-i', '-',
    '-stream_loop', '-1',
    '-i', 'assets/music/001.mp3',
    '-f', 'flv',
    '-vcodec', 'libx264',
    '-profile:v', 'main',
    '-g', '60',
    '-keyint_min', '30',
    '-b:v', CBR,
    '-minrate', CBR,
    '-maxrate', CBR,
    '-pix_fmt', 'yuv420p',
    '-preset', 'ultrafast',
    '-tune', 'zerolatency',
    '-threads', '0',
    '-bufsize', CBR,
    f'rtmp://ams03.contribute.live-video.net/app/{TWITCH_STREAM_KEY}']

proc = sp.Popen(command, stdin=sp.PIPE, stderr=sp.STDOUT, bufsize=0)

for frame in get_slided_frame(img):
    proc.stdin.write(frame.tostring())


proc.stdin.close()
proc.wait()
