# -*- coding:utf-8 -*-
import pygame as pg
from pygame.locals import *
import sys

#C0A21083効果音機能
pg.mixer.init()
sound_reflect = pg.mixer.Sound("./ex06/反射.ogg")
sound_explosion = pg.mixer.Sound("./ex06/爆発.ogg")
# ボールの動きを計算
def calc_ball(ball_x, ball_y, ball_vx, ball_vy, bar1_x, bar1_y, bar2_x, bar2_y, wall1_x, wall1_y, wall2_x, wall2_y):
        if ball_x <= bar1_x + 10.:  # プレイヤーのバーに当たったら跳ね返る
            if ball_y >= bar1_y - 7.5 and ball_y <= bar1_y + 42.5:
                #C0A21083効果音機能
                sound_reflect.play()
                ball_x = 20.
                ball_vx = -ball_vx
        if ball_x >= bar2_x - 15.:  # COMのバーに当たったら跳ね返る
            if ball_y >= bar2_y - 7.5 and ball_y <= bar2_y + 42.5:
                #C0A21083効果音機能
                sound_reflect.play()
                ball_x = 605.
                ball_vx = -ball_vx
        if ball_x < 5.:  # プレイヤーのバーより後ろなら初期位置にもどる
            ball_x, ball_y = 320., 232.5
        elif ball_x > 620.: # COMのバーより後ろなら初期位置にもどる
            ball_x, ball_y = 307.5, 232.5
        if ball_y <= 10.:# フィールドの上側に当たったら跳ね返る
            ball_vy = -ball_vy
            ball_y = 10.
        elif ball_y >= 457.5: # フィールドの下側に当たったら跳ね返る
            ball_vy = -ball_vy
            ball_y = 457.5
        
        # C0A21055 1の壁に当たったら跳ね返る
        if ball_x >= wall1_x - 10 and ball_x < wall1_x:
            if ball_y >= wall1_y - 7.5 and ball_y <= wall1_y + 92.5:
                #C0A21083効果音機能
                sound_reflect.play()

                ball_x = wall1_x - 10
                ball_vx = -ball_vx
        if ball_x <= wall1_x + 10 and ball_x > wall1_x:
            if ball_y >= wall1_y - 7.5 and ball_y <= wall1_y + 92.5:
                #C0A21083効果音機能
                sound_reflect.play()
                ball_x = wall1_x + 10
                ball_vx = -ball_vx

        # C0A21055 2の壁に当たったら跳ね返る
        if ball_x >= wall2_x - 10 and ball_x < wall2_x:
            if ball_y >= wall2_y - 7.5 and ball_y <= wall2_y + 92.5:
                ball_x = wall2_x - 10
                ball_vx = -ball_vx
        if ball_x <= wall2_x + 10 and ball_x > wall2_x:
            if ball_y >= wall2_y - 7.5 and ball_y <= wall2_y + 92.5:
                ball_x = wall2_x + 10
                ball_vx = -ball_vx

        return ball_x, ball_y, ball_vx, ball_vy

# AIの動きを計算
def calc_ai(ball_x, ball_y, bar2_x, bar2_y):
    dy = ball_y - bar2_y
    if dy > 80: bar2_y += 20
    elif dy > 50: bar2_y += 15
    elif dy > 30: bar2_y += 12
    elif dy > 10: bar2_y += 8
    elif dy < -80: bar2_y -= 20
    elif dy < -50: bar2_y -= 15
    elif dy < -30: bar2_y -= 12
    elif dy < -10: bar2_y -= 8

    if bar2_y >= 420.: bar2_y = 420.
    elif bar2_y <= 10.: bar2_y = 10.
    return bar2_y

# プレイヤーの動き
def calc_player(bar1_y, bar1_dy):
    bar1_y += bar1_dy
    if bar1_y >= 420.: bar1_y = 420.
    elif bar1_y <= 10. : bar1_y = 10.
    return bar1_y

# 得点の計算
def calc_score(ball_x, score1, score2):
    if ball_x < 5.:
        #C0A21083効果音機能
        sound_explosion.play()
    
        score2 += 1
    if ball_x > 620.:
        #C0A21083効果音機能
        sound_explosion.play()
        score1 += 1
    return score1, score2

# イベント処理
def event(bar1_dy):
    for event in pg.event.get():
        if event.type == QUIT:          # 閉じるボタンが押されたら終了
            pg.quit()
            sys.exit()
        if event.type == KEYDOWN:       # キーを押したら
            if event.key == K_UP:
                bar1_dy = -10
            elif event.key == K_DOWN:
                bar1_dy = 10
        elif event.type == KEYUP:       # キーを押し終わったら
            if event.key == K_UP:
                bar1_dy = 0.
            elif event.key == K_DOWN:
                bar1_dy = 0.
    return bar1_dy 

