#pygame基础模板
#（1）初始化环节：pygame初始化，游戏设置下载，屏幕与窗口，时钟对象
#（2）游戏主循环环节：事件循环，画面更新，帧率控制
#（3）启动逻辑：“if __name__=='__main__'”
import sys  #实现游戏关闭的功能
import pygame  #导入pygame库
from example2 import Settings
from example4 import Ship

class AlienInvasion:  #核心载体游戏
    def __init__(self):  #初始化
        pygame.init()  #初始化pygame所有模块
        self.settings = Settings()  #创建一个实例
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))  #创建显示窗口
        self.clock = pygame.time.Clock()  # 创建一个时钟
        pygame.display.set_caption('Alien Invasion')  #游戏窗口标题(游戏标题)
        self.ship = Ship(self)

    def run_game(self):
        while True:  #开始游戏主循环
            for event in pygame.event.get():  #侦听键盘和鼠标事件
                if event.type == pygame.QUIT:  #如果用户点开了窗口的“关闭按钮”
                    sys.exit()  #退出游戏
            pygame.display.flip()  #更新整个游戏屏幕
            self.clock.tick(60)  #创建游戏帧率
            self.screen.fill(self.settings.bg_color)  #创建游戏背景颜色
            self.ship.blitme()


if __name__ == '__main__':  #创建游戏实例并进行游戏，把新的画面显示出来
    ai = AlienInvasion()  #创建实例
    ai.run_game()  #启动游戏主循环

#注释：
#（1）pygame.init():即pygame initialize(初始化)，可表示为pygame的初始化开关
#（2）pygame.display.set_mode()：display是“显示”模块，set_mode是“设置模式”→“设置游戏窗口的显示模式（尺寸）”。
#（3）pygame.display.set_caption()：caption是“标题”→“给游戏窗口设置标题
#（4）pygame.event.get()：event是“事件”，get是“获取”→“获取用户的所有操作事件（点击、按键等）
#（5）if __name__=='__main__'用法：自己跑就干活，被别人借就安静当零件，不添乱。
# (6) pygame.init() 必须在所有 Pygame 功能调用前,先初始化屏幕 self.screen，再初始化飞船 self.ship
# (7)先 self.screen.fill(背景)，再 self.ship.blitme(飞船),所有绘制完成后执行 pygame.display.flip()
# (8)先处理事件（event.get()），再更新画面、控制帧率（clock.tick）
# (9)先加载所有资源（如飞船图像），再启动游戏主循环（run_game）