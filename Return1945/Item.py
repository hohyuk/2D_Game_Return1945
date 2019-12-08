import GameFrameWork
import random

from pico2d import *
from GameFrameWork import *


class Item:
    LEFT_DIR, RIGHT_DIR = 0, 1
    SizeX = 54
    SizeY = 35
    speed = 100
    Sound = None
    image = None

    def __init__(self):
        Item.Sound = load_wav('sound/Item.wav')
        Item.Sound.set_volume(64)
        self.x, self.y = random.randint(50, 750), Height
        self.frame = 0
        self.anim_time = 0
        self.dir = random.randint(0, 1)
        self.dirTime = 0

    def handle_left(self, frame_time):
        self.dirTime += frame_time
        self.x -= self.speed * frame_time
        self.dir = self.LEFT_DIR
        if self.x < (self.SizeX / 2):
            self.dir = self.RIGHT_DIR
            self.x = (self.SizeX / 2)
        if self.dirTime > 5:
            self.dir = self.RIGHT_DIR
            self.dirTime = 0

    def handle_right(self, frame_time):
        self.dirTime += frame_time
        self.x += self.speed * frame_time
        self.dir = self.RIGHT_DIR
        if self.x > Width - (self.SizeX / 2):
            self.dir = self.LEFT_DIR
            self.x = Width - (self.SizeX / 2)
        if self.dirTime > 5:
            self.dir = self.LEFT_DIR
            self.dirTime = 0

    def update(self, frame_time):
        self.anim_time += frame_time
        self.handle_dir[self.dir](self, frame_time)
        self.y -= self.speed * frame_time

        if self.y < 0:
            return True
        else:
            return False

    def draw_box(self):
        draw_rectangle(*self.get_size())

    handle_dir = {
        LEFT_DIR: handle_left,
        RIGHT_DIR: handle_right,
    }


class PowerItem(Item):

    def __init__(self):
        super().__init__()  # super() -> 부모 클래스를 부른다.
        PowerItem.image = load_image('image/item/Item_Power.png')

    def update(self, frame_time):
        if self.anim_time > 0.1:
            self.frame = (self.frame + 1) % 6
            self.anim_time = 0

        return super().update(frame_time)

    def draw(self):
        self.image.clip_draw(self.frame * PowerItem.SizeX, 0, PowerItem.SizeX, 35, self.x, self.y)

    def get_size(self):
        return self.x - (PowerItem.SizeX / 2), self.y - (PowerItem.SizeY / 2), self.x + (PowerItem.SizeX / 2), \
               self.y + (PowerItem.SizeY / 2)


class BombItem(Item):

    def __init__(self):
        super().__init__()      # super() -> 부모 클래스를 부른다.
        BombItem.image = load_image('image/item/Item_Bomb.png')

    def update(self, frame_time):
        if self.anim_time > 0.1:
            self.frame = (self.frame + 1) % 4
            self.anim_time = 0

        return super().update(frame_time)

    def draw(self):
        self.image.clip_draw(self.frame * BombItem.SizeX, 0
                             , BombItem.SizeX, BombItem.SizeY, self.x, self.y)

    def get_size(self):
        return self.x - (BombItem.SizeX / 2), self.y - (BombItem.SizeY / 2), self.x + (BombItem.SizeX / 2), self.y + \
               (BombItem.SizeY / 2)
