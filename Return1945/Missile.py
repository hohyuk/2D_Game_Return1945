import math

from pico2d import *
from GameFrameWork import *


class Missile:
    SizeX, SizeY = 0, 0
    Dir = 0
    Attack = 0
    PIXEL_PER_METER = (10.0 / 1.5)  # 10 pixel 1.5m
    MISSILE_SPEED_KMPH = 500.0  # 약 500km
    MISSILE_SPEED_MPM = (MISSILE_SPEED_KMPH * 1000.0 / 60.0)
    MISSILE_SPEED_MPS = (MISSILE_SPEED_MPM / 60.0)
    MISSILE_SPEED_PPS = (MISSILE_SPEED_MPS * PIXEL_PER_METER)
    image = None
    Sound = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.Sound = load_wav('sound/Missile.wav')
        self.Sound.set_volume(90)
        self.distance = 0

    def update(self, frame_time, height):
        self.distance = Missile.MISSILE_SPEED_PPS * frame_time
        if height > 0:
            self.y += self.distance
            if self.y > Height:
                return True
            else:
                return False
        else:
            self.y -= self.distance
            if self.y < 0:
                return True
            else:
                return False

    def draw_box(self):
        draw_rectangle(*self.get_size())

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_pos(self):
        return self.x, self.y

    def get_size(self):
        return self.x - (self.SizeX / 2), self.y - (self.SizeY / 2), self.x + (self.SizeX / 2), self.y + (self.SizeY / 2)


class PlayerMissile(Missile):
    SizeX = 20
    SizeY = 30

    def __init__(self, x, y):
        super().__init__(x, y)
        self.Attack = 10
        PlayerMissile.image = load_image('image/missile/Missile.png')

    def update(self, frame_time):
        return super().update(frame_time, Height)


class PlayerLaserMissile(Missile):
    SizeX = 15
    SizeY = 30
    STRAIGHT_MISSILE, LEFT_MISSILE, RIGHT_MISSILE = 0, 1, 2

    def __init__(self, x, y, dir):
        super().__init__(x, y)
        self.Dir = dir
        self.Attack = 15
        PlayerLaserMissile.image = load_image('image/missile/Special_Bullet.png')

    def update(self, frame_time):
        if self.Dir == PlayerLaserMissile.LEFT_MISSILE:
            self.x -= self.distance
        elif self.Dir == PlayerLaserMissile.RIGHT_MISSILE:
            self.x += self.distance

        return super().update(frame_time, Height)

    def draw(self):
        self.image.clip_draw(40 * self.Dir, 0, 40, 48, self.x, self.y)


class EnemyMissile(Missile):
    SizeX, SizeY = 10, 10

    def __init__(self, x, y):
        super().__init__(x, y)
        self.Attack = 10
        EnemyMissile.image = load_image('image/missile/Missile_Enemy01.png')

    def update(self, frame_time):
        return super().update(frame_time, 0)


class MagicMissile(Missile):
    SizeX, SizeY = 38, 38

    def __init__(self, x, y):
        super().__init__(x, y)
        self.state = 0
        self.Attack = 20
        MagicMissile.image = load_image('image/missile/Magic_Missile.png')

    def update(self, frame_time):
        self.state = (self.state + 1) % 3
        return super().update(frame_time, 0)

    def draw(self):
        self.image.clip_draw(self.state * self.SizeX, 0, self.SizeX, self.SizeY, self.x, self.y)


class RotateMissile(EnemyMissile):
    SizeX, SizeY = 10, 10

    def __init__(self, x, y, rad):
        super().__init__(x, y)
        self.posX, self.posY = x, y
        self.rad = rad * 30

    def update(self, frame_time):
        self.distance = (Missile.MISSILE_SPEED_PPS * frame_time) / 5

        self.x = self.x + math.cos(self.rad * math.pi / 180) * self.distance
        self.y = self.y + math.sin(self.rad * math.pi / 180) * self.distance

        # 두점 사이의 거리 공식을 이용
        Distance = math.sqrt(((self.posX - self.x) * (self.posX - self.x)) + (self.posY - self.y) * (self.posY - self.y))

        if Distance > Height:
            return True
        else:
            return False
