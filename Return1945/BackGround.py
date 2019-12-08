import GameFrameWork

from pico2d import *


class BackGround:
    def __init__(self):
        self.image1 = load_image('image/stage/stage1_01.png')
        self.image2 = load_image('image/stage/stage1_02.png')
        self.image3 = load_image('image/stage/stage1_03.png')
        #Sound
        self.bgm = load_music('sound/Stage1.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()
        self.bossBgm = load_music('sound/boss_sound.mp3')
        self.bossBgm.set_volume(64)
        self.width = GameFrameWork.Width
        self.height = 6000

        self.x1, self.y1 = self.width / 2, self.height / 2           # 화면 초기값. stage1_01 초기값.
        self.x2, self.y2 = self.width / 2, self.height / 2 + GameFrameWork.Height     # stage1_02화면 초기값.
        self.x3, self.y3 = self.width / 2, self.height / 2 + GameFrameWork.Height     # stage1_02화면 초기값.
        self.move = 2.5

    def update(self, frame_time):
        if self.y1 > -(self.height / 2):
            self.y1 -= self.move
        if self.y1 < -(self.height / 2) + GameFrameWork.Height:
            self.y2 -= self.move
        if (self.y2 < -(self.height / 2) + GameFrameWork.Height) and (self.y3 > -(self.height / 2) + GameFrameWork.Height):
            self.y3 -= self.move

    def draw(self):
        self.image1.clip_draw(0, 0, self.width, self.height, self.x1, self.y1)
        self.image2.clip_draw(0, 0, self.width, self.height, self.x2, self.y2)
        self.image3.clip_draw(0, 0, self.width, self.height, self.x3, self.y3)