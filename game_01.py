from random import randint
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
    for i, _ in enumerate(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)

class Map:
    GROUND_Y = 100 #地面の座標
    GROUND = GROUND_Y

class Vec2:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Block(Map):
    def __init__(self):
        self.pos = Vec2(150,self.GROUND_Y -14)
        self.LIFE = 10

        block_list.append(self)
    
    def update(self):
        self.pos.x -= 1
        if self.pos.x <-1:
            self.alive = False
    
    def draw(self):
        pyxel.blt(self.pos.x,self.pos.y,0,32,0,16,16,6)

class Ringring(Map):
    MOVE_SPEED = 2.5
    JUMP_SPEED = 2.0
    GRAVITY = 0.5
    #RELOAD_TIME = 15

    def __init__(self): # blocks, enemys
        self.pos = Vec2(0,self.GROUND_Y -15)
        self.bx = 1
        self.vy = 0
        self.vect = 1
        self.jump_lim = 0
        self.shot_lim = 0 #3
        self.LIFE = 3
        self.image = 0

    def update(self,x,y):
        if self.pos.x >-5:
            self.pos.x -= self.bx

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

        # ============jump===================
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD_1_UP):
            if self.jump_lim == 0:
                pyxel.play(3, 4)
                self.vy = -6
                self.jump_lim += 1
            """以下の処理を入れてその下のjump_lim　= 0　を消すと2段ジャンプ後硬直が入る
            if self.pos.y == self.GROUND_Y -15:
                self.jump_lim = 0"""
        if self.pos.y == self.GROUND_Y -15:
            self.jump_lim = 0

        # ============shot====================
        if len(shot_list) < 3 and pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD_1_A):
            pyxel.play(3,5)
            Karikari(self.pos.x,self.pos.y,self.vect)
            """self.shot_lim = 10
        self.shot_lim -= 1"""

    def draw(self):
        pyxel.blt(self.pos.x,self.pos.y,
        0,self.image,0,16*self.vect,16,6)

class Karikari():
    SHOT_SPEED = 4
    SHOT_W = 5
    SHOT_H = 5

    def __init__(self,x,y,v):
        self.pos = Vec2(x + 5,y + 9)
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
    MOVE_SPEED = 1.5
    CAT_W = 16
    CAT_H = 16
    
    def __init__(self):
        self.pos = Vec2(160,self.GROUND_Y -15)
        self.vy = 0
        self.vect = 1
        self.jump_lim = 0
        self.LIFE = 2

        cat_list.append(self)

    def update(self):
        self.pos.x -= self.MOVE_SPEED
        if self.pos.x <-1:
            self.alive = False

    def draw(self):
        pyxel.blt(self.pos.x,self.pos.y,1,0,0,self.CAT_W,self.CAT_H,5)

class Boss(Cat):
    MOVE_SPEED = 2.0
    def __init__(self):
        self.pos = Vec2(160,self.GROUND_Y -31)
        self.vect = 1
        self.LIFE = 16

        cat_list.append(self)
        
        #cat_list.pop(self)

    def update(self):
        self.pos.x -= (self.MOVE_SPEED * self.vect)
        if self.pos.x < -1:
            self.vect = -1
        if self.pos.x > 150:
            self.vect = 1
    
    def draw(self):
        pyxel.blt(self.pos.x,self.pos.y,1,2,16,(30 * self.vect),32,5)

