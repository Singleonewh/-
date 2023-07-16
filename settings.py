class Settings:
    """存储游戏中所以设置的类"""
    def __init__(self):
        """初始化游戏的设置"""
        #屏幕设置
        self.screen_width = 1280
        self.screen_height = 960
        self.bg_color = (0,0,255)
        self.ship_speed = 1.5

        #子弹设置
        self.bullet_speed = 2.0
        self.bullet_width = 8000
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allow = 3 #限制子弹数量

        #外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 1
        # fleet_direction 为1表示向右移动 -1表示向左移动
        self.fleet_direction = 1
