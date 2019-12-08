import GameFrameWork
import FirstStageScene
import LogoScene
from pico2d import *
from FadeScene import *

name = "PauseScene"
image = None
font = None
pause_count = 0.0
value = 0.01
fadeOut = None


def enter():
    global image, font, fadeOut
    image = load_image('image/pause/pause01.png')
    font = load_font('font/Alien-Encounters-Solid-Bold-Italic.TTF', 50)
    fadeOut = None


def exit():
    global image, font, fadeOut
    del image
    del font
    del fadeOut


def update(frame_time):
    global pause_count, value, fadeOut
    if pause_count > 1:
        value = -value
    elif pause_count < 0:
        value = -value
    pause_count += value
    if fadeOut != None :
        fadeOut.update()
        if fadeOut.count >= 1:
            GameFrameWork.pop_state()
            GameFrameWork.change_state(LogoScene)


def draw(frame_time):
    global image, fadeOut
    clear_canvas()
    FirstStageScene.draw_stage_scene()
    image.opacify(pause_count)
    image.draw(Width/2,Height/2 + 100)
    font.draw(50, 250, "Esc : Resume     Q : Exit     W : Main", (0, 255, 0))
    if fadeOut != None :
        fadeOut.draw()
    update_canvas()


def handle_events(frame_time):
    global fadeOut
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            GameFrameWork.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_q):
            GameFrameWork.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_w):
            if fadeOut == None:
                fadeOut = FadeOut()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            GameFrameWork.pop_state()


def pause():
    pass


def resume():
    pass

