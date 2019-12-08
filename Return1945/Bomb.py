import random
import GameFrameWork
from pico2d import *
from GameFrameWork import *

class BombAirplane:
    PIXEL_PER_METER = (40.0 / 22.25)  # 40 pixel 22.25m -> 22.25cm -> 73fit
    FLY_SPEED_KMPH = 500.0  # 2마하 -> 약 2400km
    FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
    FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
    FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

    image = None
    bombSound = None

    def __init__(self):
        self.x, self.y = Width/2, -150
        self.Attack = 100
        self.bossCollision = False
        BombAirplane.image = load_image('image/bomb_airplan/Bomb_Airplan.png')

        if BombAirplane.bombSound == None:
            BombAirplane.bombSound = load_wav('sound/Bomb.wav')
            BombAirplane.bombSound.set_volume(64)

    def update(self, frame_time):
        BombAirplane.bombSound.play()
        distance = BombAirplane.FLY_SPEED_PPS * frame_time
        self.y += distance

        if self.y > Height:
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x,self.y)

    def get_size(self):
        return self.x - Width/2, self.y -150, self.x + Width/2, self.y + 150

    def draw_box(self):
        draw_rectangle(*self.get_size ())
