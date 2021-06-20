from random import randint
from time import sleep
import pyxel


#pyxelのリソースファイルを読み込む
#pyxel.load("mygame_resource.pyxres")
#Map,Cat,Karikari,Bossクラスを作る

shot_list = []
cat_list = []
block_list = []
GAMEMODE = 0
GAME_WINDOW = 160,120

def update_list(list):
    for elem in list:
        elem.update()

def cleanup_list(list):
    """i = 0
    while i < len(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)
        else:
            i += 1
    """
    for i, _ in enumerate(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)

class Map:
    GROUND_Y = 100 #地面の座標
    GROUND = GROUND_Y


class Background:
    pass

class Vec2:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Ringring(Map):
    MOVE_SPEED = 2.5
    JUMP_SPEED = 2.0
    GRAVITY = 0.5
    #RELOAD_TIME = 15

    def __init__(self): # blocks, enemys
        self.pos = Vec2(0,self.GROUND_Y -15)
        self.vy = 0
        self.vect = 1
        self.jump_lim = 0
        self.shot_lim = 0
        self.LIFE = 3
        self.image = 0

    def update(self,x,y):
        # ============処理を行う前の座標を保持しておく================
        cur = self.pos.x
        # ========ringring LR===============
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            if self.pos.x > -5:
                self.pos.x -= self.MOVE_SPEED
            if self.vect == 1:
                self.vect  = -1
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            if self.pos.x < 155:
                self.pos.x += self.MOVE_SPEED
            if self.vect == -1:
                self.vect = 1
        if cur != self.pos.x:
            self.image = 16
        if cur == self.pos.x:
            self.image = 0

        self.vy += self.GRAVITY
        self.pos.y += self.vy

        #地面に着地させる
        if self.pos.y > self.GROUND_Y -15:
            self.pos.y = self.GROUND_Y -15
        """ブロックに衝突したい
        for _,cat in enumerate(cat_list):
            if not self.pos.x > cat.pos.x + 15 or self.pos.x < cat.pos.x:
                break
            if (self.pos.y) >= cat.pos.y + 15:
                self.pos.y = cat.pos.y"""

        # ============jump===================
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD_1_UP):
            if self.jump_lim == 0:
                self.vy = -6
                self.jump_lim += 1
            """以下の処理を入れてその下のjump_lim　= 0　を消すと2段ジャンプ後硬直が入る
            if self.pos.y == self.GROUND_Y -15:
                self.jump_lim = 0"""
        if self.pos.y == self.GROUND_Y -15:
            self.jump_lim = 0

        # ============shot====================
        if len(shot_list) < 3 and pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD_1_A):
            Karikari(self.pos.x,self.pos.y,self.vect)
            """self.shot_lim = 10
        self.shot_lim -= 1"""

        if pyxel.btnp(pyxel.KEY_C):
            Cat()

    def draw(self):
        pyxel.blt(self.pos.x,self.pos.y,
        0,self.image,0,16*self.vect,16,6)

class Karikari():
    SHOT_SPEED = 4
    SHOT_W = 5
    SHOT_H = 5

    def __init__(self,x,y,v):
        self.pos = Vec2(x + 2,y + 9)
        self.x = x + 2
        self.y = y + 9
        self.v = v
        self.alive = True

        if len(shot_list) < 3:
            shot_list.append(self)

    def update(self):
        self.pos.x += (self.SHOT_SPEED  * self.v)
        if self.pos.x > 161 or self.pos.x <-1:
            self.alive = False
    
    def draw(self):
        pyxel.blt(self.pos.x,self.pos.y,0,48,0,self.SHOT_W,self.SHOT_H,6)

class Cat(Map):
    MOVE_SPEED = 2.5
    CAT_W = 16
    CAT_H = 16
    
    def __init__(self):
        self.pos = Vec2(160,self.GROUND_Y -15)
        self.vy = 0
        self.vect = 1
        self.jump_lim = 0
        self.LIFE = 1
        self.ver = randint(0,3)

        cat_list.append(self)

    def update(self):
        self.pos.x -= self.MOVE_SPEED

    def draw(self):
        pyxel.blt(self.pos.x,self.pos.y,1,self.ver *16,0,self.CAT_W,self.CAT_H,5)

class Boss(Cat):
    def __init__(self):
        pass

