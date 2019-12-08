import GameFrameWork
import FirstStageScene
import LogoScene

from pico2d import *
from GameFrameWork import *
from FirstStageScene import *
from Player import *
from FadeScene import *

name = "GameOverScene"

image = None
CountFont = None
font = None
pause_time = 0.0
TimeCount = 0
ImageCount = 0.0
fadeIn = None
fadeOut = None
BGM = None
IsBGM = False


def enter():
    global image, CountFont, font, TimeCount, fadeIn, fadeOut, BGM, IsBGM, ImageCount
    image = load_image('image/gameover/GameOver.png')
    CountFont = load_font('font/Alien-Encounters-Solid-Bold-Italic.TTF', 300)
    font = load_font('font/Alien-Encounters-Solid-Bold-Italic.TTF', 50)
    BGM = load_music('sound/gameover.mp3')
    BGM.set_volume(64)

    TimeCount =10
    ImageCount = 0.0
    fadeIn = None
    fadeOut = None
    IsBGM = False


def exit():
    global image, CountFont, font, fadeIn, fadeOut, BGM
    del image, CountFont, font, BGM
    if fadeIn != None:
        del fadeIn
    if fadeOut != None:
        del fadeOut


def update(frame_time):
    global TimeCount, fadeIn, fadeOut, ImageCount

    if TimeCount >= 0 :
        TimeCount -= frame_time

    if fadeOut != None :
        fadeOut.update()
        if fadeOut.count >= 1:
            GameFrameWork.pop_state()
            GameFrameWork.change_state(LogoScene)

    if fadeIn != None :
        fadeIn.update()
        if fadeIn.count >= 1:
            GameFrameWork.pop_state()
            GameFrameWork.change_state(FirstStageScene)


def draw(frame_time):
    global image, TimeCount, fadeIn, fadeOut, BGM, IsBGM, ImageCount
    clear_canvas()
    FirstStageScene.draw_stage_scene()
    if TimeCount < 0 :
        if IsBGM == False:
            BGM.repeat_play()
            IsBGM = True
        if ImageCount <= 1:
            ImageCount += 0.001
        image.opacify(ImageCount)
        image.draw(Width/2, Height/2)

    else :
        CountFont.draw(Width / 2 - 150, Height / 2 + 100, "%d" % (TimeCount), (0, 0, 0))
        font.draw(250, 250,"1. Resume     2. Exit", (255, 255, 255))
        font.draw(250, 150, "3. Reset     4. Main", (255, 255, 255))

    if fadeIn != None :
        fadeIn.draw()

    if fadeOut != None :
        fadeOut.draw()
    update_canvas()


def handle_events(frame_time):
    global fadeIn, fadeOut, IsBGM
    events = get_events()
    for event in events:
        if IsBGM and fadeOut == None:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                    fadeOut = FadeOut()
        else:
            if event.type == SDL_QUIT:
                GameFrameWork.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
                FirstStageScene.player.revive()
                GameFrameWork.pop_state()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
                GameFrameWork.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_3):
                if fadeIn == None:
                    fadeIn = FadeIn()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_4):
                if fadeOut == None:
                    fadeOut = FadeOut()


def pause():
    pass


def resume():
    pass
