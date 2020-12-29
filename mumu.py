import tkinter as tk
import time
import pygame
import os
import random

img_base_path = os.getcwd() + '/images/'

window = tk.Tk()
#設定視窗物件的標題
window.title('Mumu Game - Start')
#設定視窗物件的大小(長x寬)
window.geometry('640x480')
state = tk.Label(window, font=('Arial',32,'bold'), foreground='#484891')
state.pack(anchor='center')
button_play = tk.Button(window, text=' 開始啟動 Mumu Game',
                       command=window.destroy)
button_play.pack()

img_gif = tk.PhotoImage(file= img_base_path + 'mumu.png')
label_img = tk.Label(window, image=img_gif)
label_img.pack()

state.config(text="\n 1. 黃色起司可增加分數\n 2. 紅色起司有毒會扣分\n 3.負分即遊戲結束")

window.mainloop()

pygame.init()
pygame.mixer.init()  #音效功能初始化

impactSound = pygame.mixer.Sound(os.getcwd() + "/sound/match0.wav")
badSound = pygame.mixer.Sound(os.getcwd() + "/sound/badswap.wav")
failSound = pygame.mixer.Sound(os.getcwd() + "/sound/gameover.ogg")
winSound = pygame.mixer.Sound(os.getcwd() + "/sound/Cheering01.mp3")
#設定音量大小，參值0~1
impactSound.set_volume(0.7)
badSound.set_volume(0.7)
failSound.set_volume(0.7)
winSound.set_volume(0.7)

WIN_WIDTH, WIN_HEIGHT = 640, 480
FRAME_PER_SECONDS = 27  #每秒最大幀數\
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BG = (0, 0, 69)
CHEESE = (255, 255, 125)
RED = (255,   0,   0)

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Mumu Game")

#向右走的圖片陣列
walkRight = [pygame.image.load(img_base_path + 'mumuR1.png'),
             pygame.image.load(img_base_path + 'mumuR2.png')]
             

#向左走的圖片陣列
walkLeft = [pygame.image.load(img_base_path + 'mumuL1.png'),
            pygame.image.load(img_base_path + 'mumuL2.png')]

walkUp = [pygame.image.load(img_base_path + 'mumu.png'),
          pygame.image.load(img_base_path + 'mumu2.png'),
          pygame.image.load(img_base_path + 'mumu3.png')]

walkDown = [pygame.image.load(img_base_path + 'mumu.png'),
            pygame.image.load(img_base_path + 'mumu2.png'),
            pygame.image.load(img_base_path + 'mumu3.png')]


#背景
bg = pygame.image.load(img_base_path + 'cosmic01.png')
# win.fill(WHITE)
#站立時的圖片
char = pygame.image.load(img_base_path + 'mumu.png')

clock = pygame.time.Clock()