def main():
    # 各パラメータ
    bar1_x, bar1_y = 10. , 215.
    bar2_x, bar2_y = 620., 215.
    ball_x, ball_y = 307.5, 232.5
    wall1_x, wall1_y = 325., 0. # C0A21055 壁一つ目
    wall2_x, wall2_y = 325., 380. # C0A21055 壁二つ目
    bar1_dy, bar2_dy = 0. , 0.
    ball_vx, ball_vy = 250., 250.
    score1, score2 = 0,0
    ball_r = 7
    RUN = True

    # pygameの設定
    pg.init()                                       # Pygameの初期化
    screen = pg.display.set_mode((640,480),0,32)    # 画面の大きさ

    pg.display.set_caption("ピンポンゲーム")                  # 画面タイトル
    clock = pg.time.Clock()
    font = pg.font.SysFont(None,40)                 # 画面文字の設定

    # 背景の設定
    back = pg.Surface((640,480))
    background = back.convert()
    screen.fill((0,0,0))

    # ボールを打つバーの設定
    bar = pg.Surface((10,50))
    bar1 = bar.convert()
    bar1.fill((255,255,255))
    bar2 = bar.convert()
    bar2.fill((255,255,255))

    # C0A21055 跳ね返る壁を設定
    wall_sur = pg.Surface((10, 100))
    wall1 = wall_sur.convert()
    wall2 = wall_sur.convert()
    wall1.fill((255,0,0))
    wall2.fill((255,0,0))

    # ボールの設定
    circ_sur = pg.Surface((20,20))
    pg.draw.circle(circ_sur,(255,255,255),(ball_r, ball_r), ball_r)
    ball = circ_sur
    ball.set_colorkey((0,0,0))

    counter = 0
    timer = 0
    font = pg.font.SysFont(None, 30)
    stop_font = pg.font.SysFont(None, 100)
    score_font = pg.font.SysFont(None, 100)
    while (RUN):
        # 各オブジェクトの描画
        screen.blit(background,(0,0))
        pg.draw.aaline(screen,(255,255,255),(330,5),(330,475))  # 中央線の描画
        pg.draw.ellipse(screen, (255, 255,255), (280, 180, 100, 100), 5) # C0A21143 中央にサークルの描画
        screen.blit(bar1,(bar1_x,bar1_y))                           # プレイヤー側バーの描画
        screen.blit(bar2,(bar2_x,bar2_y))                           # CPU側バーの描画
        screen.blit(ball,(ball_x, ball_y))                          # ボールの描画
        screen.blit(wall1,(wall1_x, wall1_y))                          # 1の壁の描画
        screen.blit(wall2,(wall2_x, wall2_y))                          # 2の壁の描画

        screen.blit(font.render(str(score1), True,(255,255,255)),(250.,10.))
        screen.blit(font.render(str(score2), True,(255,255,255)),(400.,10.))

        # プレイヤー側バーの位置
        bar1_dy = event(bar1_dy)
        bar1_y = calc_player(bar1_y,bar1_dy)

        # ボールの移動
        time_passed = clock.tick(30)
        time_sec = time_passed / 1000.0
        ball_x += ball_vx * time_sec
        ball_y += ball_vy * time_sec

        # C0A21055 時間計測(20秒経ったら終了)
        counter += 1
        if counter % 30 == 0:
            timer += 1
        if timer > 20:
            stop_text = stop_font.render("TIME OVER", True, (0,0,255))
            screen.blit(stop_text, (130, 220))
            pg.display.flip()
            pg.time.wait(2000)
            break
        text = font.render(f"Time: {int(timer)}", True, (255,0,0))
        screen.blit(text, (30, 20))

        # C0A21055 どちらかの得点が2になったら終了
        if score1 == 2:
            score_text = score_font.render("WIN", True, (255,0,0))
            screen.blit(score_text, (250, 220))
            pg.display.flip()
            pg.time.wait(2000)
            return
        elif score2 == 2:
            score_text = score_font.render("LOSE", True, (255,0,0))
            screen.blit(score_text, (230, 220))
            pg.display.flip()
            pg.time.wait(2000)
            return

        # 得点の計算
        score1, score2 = calc_score(ball_x, score1, score2)            

        # CPUのバー速度を計算
        bar2_y = calc_ai(ball_x, ball_y, bar2_x, bar2_y)

        # ボールの速度・位置を計算
        ball_x, ball_y, ball_vx, ball_vy = calc_ball(ball_x, ball_y, ball_vx, ball_vy, bar1_x, bar1_y, bar2_x, bar2_y, wall1_x, wall1_y, wall2_x, wall2_y)
        pg.display.update()                                   # 画面を更新

if __name__ == "__main__":
    main()