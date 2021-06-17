from random import randint
from time import sleep
import pyxel


#pyxelのリソースファイルを読み込む
#pyxel.load("mygame_resource.pyxres")
#Map,Cat,Karikari,Bossクラスを作る

shot_list = []
VECT = 1
GAMEMODE = 0

def update_list(list):
    for elem in list:
        elem.update()

class Map:
    GROUND_Y = 100 #地面の座標

class Background:
    pass

class Vec2:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Ringring(Map):
    MOVE_SPEED = 3.0
    JUMP_SPEED = 2.0
    GRAVITY = 0.5
    RELOAD_TIME = 15
    global VECT

    def __init__(self): # blocks, enemys
        self.pos = Vec2(0,self.GROUND_Y -15)
        self.vy = 0
        self.vect = VECT
        self.jump_lim = 0

    def update(self,x,y):
        # ========ringring LR===============
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            self.pos.x -= self.MOVE_SPEED
            if self.vect == 1:
                self.vect  = -1
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self.pos.x += self.MOVE_SPEED
            if self.vect == -1:
                self.vect = 1

        self.vy += self.GRAVITY
        self.pos.y += self.vy

        if self.pos.y > self.GROUND_Y -15:
            self.pos.y = self.GROUND_Y -15

        # ============jump===================
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD_1_UP):
            if self.jump_lim == 0:
                self.vy = -6
                self.jump_lim += 1
            if self.pos.y == self.GROUND_Y -15:
                self.jump_lim = 0

        # ============shot====================
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD_1_A):
            Karikari(self.pos.x,self.pos.y)

    def draw(self):
        pyxel.blt(self.pos.x,self.pos.y,
        0,0,0,16*self.vect,16,6)

class Karikari():
    SHOT_SPEED = 4

    def __init__(self,x,y):
        self.x = x + 2 #*VECT
        self.y = y + 9
        self.alive = True

        shot_list.append(self)
    
    """def update1(self):
        if GAMEMODE == 1:
            if VECT == 1:
                self.x += self.SHOT_SPEED
                if 161 < self.x　< -1:
                    self.alive = False
            elif VECT == -1:
                self.x -= self.SHOT_SPEED
                if self.x < -1:
                    self.alive = False
        elif GAMEMODE == 2:
            self.x += self.SHOT_SPEED
            if self.x < 161:
                self.alive = False"""

    def update(self):
        self.x += self.SHOT_SPEED #* VECT
        if self.x > 161:
            self.alive = False

    def update2(self):
        self.x += self.SHOT_SPEED
        if self.x < 161:
            self.alive = False
    
    def draw(self):
        pyxel.blt(self.x,self.y,0,48,0,5,5,6)

class Cat():
    pass


#"""
class Game(Map):
    GAME_START = 0
    GAME_PROGRESS = 1
    GAME_ORVER = 2

    def __init__(self):
        #global GAMEMODE
        #GAMEMODE = 1
        #画面サイズ、フレームレート（初期値30）を設定
        pyxel.init(160,120,caption="ringring Adventure")
        self.rinrin = Ringring()
        self.scene = self.GAME_START

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
        elif self.scene == self.GAME_ORVER:
            pass

    def first_scene(self):
        self.scene = self.GAME_PROGRESS
        #この中にムービーの描写（draw）もまとめて書こう
    
    def game_progress(self):
        self.rinrin.update(self.rinrin.pos.x,self.rinrin.pos.y)
        update_list(shot_list)
    
    def game_orver(self):
        self.scene = self.GAME_ORVER
    
    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0,self.GROUND_Y,pyxel.width,pyxel.height,11)
        #りんりんを表示させる
        if self.scene == self.GAME_PROGRESS:
            self.draw_progress()
        #カリカリを描写
        for elem in shot_list:
            elem.draw()
    
    def draw_progress(self):
        self.rinrin.draw()

Game()