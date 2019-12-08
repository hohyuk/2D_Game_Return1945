import GameFrameWork

from pico2d import *
from GameFrameWork import *

name = "Fade"


class FadeIn:
    def __init__(self):
        self.image = load_image('image/fade/Fade01.png')
        self.count = 0.0

    def update(self):
        self.count += 0.02

    def draw(self):
        self.image.opacify(self.count)
        self.image.draw(Width/2, Height/2)


class FadeOut:
    def __init__(self):
        self.image = load_image('image/fade/Fade02.png')
        self.count = 0.0

    def update(self):
        self.count += 0.02

    def draw(self):
        self.image.opacify(self.count)
        self.image.draw(Width / 2, Height / 2)