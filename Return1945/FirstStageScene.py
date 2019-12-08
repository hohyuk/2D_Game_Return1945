import GameFrameWork
import LogoScene
import PauseScene
import GameOverScene
import GameClearScene
from pico2d import *

from BackGround import *
from Player import *
from Missile import *
from Item import *
from Enemy import *
from Explosion import *
from Bomb import *
from Boss import *
name = "FirstStageScene"

background = None
player = None
boss = None

# List
ItemList = []
EnemyList = []
ExplosionList = []
BombList = []
PlayerMissileList = []
EnemyMissileList = []


def init_object():
    global background, player, boss
    background = BackGround()
    player = Player()
    boss = None
    NormalEnemy.CreateTime = 0
    MiddleEnemy.CreateTime = 0
    HighEnemy.CreateTime = 0
    Boss.CreateTime = 0
    Boss.Create = False


def init_list():
    global ItemList, EnemyList, ExplosionList, BombList,PlayerMissileList, EnemyMissileList
    ItemList = []
    EnemyList = []
    ExplosionList = []
    BombList = []
    PlayerMissileList = []
    EnemyMissileList = []


def enter():
    GameFrameWork.reset_time()
    init_object()
    init_list()


def exit():
    global background, player, boss
    global ItemList, EnemyList, ExplosionList, BombList,PlayerMissileList, EnemyMissileList
    del background, player
    del ItemList, EnemyList, ExplosionList, BombList,PlayerMissileList, EnemyMissileList
    if boss != None:
        del boss


def update(frame_time):
    global player, boss
    if player.isAlive:
        live_player(frame_time)
    else:
        GameFrameWork.push_state(GameOverScene)


def live_player(frame_time):
    global background, player, boss
    background.update(frame_time)
    player.update(frame_time)
    create_item(frame_time)
    if player.isClear:
        for enemies in EnemyList:
            if type(enemies) == type(HighEnemy()):
                explosion = BigExplosion(enemies.x, enemies.y)
            else:
                explosion = EnemyExplosion(enemies.x, enemies.y)
            player.Score += enemies.score
            explosion.Sound.play()
            ExplosionList.append(explosion)
            EnemyList.remove(enemies)
        for missiles in EnemyMissileList:
            explosion = EnemyExplosion(missiles.x, missiles.y)
            explosion.Sound.play()
            ExplosionList.append(explosion)
            EnemyMissileList.remove(missiles)
        if boss.isDie:
            GameFrameWork.push_state(GameClearScene)
    else:
        create_enemy(frame_time)

    if player.isMissileOn and player.MissileTime > 0.2:
        missile = None
        if player.upgradeMissile:
            for i in range(3) :
                missile = PlayerLaserMissile(player.x, player.y, i)
                PlayerMissileList.append(missile)
        else:
            missile = PlayerMissile(*player.get_pos())
            PlayerMissileList.append(missile)
        missile.Sound.play()
        player.MissileTime = 0

    for enemies in EnemyList:
        isDel = enemies.update(frame_time)
        if isDel:
            EnemyList.remove(enemies)
        else:
            if enemies.time > 1:
                if type(enemies) == type(HighEnemy()):
                    enemyMissile1 = MagicMissile(*enemies.get_left_pos())
                    enemyMissile2 = MagicMissile(*enemies.get_right_pos())
                    EnemyMissileList.append(enemyMissile1)
                    EnemyMissileList.append(enemyMissile2)
                else:
                    enemyMissile = EnemyMissile(*enemies.get_pos())
                    EnemyMissileList.append(enemyMissile)
                enemies.time = 0

    for explosions in ExplosionList:
        isDel = explosions.update(frame_time)
        if isDel:
            ExplosionList.remove(explosions)

    if Boss.Create and boss != None:
        boss.update(frame_time)
        if boss.specialAttack and boss.attackTime > 1.5:
            for i in range(12):
                bossmissile = RotateMissile(boss.x, boss.y, i)
                EnemyMissileList.append(bossmissile)
            boss.attackTime = 0
        elif (not boss.specialAttack) and boss.attackTime > 0.5:
            boss_missile1 = MagicMissile(*boss.get_left_pos())
            boss_missile2 = MagicMissile(*boss.get_right_pos())
            EnemyMissileList.append(boss_missile1)
            EnemyMissileList.append(boss_missile2)
            boss.attackTime = 0

    for missiles in PlayerMissileList:
        isDel = missiles.update(frame_time)
        if isDel:
            PlayerMissileList.remove(missiles)
        else:
            if Boss.Create and boss != None:
                if collision(missiles, boss):
                    boss.Hp -= missiles.Attack
                    explosion = EnemyExplosion(missiles.x, missiles.y)
                    explosion.Sound.play()
                    ExplosionList.append(explosion)
                    PlayerMissileList.remove(missiles)
                    if boss.Hp <= 0 :
                        player.Score += boss.score
                        player.isClear = True
                    break
            for enemies in EnemyList:
                if collision(missiles, enemies):
                    enemies.Hp -= missiles.Attack
                    if enemies.Hp <= 0:
                        if type(enemies) == type(HighEnemy()):
                            explosion = BigExplosion(enemies.x, enemies.y)
                        else:
                            explosion = EnemyExplosion(enemies.x, enemies.y)
                        player.Score += enemies.score
                        explosion.Sound.play()
                        ExplosionList.append(explosion)
                        EnemyList.remove(enemies)
                    PlayerMissileList.remove(missiles)
                    break  # break 이유 겹처서 오는 적과 미사일 충돌 판단.





    for missiles in EnemyMissileList:
        isDel = missiles.update(frame_time)
        if isDel:
            EnemyMissileList.remove(missiles)
        elif collision(missiles, player):
            if player.respawn == REVIVAL:
                player.HP -= missiles.Attack
                EnemyMissileList.remove(missiles)

    for items in ItemList:
        isDel = items.update(frame_time)
        if isDel:
            ItemList.remove(items)
        else:
            if collision(items, player):
                if type(items) == type(BombItem()) and player.boomCount < 5:
                    player.boomCount += 1
                elif type(items) == type(PowerItem()):
                    player.upgradeMissile = not player.upgradeMissile
                items.Sound.play()
                ItemList.remove(items)
                break

    for bombs in BombList:
        isDel = bombs.update(frame_time)
        if isDel:
            BombList.remove(bombs)
        else:
            if Boss.Create and boss != None and not bombs.bossCollision:
                if collision(bombs, boss):
                    boss.Hp -= bombs.Attack
                    bombs.bossCollision = True
            for enemies in EnemyList:
                if collision(bombs, enemies):
                    if type(enemies) == type(HighEnemy()):
                        explosion = BigExplosion(enemies.x, enemies.y)
                    else:
                        explosion = EnemyExplosion(enemies.x, enemies.y)
                    player.Score += enemies.score
                    explosion.Sound.play()
                    ExplosionList.append(explosion)
                    EnemyList.remove(enemies)
                    break
            for missiles in EnemyMissileList:
                if collision(bombs, missiles):
                    explosion = EnemyExplosion(missiles.x, missiles.y)
                    explosion.Sound.play()
                    ExplosionList.append(explosion)
                    EnemyMissileList.remove(missiles)
                    break