#"""
class Game(Map):
    GAME_START = 0
    GAME_PROGRESS = 1
    GAME_OVER = 2

    def __init__(self):
        #global GAMEMODE
        #GAMEMODE = 1
        #画面サイズ、フレームレート（初期値30）を設定
        pyxel.init(160,120,caption="ringring Adventure")
        self.rinrin = Ringring()
        self.life = self.rinrin.LIFE
        self.scene = self.GAME_START
        self.back_cloud =  [((i) * 45, randint(8, 60), i) for i in range(4)]
        self.back_mountain =  [((i) * 45, self.GROUND_Y - 8, i) for i in range(4)]

        #pyxel用のリソースファイルを読み込む
        pyxel.load("mygame_resource.pyxres")
        #runで処理を走らせる
        pyxel.run(self.update,self.draw)

    def update(self):
        #ゲームを終了する
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # ゲームのムービー部分、メイン、ゲームオーバー画面を遷移
        if self.scene == self.GAME_START:
            self.first_scene()
        elif self.scene == self.GAME_PROGRESS:
            self.game_progress()
        elif self.scene == self.GAME_OVER:
            self.game_over()

    def first_scene(self):
        self.scene = self.GAME_PROGRESS
        #この中にムービーの描写（draw）もまとめて書こう
    
    def game_progress(self):
        self.rinrin.update(self.rinrin.pos.x,self.rinrin.pos.y)
        update_list(shot_list)
        update_list(cat_list)
        cleanup_list(shot_list)

        if self.rinrin.pos.x >-5:
            self.rinrin.pos.x -= 1
        
        #敵（Cat）の消滅
        for _,i in enumerate(shot_list):
            for j,k in enumerate(cat_list):
                if ((k.pos.x < i.pos.x)
                    and (i.pos.x < k.pos.x + 15) 
                    and (k.pos.y < i.pos.y) 
                    and (i.pos.y < k.pos.y + 15)):
            # 消滅(敵インスタンス破棄)
                    cat_list.pop(j)
                    break

        #りんりんダメージ
        for j,k in enumerate(cat_list):
            if ((k.pos.x <= self.rinrin.pos.x + 14)
                and (self.rinrin.pos.x <= k.pos.x + 15) 
                and (k.pos.y <= self.rinrin.pos.y + 14) 
                and (self.rinrin.pos.y <= k.pos.y + 15)):
            # ライフ現象
                cat_list.pop(j)
                self.rinrin.LIFE -= 1
                break

        #ゲームオーバー画面
        if self.rinrin.LIFE == 0:
            self.scene = self.GAME_OVER
    
    def game_over(self):
        del shot_list[:]
        del cat_list[:]
    
    def draw(self):
        if self.scene == self.GAME_START:
            self.first_scene()
        elif self.scene == self.GAME_PROGRESS:
            self.draw_game_progress()
        elif self.scene == self.GAME_OVER:
            self.draw_game_over()
    
    def draw_game_progress(self):
        pyxel.cls(12)
        pyxel.rect(0,self.GROUND_Y,pyxel.width,pyxel.height,11)
        pyxel.blt(130,5,0,64,16,15,15,12)

        #ステージを描写
        if self.scene == self.GAME_PROGRESS:
            offset = (pyxel.frame_count // 16) % 160
            for i in range(2): #背景の雲
                for x, y, z in self.back_cloud:
                    pyxel.blt(x + i * 160 - offset, y, 0, 16 * z, 16, 15, 15, 12)
            offset = (pyxel.frame_count // 4) % 160 # // 4
            for i in range(2): #背景の山
                for x, y, z in self.back_mountain:
                    pyxel.blt(x + i * 160 - offset, y, 0, 16 * z, 32, 16, 8, 12)
            offset = pyxel.frame_count % 160
            for i in range(2): #段ボール
                pyxel.blt(i * 160 -offset,self.GROUND_Y - 6, 0, 0, 40, 160, 15, 12)

            #りんりんを描写
            self.rinrin.draw()

        #カリカリを描写
        for elem in shot_list:
            elem.draw()
        #猫を描写
        for elem in cat_list:
            elem.draw()
        #ライフを描写
        for i in range(self.rinrin.LIFE):
            pyxel.blt(1 + 8 * i,1,0,56,0,7,6,6)

    def draw_game_over(self):
        pyxel.rect(0,0,160,120,8)
        pyxel.text(63, 45,"GAME OVER",0)
        pyxel.text(51, 70,"- PRESS ENTER -",0)

Game()