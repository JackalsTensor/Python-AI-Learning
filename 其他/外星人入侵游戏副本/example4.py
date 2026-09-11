import pygame
class Ship:
    def __init__(self,ai_game):
        self.screen = ai_game.screen    #获取游戏的屏幕对象
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()    #获取屏幕的矩形区域
        self.image = pygame.image.load('images副本/ship2.bmp')  #加载外星人图像资源
        self.rect = self.image.get_rect()   #获取外星人图像外接矩形
        self.rect.midbottom=self.screen_rect.midbottom  #设置外星人的初始位置
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
    def update(self):
        if self.moving_right:
            self.x += self.settings.ship_speed
        if self.moving_left:
            self.x -= self.settings.ship_speed
        self.rect.x=self.x
    def blitme(self):
        self.screen.blit(self.image,self.rect)  #把飞船的图像(self.image)，按照self.rect所指定的矩形区域，绘制到游戏屏幕上(self.screen)