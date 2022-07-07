import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """显示得分信息的类。"""
    def __init__(self, ai_game):
        """初始化显示得分涉及的属性。"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分信息时使用的字体设置。
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始得分图像。
        self.prep_score()
        self.prep_high_score()

        self.prep_level()

        self.prep_ships()

    def prep_score(self):
        """将得分转换为一幅渲染的图像。"""

        # 函数round() 通常让小数精确到小数点后某一位，其中小数位数是由第二个实参指定的。
        # 然而，如果将第二个实参指定为负数，round() 将舍入到最近的10的整数倍，如10、100、1000等
        rounded_score = round(self.stats.score, -1)

        # 使用一个字符串格式设置指令，让Python将数值转换为字符串时在其中插入逗号。例如，输出为1,000,000 而不是1000000
        score_str = "{:,}".format(rounded_score)

        # 将这个字符串传递给创建图像的render()。为在屏幕上清晰地显示得分，向render() 传递屏幕背景色和文本颜色。
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # 将得分放在屏幕右上角，并在得分增大导致数变宽时让其向左延伸。
        # 为确保得分始终锚定在屏幕右边，创建一个名为score_rect的rect，让其右边缘与屏幕右边缘相距20像素，并让其上边缘与屏幕上边缘也相距20像素
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转换为渲染的图像。"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()

        # 将最高得分放在屏幕顶部中央。
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """检查是否诞生了新的最高得分。"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
        self.prep_high_score()

    def show_score(self):
        """在屏幕上显示得分。"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_level(self):
        """将等级转换为渲染的图像。"""
        # prep_level() 根据存储在stats.level 中的值创建一幅图像
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # 将其right 属性设置为得分的right 属性。然后，将top属性设置为比得分图像的bottom属性大10像素，以便在得分和等级之间留出一定的空间
        self.level_rect = self.level_image.get_rect()

        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还余下多少艘飞船。"""

        # 创建一个空编组self.ships ，用于存储飞船实例
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
