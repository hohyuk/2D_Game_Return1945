import random
import GameFrameWork

from pico2d import *
from GameFrameWork import *
from Explosion import BossExplosion


class Boss:
    SizeX = 400
    SizeY = 309

    Create = False
    CreateTime = 0.0
    PIXEL_PER_METER = (10.0 / 22.25)  # 10 pixel 22.25m -> 22.25cm -> 73fit
    SPEED_KMPH = 1500.0  # 2마하 -> 약 2000km
    SPEED_MPM = (SPEED_KMPH * 1000.0 / 60.0)
    SPEED_MPS = (SPEED_MPM / 60.0)
    SPEED_PPS = (SPEED_MPS * PIXEL_PER_METER)
    image = None
    weakImage = None
    gauge = None
    STOP_DIR, LEFT_DIR, RIGHT_DIR = 0, 1, 2

    def __init__(self):
        self.x, self.y = Width/2, Height
        self.Hp = 500
        self.score = 200
        self.attackTime = 0.0
        self.stateTime = 0
        self.moveTime = 0
        self.state =0
        self.dir = 0
        self.distance = 0
        self.specialAttack = False
        self.Explosion = None
        self.isDie = False
        Boss.image = load_image('image/boss/Boss01.png')
        Boss.weakImage = load_image('image/boss/Boss02.png')
        Boss.gauge = load_image('image/boss/hp.png')

    def handle_stop(self):
        self.specialAttack = True
        if self.moveTime > 3:
            self.specialAttack = False
            self.dir = random.randint(1, 2)
            self.moveTime = 0

    def handle_left(self):
        self.x -= self.distance
        if self.x < 0 + self.SizeX / 2:
            self.state = self.RIGHT_DIR
            self.x = 0 + self.SizeX / 2
        if self.moveTime > 3:
            self.dir = self.STOP_DIR
            self.moveTime = 0

    def handle_right(self):
        self.x += self.distance
        if self.x > 800 - self.SizeX / 2:
            self.dir = self.LEFT_DIR
            self.x = 800 - self.SizeX / 2
        if self.moveTime > 3:
            self.dir = self.STOP_DIR
            self.moveTime = 0

    handle_state = {
        STOP_DIR: handle_stop,
        LEFT_DIR: handle_left,
        RIGHT_DIR: handle_right
    }

    def update(self, frame_time):
        if self.Hp > 0:
            self.attackTime += frame_time
            self.stateTime += frame_time
            self.moveTime += frame_time
            self.distance = Boss.SPEED_PPS * frame_time
            if self.y > Height - 200:
                self.y -= self.distance
            else:
                self.handle_state[self.dir](self)

            if self.stateTime > 0.5:
                self.state = (self.state + 1) % 4
                self.stateTime = 0
        else:
            if self.Explosion == None:
                self.Explosion = BossExplosion(self.x, self.y)
            else:
                self.Explosion.update(frame_time)

    def draw(self):
        self.gauge.clip_draw_to_origin(0, 0, 100, 30, self.x - 250, self.y + 150, self.Hp, 10)
        if self.Hp > 100 :
            self.image.clip_draw(self.state * self.SizeX, 0
                                 , self.SizeX, self.SizeY, self.x, self.y)
        elif self.Hp > 0:
            self.weakImage.clip_draw(self.state * self.SizeX, 0
                                     , self.SizeX, self.SizeY, self.x, self.y)
        elif self.Explosion != None:
            if self.Explosion.state < 4:
                self.Explosion.draw()
            else:
                self.isDie = True

    def draw_box(self):
        draw_rectangle(*self.get_size())

    def get_size(self):
        return self.x - self.SizeX / 4, self.y - self.SizeY / 2, self.x + self.SizeX / 4, self.y + self.SizeY / 2

    def get_left_pos(self):
        return self.x - 80, self.y - 30

    def get_right_pos(self):
        return self.x + 80, self.y - 30