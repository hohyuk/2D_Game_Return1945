import GameFrameWork

from pico2d import *


class Explosion:
    image = None
    Size = 0

    def __init__(self, x, y):
        self.Sound = load_wav('sound/explosion.wav')
        self.Sound.set_volume(90)
        self.x, self.y = x, y
        self.frame = 0
        self.time = 0

    def update(self, frame_time, speed, count):
        self.time += frame_time * speed
        if self.frame < count:
            if self.time > 1:
                self.frame = (self.frame + 1) % (count + 1)
                self.time = 0
        if self.frame == count:
            return True
        else:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * self.Size, 0, self.Size, self.Size, self.x, self.y)


class PlayerExplosion(Explosion):
    Size = 128

    def __init__(self, x, y):
        super().__init__(x, y)
        PlayerExplosion.image = load_image('image/explosion/explosion1.png')

    def update(self, frame_time):
        super().update(frame_time, 10, 6)


class EnemyExplosion(Explosion):
    Size = 71

    def __init__(self, x, y):
        super().__init__(x, y)
        EnemyExplosion.image = load_image('image/explosion/explosion2.png')

    def update(self, frame_time):
        return super().update(frame_time, 30, 11)


class BigExplosion(Explosion):
    Size = 160

    def __init__(self, x, y):
        super().__init__(x, y)
        self.state = 0
        BigExplosion.image = load_image('image/explosion/explosion3.png')

    def update(self, frame_time):
        self.time += frame_time * 30

        if self.time > 1:
            if self.frame >= 3:
                self.state += 1
            self.frame = (self.frame + 1) % 4
            self.time = 0

        if self.state == 4:
            return True
        else:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * BigExplosion.Size, self.state * BigExplosion.Size
                             , BigExplosion.Size, BigExplosion.Size, self.x, self.y)


class BossExplosion(Explosion):
    Size = 320

    def __init__(self, x, y):
        super().__init__(x, y)
        self.state = 0
        BossExplosion.image = load_image('image/explosion/explosion4.png')

    def update(self,frame_time):
        self.time += frame_time * 3

        if self.time > 0.3:
            if self.frame >= 3:
                self.state += 1
            self.frame = (self.frame + 1) % 4
            self.time = 0

        if self.state == 4:
            return True
        else:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * BossExplosion.Size, self.state * BossExplosion.Size
                             , BossExplosion.Size, BossExplosion.Size, self.x, self.y)