class player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        super().__init__()
        self.x, self.y = x, y  #起點
        self.width, self.height = width, height  #寬、高
        self.isJump, self.left, self.right, self.up, self.down = False, False, False, False, False
        self.speed = speed  #速度
        self.t = 10
        self.walkCount = 0
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def redrawGameWindow(self):
        # win.blit(bg, (0, 0))
        # win.fill(WHITE)
    
        if self.walkCount >= FRAME_PER_SECONDS:
            self.walkCount = 0

        if self.left:
            #切換向左走的圖片
            win.blit(walkLeft[self.walkCount % 2], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            #切換向右走的圖片
            win.blit(walkRight[self.walkCount % 2], (self.x, self.y))
            self.walkCount += 1
        elif self.up:
            win.blit(walkUp[self.walkCount % 3], (self.x, self.y))
            self.walkCount += 1
        elif self.down:
            win.blit(walkDown[self.walkCount % 3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(char, (self.x, self.y))

        pygame.display.update()

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= speed
            self.rect.x = self.x
            self.left = True
            self.up = False
            self.down = False
            self.right = False
        elif keys[pygame.K_RIGHT] and self.x < win.get_size()[0] - (width + 37):
            self.x += speed
            self.rect.x = self.x
            self.left = False
            self.up = False
            self.down = False
            self.right = True
        elif keys[pygame.K_UP] and self.y > (0 - 18):
            self.y -= speed
            self.rect.y = self.y
            self.left = False
            self.up = True
            self.down = False
            self.right = False
        elif keys[pygame.K_DOWN] and self.y < win.get_size()[0] - (height + 184):
            self.y += speed
            self.rect.y = self.y
            self.left = False
            self.up = False
            self.down = True
            self.right = False
        else:
            self.left = False
            self.right = False
            self.walkCount = 0

        if not self.isJump:
            if keys[pygame.K_SPACE]:
                self.isJump = True
                self.right = False
                self.left = False
                self.walkCount = 0
        else:
            if self.t >= -10:
                a = 1
                if self.t < 0:
                    a = -1
                self.y -= 0.5 * a * (self.t ** 2)
                self.t -= 1
            else:
                self.isJump = False
                self.t = 10

        self.redrawGameWindow()


class Block(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
 
        self.image = pygame.Surface((width,height))
        self.image.fill((color))
        self.rect = self.image.get_rect()
        self.dx = random.randint(0, 1)
        if self.dx == 0:
            self.dx = random.randint(1, 2)
        else:
            self.dx = random.randint(-2, -1)
        self.dy = -2
        

    def move(self):
        if self.rect.x > 640 or self.rect.x < 0: #到達右邊界 或 左邊界
            self.dx *= -1 #水平速度變號 
        self.rect.x += self.dx


x, y = 270, 200  #起點
width, height = 64, 64  #寬、高
speed = 5  #速度
run = True
mumu = player(x, y, width, height, speed)
score = 0
bad_sprites_list = pygame.sprite.Group()
cheese_sprites_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

for i in range(50):
    block = Block(CHEESE, 10, 5)
 
    block.rect.x = random.randrange(WIN_WIDTH - 37)
    block.rect.y = random.randrange(WIN_HEIGHT - 45)
 
    cheese_sprites_list.add(block)
    all_sprites_list.add(block) 

for i in range(2):
    bad_block = Block(RED, 10, 5)

    bad_block.rect.x = random.randrange(WIN_WIDTH - 37)
    bad_block.rect.y = random.randrange(WIN_HEIGHT - 45)

    bad_sprites_list.add(bad_block)
    all_sprites_list.add(bad_block)

def showScore(score, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect() 
    score_rect.midtop = (70, 50)
    win.blit(score_surface, score_rect)

def showFin(score, color, str):
    Font = pygame.font.SysFont('arial.ttf', 54)
    Surf = Font.render(str, True, RED)
    Rect = Surf.get_rect()
    Rect.midtop = (320, 150)
    win.fill(color)
    win.blit(Surf, Rect)
    showScore(score, RED, 'consolas', 20)

    pygame.display.flip() # 更新視窗
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                time.sleep(1) # 停留一秒
                pygame.quit()

eatenCheese = 0


while run:
    clock.tick(FRAME_PER_SECONDS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    win.fill(BG)
    # win.blit(bg, (0, 0))

    # Draw all the spites
    all_sprites_list.draw(win)
    mumu.move()

    cheese_hit_list = pygame.sprite.spritecollide(mumu, cheese_sprites_list, True)
    black_hit_list = pygame.sprite.spritecollide(mumu, bad_sprites_list, True)

    for i in all_sprites_list:
        i.move()
   
    for i in cheese_hit_list:
        impactSound.play()
        score += 1
        eatenCheese += 1

    for i in black_hit_list:
        badSound.play()
        score -= 50
    
    if score < 0:
        showFin(score, BLACK, "Game Over !")
        failSound.play()
    
    if eatenCheese == 50:
        showFin(score, WHITE, "Congratulations !")
        winSound.play()
 
    showScore(score, WHITE, 'consolas', 20)
    
    pygame.display.update()
    # Go ahead and update the screen with what we've drawn.

pygame.quit()