import random
import GameFrameWork

from pico2d import *
from GameFrameWork import *


class Enemy:
    LEFT_DIR, GO_STRAIGHT, RIGHT_DIR = 0, 1, 2
    SizeX, SizeY = 0, 0
    Attack = 0
    CreateTime = 0
    PIXEL_PER_METER = (10.0 / 22.25)  # 10 pixel 22.25m -> 22.25cm -> 73fit
    Enemy_SPEED_KMPH = 1500.0  # 2마하 -> 약 2000km
    Enemy_SPEED_MPM = (Enemy_SPEED_KMPH * 1000.0 / 60.0)
    Enemy_SPEED_MPS = (Enemy_SPEED_MPM / 60.0)
    Enemy_SPEED_PPS = (Enemy_SPEED_MPS * PIXEL_PER_METER)
    image = None
    Sound = None

    def __init__(self):
        self.x, self.y = random.randint(100, 700), Height
        self.time = 0
        self.Sound = load_wav('sound/EnemyMissile.wav')
        self.Sound.set_volume(64)
        self.distance = 0
        self.state = 0
        self.stateTime = 0

    def get_pos(self):
        self.Sound.play()
        return self.x, self.y - 10

    def get_size(self):
        return self.x - self.SizeX, self.y - self.SizeY, self.x + self.SizeX, self.y + self.SizeY

    def draw_box(self):
        draw_rectangle(*self.get_size ())

    def handle_left(self, frame_time):
        self.x -= self.distance
        self.state = self.LEFT_DIR
        if self.x < 0:
            self.state = self.RIGHT_DIR
            self.x = 0
        if self.stateTime > 10:
            self.state = self.GO_STRAIGHT
            self.stateTime = 0

    def handle_right(self, frame_time):
        self.x += self.distance
        self.state = self.RIGHT_DIR
        if self.x > Width:
            self.state = self.LEFT_DIR
            self.x = Width
        if self.stateTime > 10:
            self.state = self.GO_STRAIGHT
            self.stateTime = 0

    def handle_go_straight(self, frame_time):
        self.state = self.GO_STRAIGHT
        if self.stateTime > 10:
            self.state = random.randint(0, 2)
            self.stateTime = 0

    handle_state = {
        LEFT_DIR: handle_left,
        RIGHT_DIR: handle_right,
        GO_STRAIGHT: handle_go_straight
    }

    def update(self, frame_time):
        self.time += frame_time
        self.distance = Enemy.Enemy_SPEED_PPS * frame_time
        self.y -= self.distance
        if self.y < 0 :
            return True
        else :
            return False

    def draw(self):
        self.image.draw(self.x,self.y)


class NormalEnemy(Enemy):
    SizeX, SizeY = 24, 24

    def __init__(self):
        super().__init__()
        self.image = load_image('image/enemy/Enemy.png')
        self.Hp = 10
        self.score = 10


class MiddleEnemy(Enemy):
    SizeX, SizeY = 22, 32

    def __init__(self):
        super().__init__()
        self.Hp = 15
        self.score = 20
        self.state = random.randint(0, 2)
        MiddleEnemy.image = load_image('image/enemy/MiddleEnemy.png')

    def update(self, frame_time):
        self.stateTime += frame_time * 10
        self.handle_state[self.state](self, frame_time)
        return super().update(frame_time)

    def draw(self):
        self.image.clip_draw(self.state * 44, 0, 44, 64, self.x, self.y)


class HighEnemy(Enemy):
    SizeX, SizeY = 120, 60

    def __init__(self):
        super().__init__()
        self.dir = 0
        self.Hp = 30
        self.score = 40
        HighEnemy.image = load_image('image/enemy/HighEnemy.png')

    def update(self, frame_time):
        self.state = (self.state + 1) % 2
        if self.y > 600:
            super().update(frame_time)
        elif self.dir == 0:
            isdir = random.randint(0, 1)
            if isdir == 1:
                self.dir = -1
            else:
                self.dir = 1
        else:
            if self.x > Width - self.SizeX / 2:
                self.dir = -self.dir
            elif self.x < 0 + self.SizeX / 2:
                self.dir = -self.dir
            self.time += frame_time
            self.x += (self.distance/2 * self.dir)

    def draw(self):
        self.image.clip_draw(self.state * 240, 0, 240, 120, self.x, self.y)

    def get_left_pos(self):
        return self.x - 60, self.y - 10

    def get_right_pos(self):
        return self.x + 60, self.y - 10