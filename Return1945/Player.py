import random
import GameFrameWork

from pico2d import *
from GameFrameWork import *
from PlayerUI import *
from Explosion import *

REVIVAL = 1


class Player:
    SIZE = 80
    EXPLOSION_SIZE =128
    SIZE_HALF_X = 25
    SIZE_HALF_Y = 30
    PIXEL_PER_METER = (10.0 / 22.25)          # 10 pixel 22.25m -> 22.25cm -> 73fit
    FLY_SPEED_KMPH = 2500.0                   # 2마하 -> 약 2500km
    FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
    FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
    FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

    STAND, BACK, FORWARD, LEFT, RIGHT = 0, 1, 2, 3, 4

    image = None

    MissileTime = 0.0
    BombTime = 0.0
    PowerTime = 0.0
    StageTime = 0.0
    Score = 0
    isClear = False

    def __init__(self):
        self.HP = 180
        self.respawn = REVIVAL
        self.frame = 0
        self.state = self.STAND
        self.x, self.y = Width/2, 90
        self.xDir, self.yDir = 0, 0
        self.boomCount = 0 # 필살기 횟수
        self.Explosion = None
        self.isMissileOn = False
        self.isAlive = True        #  player 폭발이 끝나고 죽으면 false
        self.upgradeMissile = False    # True = Laser False = 기본
        Player.image = load_image('image/player/player.png')

        # UI
        self.hpBarUI = PlayerHpBar()
        self.hpGaugeUI = PlayerHpGauge()
        self.boomUI = BoomUI()
        self.scoreUI = ScoreUI()

    def update(self, frame_time):
        if self.respawn >= REVIVAL:
            self.respawn = REVIVAL
        else:
            self.respawn += 0.005

        self.create_time(frame_time)
        self.scoreUI.update(frame_time)

        if self.HP > 0 :
            distance = Player.FLY_SPEED_PPS * frame_time
            if self.state in (self.STAND, self.FORWARD, self.BACK):
                self.frame = (self.frame + 1) % 3
            elif self.state in (self.LEFT, self.RIGHT):
                if self.frame >= 2:
                    self.frame = 2
                else:
                    self.frame += 1
            self.x += (self.xDir * distance)
            self.y += (self.yDir * distance)

            self.x = clamp(self.SIZE_HALF_X, self.x, Width - self.SIZE_HALF_X)
            self.y = clamp(self.SIZE_HALF_Y, self.y, Height - self.SIZE_HALF_Y)
        else:
            if self.Explosion == None:
                self.Explosion = PlayerExplosion(self.x, self.y)
                self.Explosion.Sound.play()
            else:
                self.Explosion.update(frame_time)

    def draw(self):
        if self.HP > 0:
            self.image.opacify(self.respawn)
            self.image.clip_draw(self.frame * Player.SIZE, self.state * Player.SIZE
                                 , Player.SIZE, Player.SIZE, self.x, self.y)
        elif self.Explosion != None:
            if self.Explosion.frame < 6 :
                self.Explosion.draw()
            else:
                self.isAlive = False
        self.hpBarUI.draw()
        self.hpGaugeUI.draw(self.HP)
        self.boomUI.draw(self.boomCount)
        self.scoreUI.draw()

    def handle_event(self, event):
        # 위
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state in (self.STAND, self.LEFT, self.RIGHT):
                self.state = self.FORWARD
                self.yDir = 1

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            if self.state in (self.FORWARD,):
                self.state = self.STAND
                self.frame = 0
                self.xDir = 0
                self.yDir = 0

        # 아래
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state in (self.STAND, self.FORWARD, self.LEFT, self.RIGHT):
                self.state = self.BACK
                self.yDir = -1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.state in (self.BACK,):
                self.state = self.STAND
                self.frame = 0
                self.xDir = 0
                self.yDir = 0
        # 왼쪽
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.FORWARD, self.BACK, self.STAND, self.RIGHT):
                self.state = self.LEFT
                self.xDir = -1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT, ):
                self.state = self.STAND
                self.frame = 0
                self.xDir = 0
                self.yDir = 0

        # 오른쪽
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.FORWARD, self.BACK, self.STAND, self.LEFT):
                self.state = self.RIGHT
                self.xDir = 1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT,):
                self.state = self.STAND
                self.frame = 0
                self.xDir = 0
                self.yDir = 0

    def get_pos(self):
        return self.x, self.y

    def get_size(self):
        return self.x - self.SIZE_HALF_X, self.y - self.SIZE_HALF_Y, self.x + self.SIZE_HALF_X, \
               self.y + self.SIZE_HALF_Y

    def draw_box(self):
        draw_rectangle(*self.get_size())

    def revive(self):
        self.__init__()
        self.scoreUI.Time = self.StageTime
        self.respawn = 0.1

    def create_time(self, frame_time):
        self.MissileTime += frame_time
        self.BombTime += frame_time
        self.PowerTime += frame_time
        self.StageTime = self.scoreUI.Time
        self.scoreUI.score = self.Score