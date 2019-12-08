import GameFrameWork
import FirstStageScene
import LogoScene
from pico2d import *
from FadeScene import *

name = "GameClearScene"
image = None
font = None
ImageCount = 0.0
SizeX, SizeY = 1024, 606
BGM = None
fadeOut = None


def enter():
    global image, font, fadeOut, BGM, ImageCount
    image = load_image('image/finish/GameClear.png')
    font = load_font('font/Alien-Encounters-Solid-Bold-Italic.TTF', 50)
    BGM = load_music('sound/gameover.mp3')
    BGM.set_volume(64)
    BGM.repeat_play()
    ImageCount = 0.0
    fadeOut = None


def exit():
    global image, font, BGM
    del image, font, BGM


def update(frame_time):
    global fadeOut, ImageCount

    if fadeOut != None :
        fadeOut.update()
        if fadeOut.count >= 1:
            GameFrameWork.pop_state()
            GameFrameWork.change_state(LogoScene)

    if ImageCount <= 1:
        ImageCount += 0.01


def draw(frame_time):
    global image,font, SizeX, SizeY, ImageCount
    clear_canvas()
    FirstStageScene.draw_stage_scene()
    image.opacify(ImageCount)
    image.clip_draw_to_origin(0, 0, SizeX, SizeY, 0, 200, SizeX, SizeY)
    font.draw(300, 250,"1. Main     2. Exit",(0, 0, 0))
    if fadeOut != None :
        fadeOut.draw()
    update_canvas()


def handle_events(frame_time):
    global fadeOut
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            GameFrameWork.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
            if fadeOut == None:
                fadeOut = FadeOut()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
            GameFrameWork.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            GameFrameWork.pop_state()


def pause():
    pass


def resume():
    pass
