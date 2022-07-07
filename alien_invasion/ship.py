import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """管理飞船的类"""
    # __init__() 接受两个参数：引用self 和指向当前AlienInvasion 实例的引用。

    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置。"""

        super().__init__()

        # 将屏幕赋给了Ship的一个属性，以便在这个类的所有方法中轻松访问
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 使用方法get_rect()访问屏幕的属性rect，并将其赋给了self.screen_rect，从而获取到屏幕的位置
        self.screen_rect = ai_game.screen.get_rect()

        # 调用pygame.image.load() 加载图像该函数返回一个表示飞船的surface, 而我们将这个surface赋给了self.image
        self.image = pygame.image.load('images/ship.bmp')

        # 加载图像后，使用get_rect()获取相应surface的属性rect，以便后面能够使用它来指定飞船的位置。
        # 之后的代码中self.rect代表的就是飞船的位置
        self.rect = self.image.get_rect()

        # 可设置相应rect对象的属性center 、centerx 或centery ；
        # 要让游戏元素与屏幕边缘对齐，可使用属性top 、bottom 、left 或right 。
        # 除此之外，还有一些组合属性，如midbottom 、midtop 、midleft 和midright
        # 将self.rect.midbottom设置为表示屏幕的矩形的属性midbottom，这些rect属性设置飞船位置，使其与屏幕下边缘对齐并水平居中。
        self.rect.midbottom = self.screen_rect.midbottom

        # 前面的代码将飞船放置在底部中心，此处获取的self.rect.x即此时的底部中心位置的横坐标
        # 鉴于调整飞船的位置时，将增减一个单位为像素的小数值，因此需要将位置赋给一个能够存储小数值的变量。
        # 可使用小数来设置rect的属性，但rect将只存储这个值的整数部分。为准确存储飞船的位置，定义一个可存储小数值的新属性self.x
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根据移动标志调整飞船的位置"""

        # 更新飞船而不是rect对象的x值。
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # 根据self.x更新rect对象，即更新飞船的位置。
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_ship(self):
        """在指定位置绘制飞船。"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕底端居中。"""
        # 让飞船在屏幕底端居中后，重置用于跟踪飞船确切位置的属性self.x 。
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
