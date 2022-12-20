import pygame as pg
import random
import sys
import tkinter.messagebox as tkm
import tkinter as tk

#BGMを設定
def alarm():
    pg.mixer.init(frequency = 44100)    # 初期設定
    pg.mixer.music.load("boom.wav")     # 音楽ファイルの読み込み
    pg.mixer.music.play(1)              # 音楽の再生回数(1回)
    while(1):
        a = input("Finish? --->")
        if(a is 'y'): break
    pg.mixer.music.stop()               # 再生の終了
    return 0
    
if __name__ is "__main__":
    alarm()

class Screen:
    def __init__(self, title, wh, img_path):
        pg.display.set_caption(title) 
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(img_path)
        self.bgi_rct = self.bgi_sfc.get_rect() 

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct) 


class Bird:
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    def __init__(self, img_path, ratio, xy):
        self.sfc = pg.image.load(img_path)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, ratio)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        key_dct = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_dct[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]  
            if check_bound(self.rct, scr.rct) != (+1, +1):
                self.rct.centerx -= delta[0]
                self.rct.centery -= delta[1]
        self.blit(scr)                    


class Bomb:
    def __init__(self, color, rad, vxy, scr:Screen):
        self.sfc = pg.Surface((2*rad, 2*rad)) # 正方形の空のSurface
        self.sfc.set_colorkey((0, 0, 0))
        #赤い点から爆弾の画像に変更した
        #爆弾の大きさを拡大した
        self.sfc = pg.image.load("./ex04/fig/bomb.png")
        self.sfc = pg.transform.rotozoom(self.sfc, 0, 0.15)#画像の大きさを調整
        self.sfc.set_colorkey((0, 0, 0))
        #pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)


def check_bound(obj_rct, scr_rct):
    """
    第1引数：こうかとんrectまたは爆弾rect
    第2引数：スクリーンrect
    範囲内：+1／範囲外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


def main():
    clock =pg.time.Clock()

    # 練習１
    #背景画像を変更した
    #背景画像の大きさを変えた
    scr = Screen("逃げろ！こうかとん", (1500,1000), "fig/a.jpg")

    # 練習３
    kkt = Bird("fig/6.png", 2.0, (900,400))
    kkt.update(scr)

    # 練習５
    bkd = Bomb((255, 0, 0), 10, (+1, +1), scr)
    bkd.update(scr)


    # 練習２
    while True:        
        scr.blit()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        kkt.update(scr)
        bkd.update(scr)
        # 爆弾に当たると「もう一度挑戦しよう」「Game Over」というテキストボックスが表示され「OK」ボタンを押すと終了
        if kkt.rct.colliderect(bkd.rct):#爆弾にあたったとき
            root = tk.Tk()
            root.withdraw()
            tkm.showinfo("もう一度挑戦しよう","Game Over")#コメントを表示
            return


        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()