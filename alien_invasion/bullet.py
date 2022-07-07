import pygame

# Bullet类继承了从模块pygame.sprite 导入的Sprite 类。通过使用精灵（sprite），可将游戏中相关的元素编组，进而同时操作编组中的所有元素。
from pygame.sprite import Sprite


class Bullet(Sprite):
    """管理飞船所发射子弹的类"""

    def __init__(self, ai_game):
        """在飞船当前位置创建一个子弹对象。"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 提供矩形左上角的x坐标和y坐标，以及矩形的宽度和高度。
        # 我们在(0, 0)处创建这个矩形，子弹的宽度和高度是从self.settings中获取的。
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)

        # 将其移到正确的位置，因为子弹的初始位置取决于飞船当前的位置。
        self.rect.midtop = ai_game.ship.rect.midtop

        # 存储用小数表示的子弹位置。
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹。"""

        # 发射出去后，子弹向上移动，意味着其y坐标将不断减小。
        self.y -= self.settings.bullet_speed

        # 更新表示子弹的rect的位置。
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹。"""
        # draw.rect()函数使用存储在self.color中的颜色填充表示子弹的rect占据的屏幕部分
        pygame.draw.rect(self.screen, self.color, self.rect)