def draw_stage_scene():
    global background, player, boss
    global PlayerMissileList, EnemyMissileList, ItemList, EnemyList, ExplosionList, BombList
    background.draw()

    for missiles in EnemyMissileList:
        missiles.draw()
        #missiles.draw_box()

    for missiles in PlayerMissileList:
        missiles.draw()
        #missiles.draw_box()

    for items in ItemList:
        items.draw()
        #items.draw_box()

    for enemies in EnemyList:
        enemies.draw()
        #enemies.draw_box()

    for bombs in BombList:
        bombs.draw()
        #bombs.draw_box()

    if Boss.Create and boss != None:
        boss.draw()

    for explosions in ExplosionList:
        explosions.draw()

    player.draw()
    # player.draw_box()


def draw(frame_time):
    clear_canvas()
    draw_stage_scene()
    update_canvas()


def handle_events(frame_time):
    global player, BombList
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            GameFrameWork.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            GameFrameWork.push_state(PauseScene)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            if player.Explosion == None:
                player.isMissileOn = True
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_SPACE):
            player.isMissileOn = False
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            if player.boomCount > 0 and player.BombTime > 1.5:
                bomb = BombAirplane()
                BombList.append(bomb)
                player.boomCount -= 1
                player.BombTime = 0.0
        else:
            player.handle_event(event)


def pause():
    pass


def resume():
    pass


def collision(a, b):
    left_a, bottom_a, right_a, top_a = a.get_size()
    left_b, bottom_b, right_b, top_b = b.get_size()

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True


def create_item(frame_time):
    global player
    if player.BombTime > 10:
        item = BombItem()
        ItemList.append(item)
        player.BombTime = 0

    if player.PowerTime > 20:
        item = PowerItem()
        ItemList.append(item)
        player.PowerTime = 0


def create_enemy(frame_time):
    global player, boss, background
    NormalEnemy.CreateTime += frame_time
    MiddleEnemy.CreateTime += frame_time
    HighEnemy.CreateTime += frame_time

    if player.StageTime >= 30:
        count = 3
    elif player.StageTime >= 10:
        count = 2
    else:
        count = 1

    if NormalEnemy.CreateTime >= 2.0:
        for i in range(count):
            enemy = NormalEnemy()
            EnemyList.append(enemy)
        NormalEnemy.CreateTime = 0.0
    if player.StageTime > 20 :
        if MiddleEnemy.CreateTime >= 5.0:
            for i in range(count - 1):
                enemy = MiddleEnemy()
                EnemyList.append(enemy)
            MiddleEnemy.CreateTime = 0.0
    if player.StageTime > 50:
        if HighEnemy.CreateTime >= 5.0:
            enemy = HighEnemy()
            EnemyList.append(enemy)
            HighEnemy.CreateTime = 0.0

    # boss create
    if Boss.Create and boss == None:
        background.bossBgm.repeat_play()
        boss = Boss()
    elif Boss.CreateTime >= 110:
        Boss.Create = True
    else:
        Boss.CreateTime += frame_time
