import sys
import time
import keyboard
import pygame
from settings import Settings   #from 后面是导入的文件名称
from Ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        #全屏模式
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()  #用于存储有效的子弹
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def _check_events(self):  #辅助方法一般以单下划线开头 _ 并在本类中使用
         """响应按键和鼠标事件"""
         for event in pygame.event.get():
            # if event.type == pygame.QUIT:
            #     sys.exit()
            # elif keyboard.is_pressed("q"):
            #     sys.exit()
            # elif event.key == pygame.K_q:
            #     sys.exit()
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    def _check_keydown_events(self, event):
        """响应按下"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.QUIT:
            sys.exit()
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应释放"""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        """判断子弹数量"""
        if len(self.bullets) < self.settings.bullets_allow:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除已消失的子弹"""
        #更新子弹的位置
        self.bullets.update()

        #删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        """检查是否有子弹击中了外星人，如果是，则删除相应的子弹和外星人"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
        # 删除现有的子弹并创建一个新的外星舰队
            self.bullets.empty()
            self._create_fleet()



    def _create_fleet(self):
        """创建一个外形舰队"""
        # 创造一个外星人
        # 不断添加外星人，知道没有空间为止
        alien = Alien(self)
        alien_width = alien.rect.width
        current_x = alien_width
        while current_x < (self.settings.screen_width - 2 * alien_width):
            self._create_alien(current_x)
            current_x += 2 * alien_width

    def _create_alien(self, x_position):
        """创建一个外星人并将其防在当前行中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """在有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            self._change_fleet_direction()
            break


    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1





    def _update_screen(self):
        # 让最近绘制的屏幕可见
        # 更新屏幕上的图像，并切换到新屏幕
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(144)

    def _update_aliens(self):
        """更新外星舰队中所以外星人的位置"""
        """检查是否有外星人处于屏幕边缘，并更新整个外星舰队的位置"""
        self._check_fleet_edges()
        self.aliens.update()


    def run_game(self):
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()


            #每次循环都重绘屏幕
            self._update_screen()




#创建游戏实例并运行游戏
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