#"""
class Game(Map):
    GAME_START = 1
    GAME_PROGRESS = 2
    GAME_OVER = 3
    GAME_BOSS = 4
    PAUSE = 0
    BOSS_alive = 0

    def __init__(self):
        #global GAMEMODE
        #GAMEMODE = 1
        #画面サイズ、フレームレート（初期値30）を設定
        pyxel.init(160,120,caption="ringring Adventure",fps=30,quit_key=pyxel.KEY_ESCAPE)
        self.rinrin = Ringring()
        self.life = self.rinrin.LIFE
        self.scene = self.GAME_START
        self.back_cloud =  [((i) * 45, randint(8, 60), i) for i in range(4)]
        self.back_mountain =  [((i) * 45, self.GROUND_Y - 8, i) for i in range(4)]
        self.framecount = 0
        self.brake_cat = []
        self.play_music = True
        self.game_clear = False
        self.now_scene = 0
        self.menu = 0
        
        #pyxel用のリソースファイルを読み込む
        pyxel.load("mygame_resource.pyxres")

        pyxel.playm(0,loop=True)
        #runで処理を走らせる
        pyxel.run(self.update,self.draw)

    def update(self):
        #ゲームを終了する
        if pyxel.btnr(pyxel.KEY_Q) or pyxel.btnr(pyxel.GAMEPAD_1_SELECT):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD_1_START):
            if self.scene == self.PAUSE:
                self.scene = self.now_scene
            else:
                self.now_scene = self.scene
                self.menu = 0
                self.scene = self.PAUSE

        # ゲームのムービー部分、メイン、ゲームオーバー画面を遷移
        if self.scene == self.GAME_START:
            self.first_scene()
        elif self.scene == self.PAUSE:
            self.pause()
        elif self.scene == self.GAME_PROGRESS:
            self.game_progress()
        elif self.scene == self.GAME_BOSS:
            self.boss_stage()
        elif self.scene == self.GAME_OVER:
            self.game_over()
    
    def pause(self):
        if pyxel.btnp(pyxel.KEY_B) or pyxel.btnp(pyxel.GAMEPAD_1_LEFT):
            self.menu -= 1
        if pyxel.btnp(pyxel.KEY_N) or pyxel.btnp(pyxel.GAMEPAD_1_RIGHT):
            self.menu += 1
        pyxel.rect(10,10,140,100,7)
        if self.menu == 0:
            pyxel.rect(10,10,140,100,7)
            pyxel.text(70,11,"PAUSE",0)
            pyxel.text(20,20,"[MENU]",0)
            pyxel.text(20,30,"UP KEY : JUMP",0)
            pyxel.text(20,40,"LEFT KEY : MOVE LEFT",0)
            pyxel.text(20,50,"RIGFT KEY : MOVE RIGHT",0)
            pyxel.text(20,60,"SPACE KEY : RINGRING SHOT",0)
            pyxel.text(20,70,"[Z] KEY: RETURN PAUSE",0)
            pyxel.text(20,99,"[B] BACK             [N] NEXT",0)
        if self.menu == 1:
            pyxel.rect(10,10,140,100,7)
            pyxel.text(70,11,"PAUSE",0)
            pyxel.blt(20,30,2,0,0,126,55,7)
            pyxel.text(20,99,"[B] BACK             [N] NEXT",0)
        if self.menu == 2:
            pyxel.rect(10,10,140,100,7)
            pyxel.text(70,11,"PAUSE",0)
            pyxel.blt(20,30,2,0,56,126,38,7)
            pyxel.text(20,99,"[B] BACK             [N] NEXT",0)

        if self.menu == 3:
            pyxel.text(20,99,"[B] BACK             [N] NEXT",0)
        
        if self.menu ==4:
            pyxel.rect(10,10,140,100,7)
            pyxel.blt(20,30,2,0,104,126,38,7)
            pyxel.text(20,99,"[B] BACK             [N] NEXT",0)
        
        if self.menu <= -1 or self.menu >= 5:
            self.menu = 0

    def first_scene(self):
        del shot_list[:]
        del cat_list[:]
        del block_list[:]
        del self.brake_cat[:]

        self.BOSS_alive = 0
        self.game_clear = False
        if pyxel.btnp(pyxel.KEY_ENTER):
            if self.play_music == False:
                pyxel.stop()
                pyxel.playm(0, loop=True)
                self.play_music = True
            self.framecount = pyxel.frame_count /30
            self.scene = self.GAME_PROGRESS

    def move_scene(self):
        #中にムービーの描写（draw）もまとめて書こう
        pass
    
    def game_progress(self):
        self.rinrin.update(self.rinrin.pos.x,self.rinrin.pos.y)
        update_list(shot_list)
        update_list(cat_list)
        update_list(block_list)
        cleanup_list(shot_list)

        if pyxel.frame_count % randint(60,80) == 0:
            Block()

        if pyxel.frame_count % randint(20,65) == 0:
            Cat()
        
        # パンダブロックにぶつかったshotを消滅
        for i2,i in enumerate(shot_list):
            for _,k in enumerate(block_list):
                if ((k.pos.x < i.pos.x)
                    and (i.pos.x < k.pos.x + 15)
                    and (k.pos.y < i.pos.y)
                    and (i.pos.y < k.pos.y + 15)):
            # 敵にダメージ
                    k.LIFE -= 1
                    shot_list.pop(i2)
                    break
        for j,k in enumerate(block_list):
            # LIFEが０のパンダブロックを消滅させる
            if k.LIFE == 0:
                block_list.pop(j)

        #敵（Cat）の消滅
        for i2,i in enumerate(shot_list):
            for _,k in enumerate(cat_list):
                if ((k.pos.x < i.pos.x)
                    and (i.pos.x < k.pos.x + 15) 
                    and (k.pos.y < i.pos.y) 
                    and (i.pos.y < k.pos.y + 15)):
            # 敵にダメージ
                    k.LIFE -= 1
                    shot_list.pop(i2)
                    break
        for j,k in enumerate(cat_list):
            # LIFEが０の敵を消滅させる
            if k.LIFE == 0:
                self.brake_cat.append(cat_list.pop(j))

        #りんりんダメージ
        for j,k in enumerate(cat_list):
            if ((k.pos.x <= self.rinrin.pos.x + 14)
                and (self.rinrin.pos.x <= k.pos.x + 15) 
                and (k.pos.y <= self.rinrin.pos.y + 14) 
                and (self.rinrin.pos.y <= k.pos.y + 15)):
            # ライフ減少
                cat_list.pop(j)
                self.rinrin.LIFE -= 1
                break
        
        if len(self.brake_cat) == 32:
            #del shot_list[:]
            #del cat_list[:]
            self.scene = self.GAME_BOSS

        #ゲームオーバー画面
        if self.rinrin.LIFE == 0:
            self.scene = self.GAME_OVER
        
    def boss_stage(self):
        if self.BOSS_alive == 0:
            self.boss = Boss()
            self.BOSS_alive = 1
        boss_life = self.boss.LIFE

        if pyxel.frame_count % randint(35,60) == 0:
            Cat()

        self.rinrin.update(self.rinrin.pos.x,self.rinrin.pos.y)
        update_list(shot_list)
        update_list(cat_list)
        update_list(block_list)
        cleanup_list(shot_list)

        # パンダブロックにぶつかったshotを消滅
        for i2,i in enumerate(shot_list):
            for j,k in enumerate(block_list):
                if ((k.pos.x < i.pos.x)
                    and (i.pos.x < k.pos.x + 15)
                    and (k.pos.y < i.pos.y)
                    and (i.pos.y < k.pos.y + 15)):
            # パンダとショットを消滅
                    k.LIFE -= 1
                    shot_list.pop(i2)
                    block_list.pop(j)
                    break
        
        #敵（Cat）の消滅
        for i2,i in enumerate(shot_list):
            for _,k in enumerate(cat_list):
                if ((k.pos.x < i.pos.x)
                    and (i.pos.x < k.pos.x + 23) 
                    and (k.pos.y < i.pos.y) 
                    and (i.pos.y < k.pos.y + 31)):
            # 敵にダメージ
                    k.LIFE -= 1
                    shot_list.pop(i2)
                    break
        for j,k in enumerate(cat_list):
            # LIFEが０の敵を消滅させる
            if k.LIFE == 0:
                cat_list.pop(j)
        if self.boss.LIFE != boss_life:
            if len(block_list):
                self.brake_cat.pop()
                self.brake_cat.pop()

        #りんりんダメージ
        for j,k in enumerate(cat_list):
            if ((k.pos.x <= self.rinrin.pos.x + 14)
                and (self.rinrin.pos.x <= k.pos.x + 15) 
                and (k.pos.y <= self.rinrin.pos.y + 14) 
                and (self.rinrin.pos.y <= k.pos.y + 30)):
            # ライフ減少
                if cat_list[j] != self.boss:
                    cat_list.pop(j)
                self.rinrin.LIFE -= 1
                break

        if self.boss.LIFE == 0:
            self.game_clear = True
            self.scene = self.GAME_OVER
        
        #ゲームオーバー画面
        if self.rinrin.LIFE == 0:
            self.scene = self.GAME_OVER
    
    def game_over(self):
        self.rinrin.LIFE,self.rinrin.pos.x = 3,0
        if pyxel.btn(pyxel.KEY_ENTER) or pyxel.btn(pyxel.GAMEPAD_1_START):
            self.scene = self.GAME_START
    
    def draw(self):
        if self.scene == self.GAME_START:
            self.draw_first_scene()
        elif self.scene == self.GAME_PROGRESS or self.scene == self.GAME_BOSS:
            self.draw_game_progress()
        elif self.scene == self.GAME_OVER:
            self.draw_game_over()

    def draw_first_scene(self):
        #この中にムービーの描写（draw）もまとめて書こう
        pyxel.cls(0)
        pyxel.text(45, 45,"ringring Adventure",14)
        pyxel.text(51, 70,"- PRESS ENTER -",14)
        pyxel.text(51, 80,"PRESS [z] PAUSE",14)
        pyxel.text(51, 90,"PRESS [q] EXIT!",14)

    def draw_game_progress(self):
        pyxel.cls(12)
        pyxel.rect(0,self.GROUND_Y,pyxel.width,pyxel.height,11)
        pyxel.blt(130,5,0,64,16,15,15,12)

        #ステージを描写
        offset = (pyxel.frame_count // 16) % 160
        for i in range(2): #背景の雲
            for x, y, z in self.back_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 16 * z, 16, 15, 15, 12)
        offset = (pyxel.frame_count // 4) % 160 # // 4
        for i in range(2): #背景の山
            for x, y, z in self.back_mountain:
                pyxel.blt(x + i * 160 - offset, y, 0, 16 * z, 32, 16, 8, 12)
        offset = pyxel.frame_count % 160
        for i in range(2):
            pyxel.blt(i * 160 - offset, 99, 0, 0, 45, 160, 3, 12)

        #ブロックパンダを配置
        for elem in block_list:
            elem.draw()
        #カリカリを描写
        for elem in shot_list:
            elem.draw()
        #熊猫を描写
        for elem in cat_list:
            elem.draw()
        """if self.BOSS_alive == 1:
            self.boss.draw()"""
        
        #ボスのライフメーター（出現カウントダウン）を表示
        pyxel.rect(40,5,84,8,10)
        gauge = len(self.brake_cat)
        pyxel.rect(42,6,2.5*gauge,6,3)

        #りんりんを描写
        self.rinrin.draw()

        #ライフを描写
        for i in range(self.rinrin.LIFE):
            pyxel.blt(5 + 10 * i,5,0,56,0,7,6,6)

    def draw_game_over(self):
        if self.game_clear:
            pyxel.rect(40,5,84,8,10)
            pyxel.rect(20,20,120,80,10)
            pyxel.text(58,45,"GAME CLEAR!!",0)
        else:
            self.play_music = False
            pyxel.stop()
            pyxel.play(3,6, loop=True)
            pyxel.rect(0,0,160,120,8)
            pyxel.text(63, 45,"GAME OVER",0)
        pyxel.text(51, 70,"- PRESS ENTER -",0)

Game()