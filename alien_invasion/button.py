import pygame.font


class Button:
    def __init__(self, ai_game, msg):
        """初始化按钮的属性。msg 是要在按钮中显示的文本"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮的尺寸和其他属性。
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)

        # 实参None让Pygame使用默认字体，而48指定了文本的字号。
        self.font = pygame.font.SysFont(None, 48)

        # 为让按钮在屏幕上居中，创建一个表示按钮的rect对象并将其center属性设置为屏幕的center 属性。
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Pygame处理文本的方式是，将要显示的字符串渲染为图像。调用_prep_msg() 来处理这样的渲染。
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上居中。_prep_msg()接受实参self以及要渲染为图像的文本"""

        # 调用font.render() 将存储在msg中的文本转换为图像，再将该图像存储在self.msg_image中
        # 方法font.render() 还接受一个布尔实参，该实参指定开启还是关闭反锯齿功能（反锯齿让文本的边缘更平滑）。
        # 余下的两个实参分别是文本颜色和背景色。我们启用了反锯齿功能，并将文本的背景色设置为按钮的颜色。
        # 如果没有指定背景色，Pygame渲染文本时将使用透明背景。
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)

        # 让文本图像在按钮上居中：根据文本图像创建一个rect ，并将其center属性设置为按钮的center 属性
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 调用screen.fill() 来绘制表示按钮的矩形
        # 调用screen.blit() 并向它传递一幅图像以及与该图像相关联的rect ，从而在屏幕上绘制文本图像
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

