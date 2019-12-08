from pico2d import *
from FadeScene import *

import random
import GameFrameWork
import LogoScene

name = "StartScene"
image = None
fadeIn = None
Time = 0.0


def enter():
    global image
    open_canvas(Width, Height, sync = True)  # 가로크기, 세로 크기, 60FPS
    image = load_image('image/start/kpu_credit.png')


def exit():
    global image
    del image
    close_canvas()


def update(frame_time):
    global Time, fadeIn
    Time += frame_time
    if Time > 1.5 :
        if fadeIn == None:
            fadeIn = FadeIn()
    if fadeIn != None:
        if fadeIn.count >= 1:
            GameFrameWork.push_state(LogoScene)
        fadeIn.update()


def draw(frame_time):
    global image, fadeIn
    clear_canvas()
    image.draw(GameFrameWork.Width/2, GameFrameWork.Height/2)
    if fadeIn != None:
        fadeIn.draw()
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            GameFrameWork.quit()


def pause():
    pass


def resume():
    pass