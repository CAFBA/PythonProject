import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship

from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """管理游戏资源与行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        # 调用函数pygame.init() 来初始化背景设置，让Pygame能够正确地工作
        pygame.init()
        # 创建一个Settings 实例并将其赋给self.settings
        self.settings = Settings()

        # 调用pygame.display.set_mode() 来创建一个显示窗口，实参是一个元组，指定了游戏窗口的尺寸
        # 赋给属性self.screen的对象是一个surface 在Pygame中，surface是屏幕的一部分，用于显示游戏元素。
        # 传入了尺寸(0, 0)以及参数pygame.FULLSCREEN 这让Pygame生成一个覆盖整个显示器的屏幕。
        # 由于无法预先知道屏幕的宽度和高度，要在创建屏幕后更新这些设置：使用屏幕的rect的属性width和height来更新对象settings
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((1200, 800))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        # 创建一个用于存储游戏统计信息的实例。
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # 调用Ship()时，必须提供一个参数：一个AlienInvasion实例。
        # 在这里，self 指向的是当前AlienInvasion实例
        # 这个参数让Ship能够访问游戏资源，如对象screen 我们将这个Ship实例赋给了self.ship
        self.ship = Ship(self)

        # 在AlienInvasion中创建一个编组（group），用于存储所有有效的子弹，以便管理发射出去的所有子弹。
        # 这个编组是pygame.sprite.Group类的一个实例。
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # 创建外星人群
        self._create_fleet()

        # 创建Play按钮。
        self.play_button = Button(self, "Play")

        self.fire = False

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._fire_bullet()

            self._update_screen()

    # 每当用户按键时，都将在Pygame中注册一个事件。事件都是通过方法pygame.event.get() 获取的
    # 因此需要在方法_check_events() 中指定要检查哪些类型的事件。每次按键都被注册为一个KEYDOWN 事件。
    def _check_events(self):
        """监视键盘和鼠标事件"""
        # 为访问Pygame检测到的事件，我们使用了函数pygame.event.get()
        # 这个函数返回一个列表，其中包含它在上一次被调用后发生的所有事件。所有键盘和鼠标事件都将导致这个for循环运行。
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 使用pygame.mouse.get_pos() ，它返回一个元组，其中包含玩家单击时鼠标的坐标，我们将这些值传递给新方法_check_play_button()
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单击Play按钮时开始新游戏。"""
        # 使用rect的方法collidepoint()检查鼠标单击位置是否在Play按钮的rect内
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.start_game()

    def start_game(self):
        """按p开始游戏"""
        # 重置游戏统计信息，给玩家提供三艘新飞船，将game_active设置为True
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # 清空余下的外星人和子弹。
        self.aliens.empty()
        self.bullets.empty()

        # 创建一群新的外星人并让飞船居中。
        self._create_fleet()
        self.ship.center_ship()

        # 隐藏鼠标光标。
        # set_visible() 传递False ，让Pygame在光标位于游戏窗口内时将其隐藏起来。
        pygame.mouse.set_visible(False)

        # 重置游戏设置。
        self.settings.initialize_dynamic_settings()

    def _check_keydown_events(self, event):
        """响应按键。"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            self.start_game()
        elif event.key == pygame.K_SPACE:
            self.fire = True

    def _check_keyup_events(self, event):
        """响应松开。"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_SPACE:
            self.fire = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中。"""
        if len(self.bullets) < self.settings.bullets_allowed and self.fire:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹。"""
        # 更新子弹的位置。
        # 对编组调用update()时，编组自动对其中的每个精灵调用update() 。
        # 因此代码行bullets.update()将为编组bullets中的每颗子弹调用bullet.update()
        self.bullets.update()
        # 因为不能从for循环遍历的列表或编组中删除元素，所以必须遍历编组的副本。
        # 我们使用方法copy()来设置for循环，从而能够在循环中修改bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞。"""
        # 将self.bullets 中所有的子弹都与self.aliens 中所有的外星人进行比较，看它们是否重叠在一起。
        # 每当有子弹和外星人的rect重叠时，groupcollide()就在它返回的字典中添加一个键值对。
        # 与外星人碰撞的子弹都是字典collisions 中的一个键，而与每颗子弹相关的值都是一个列表，其中包含该子弹击中的外星人。
        # 两个实参True让Pygame删除发生碰撞的子弹和外星人。
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                # 调用 prep_score() 来创建一幅包含最新得分的新图像。
                self.sb.prep_score()
                self.sb.check_high_score()

        if not self.aliens:
            # 如果编组aliens 为空，就使用方法empty()删除编组中余下的所有精灵，从而删除现有的所有子弹
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提高等级，增加子弹。
            self.stats.level += 1
            self.settings.bullets_allowed += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置。"""
        self._check_fleet_edges()
        self.aliens.update()
        # for alien in self.aliens.copy():
        #     if alien.rect.top <= 0:
        #         self.aliens.remove(alien)
        # print(len(self.aliens))

        # 函数spritecollideany()接受两个实参：一个精灵和一个编组。
        # 它检查编组是否有成员与精灵发生了碰撞，并在找到与精灵发生碰撞的成员后停止遍历编组。
        # 在这里，它遍历编组aliens ，并返回找到的第一个与飞船发生碰撞的外星人。
        # 如果没有发生碰撞，spritecollideany()将返回None，因此处的if代码块不会执行。
        # 如果找到了与飞船发生碰撞的外星人，它就返回这个外星人，因此if代码块将执行：打印
        # 检查是否有外星人撞到飞船。
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达了屏幕底端。
        self._check_aliens_bottom()

    def _create_fleet(self):
        """创建外星人群。"""
        # 创建一个外星人并计算一行可容纳多少个外星人。
        # 外星人的间距为外星人宽度。
        alien = Alien(self)

        # 属性size是一个元组，包含rect对象的宽度和高度。
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕可容纳多少行外星人。
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # 创建外星人群。
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人，并将其放在当前行。"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施。"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向。"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕。"""

        # 调用方法fill() 用这种背景色填充屏幕。方法fill()用于处理surface，只接受一个实参：一种颜色
        self.screen.fill(self.settings.bg_color)

        # 填充背景后，调用ship.blitme()将飞船绘制到屏幕上，确保它出现在背景前面
        self.ship.draw_ship()

        # bullets.sprites()返回一个列表，其中包含编组bullets中的所有精灵
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # 调用draw()时，Pygame将把编组中的每个元素绘制到属性rect指定的位置。
        # 方法draw()接受一个参数，这个参数指定了要将编组中的元素绘制到哪个surface上
        self.aliens.draw(self.screen)

        # 显示得分。
        self.sb.show_score()

        # 如果游戏处于非活动状态，就绘制Play按钮。
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 调用pygame.display.flip() ，命令Pygame让最近绘制的屏幕可见。
        # 在这里，它在每次执行while循环时都绘制一个空屏幕，并擦去旧屏幕，使得只有新屏幕可见。
        # 我们移动游戏元素时，pygame.display.flip()将不断更新屏幕，以显示元素的新位置，并且在原来的位置隐藏元素，从而营造平滑移动的效果。
        pygame.display.flip()

    def _ship_hit(self):
        """响应飞船被外星人撞到。"""

        if self.stats.ships_left > 0:
            # 将ships_left减1。
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 清空余下的外星人和子弹。
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底端的中央。
            self._create_fleet()
            self.ship.center_ship()

            # 暂停。
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端。"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            # 到达屏幕底端后，外星人的属性rect.bottom 大于或等于屏幕的属性rect.bottom
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理。
                self._ship_hit()
                break


if __name__ == '__main__':
    # 创建游戏并运行
    ai = AlienInvasion()
    ai.run_game()
