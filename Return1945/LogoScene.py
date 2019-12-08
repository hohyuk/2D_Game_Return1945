import GameFrameWork
import FirstStageScene

from pico2d import *
from GameFrameWork import *
from FadeScene import *



name = "LogoScene"

logo = None
flicker = None
fadeOut = None


class Logo:
    def __init__(self):
        self.image = load_image('image/logo/logo.png')
        # Sound
        self.bgm = load_music('sound/ophelia.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()

    def draw(self):
        self.image.draw(Width/2, Height/2)


class Flicker:
    def __init__(self):
        self.image = load_image('image/logo/start_key.png')
        self.flash_count = 0        # 버튼 깜박임.
        self.time = 0.0
        self.isShow = True

    def update(self, frame_time):
        self.time += frame_time
        if self.time > 2.0:
            self.isShow = True
            self.time = 0.0
        elif self.time > 1.0:
            self.isShow = False

    def draw(self):
        self.image.draw(Width/2, 100)


def enter():
    global logo, flicker, fadeOut
    logo = Logo()
    flicker = Flicker()
    fadeOut = None


def exit():
    global logo, flicker, fadeOut
    del logo
    del flicker
    del fadeOut


def update(frame_time):
    global fadeOut
    flicker.update(frame_time)
    if fadeOut != None :
        fadeOut.update()
        if fadeOut.count >= 1:
            GameFrameWork.change_state(FirstStageScene)


def draw(frame_time):
    global fadeOut
    clear_canvas()
    logo.draw()
    if flicker.isShow:
        flicker.draw()

    if fadeOut != None :
        fadeOut.draw()
    update_canvas()


def handle_events(frame_time):
    global fadeOut
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            GameFrameWork.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                GameFrameWork.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):         # enter key
                if fadeOut == None:
                    fadeOut = FadeOut()


def pause():
    pass


def resume():
    pass

