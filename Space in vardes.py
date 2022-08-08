import arcade
import random
import time
TITLE = "Space warden"
HEIGHT = 700
WIDTH = 1300
BULLET_SCALE = 0.1
X_WING_SCALE = 0.6
BULLET_SPEED = 6
ENEMY_SCALE = 0.23
ENEMY_SPEED = 3
BOOM_SCALE = 1
FAILS = 5
class Boom(arcade.Sprite):
    def __init__(self):
        super().__init__("Новая папка\Взрыв.png",BOOM_SCALE)
        self.start = time.time()
        self.sound = arcade.load_sound("Новая папка\Record (online-voice-recorder.com).mp3")
    def update(self):
        if time.time() - self.start > 1:
            self.kill()
            if space_warden.alive ==False:
                space_warden.game = True
class X_wing(arcade.Sprite):
    def __init__(self):
        super().__init__("Новая папка\X-wing_good.png", X_WING_SCALE)
        self.bottom = 10
        self.center_x = WIDTH/2
    def update(self):
        if self.left <= 0:
            self.left = 0
        if self.right >= WIDTH:
            self.right = WIDTH
class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__("Новая папка\T-fighter.png", ENEMY_SCALE)
        self.change_y = ENEMY_SPEED
    def update(self):
        self.center_y -= self.change_y
        if self.top < 0:
            space_warden.tries -= 1
            self.kill()
class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Новая папка\Фиолетовый.jpg", BULLET_SCALE)
        self.angle = 90
        self.change_y = BULLET_SPEED
        tx_1 = arcade.load_texture("Новая папка\Фиолетовый.jpg")
        tx_2 = arcade.load_texture("Новая папка\Синий.jpg")
        tx_3 = arcade.load_texture("Новая папка\Красный.jpg")
        tx_4 = arcade.load_texture("Новая папка\Зелёный.jpg")
        list = [tx_1, tx_2, tx_3, tx_4]
        self.texture = random.choice(list)
        self.sound = arcade.load_sound("Новая папка\laser-warble_f1dcq_e_.mp3")
    def update(self):
        self.center_y+= self.change_y
        if self.bottom>HEIGHT:
            self.kill()
class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.game = False
        self.tx = arcade.load_texture("Новая папка\Фон.jpg")
        self.x_wing = X_wing()
        self.tx_1 = arcade.load_texture("Новая папка\Империя.jpg")
        self.lasers = arcade.SpriteList()
        self.t_figthers = arcade.SpriteList()
        self.booms = arcade.SpriteList()
        self.alive = True
        self.tries = FAILS
    def set_up(self):
        for i in range(50):
            enemy = Enemy()
            enemy.center_y = HEIGHT + i * 100
            enemy.center_x = random.randint(0,WIDTH)
            if enemy.left < 0:
                enemy.left = 0
            if enemy.right > WIDTH:
                enemy.right = WIDTH
            self.t_figthers.append(enemy)
    def on_draw(self):
        if self.game == False:
            self.clear((124, 150, 178))
            arcade.draw_texture_rectangle(center_x=WIDTH/2, center_y=HEIGHT/2, height=HEIGHT, width=WIDTH, texture=self.tx)
            self.x_wing.draw()
            self.lasers.draw()
            self.t_figthers.draw()
            self.booms.draw()
            if self.game == False:
                self.a = False
        if self.game == True or self.tries == 0:
            arcade.draw_texture_rectangle(center_x=WIDTH/2, center_y=HEIGHT/2, height=HEIGHT, width=WIDTH, texture=self.tx_1)
    def on_update(self, delta_time):
        if self.game == False:
            if self.tries == 0:
                self.game = True
            self.x_wing.update()
            self.lasers.update()
            self.t_figthers.update()
            self.booms.update()
            for laser in self.lasers:
                hit_list = arcade.check_for_collision_with_list(laser, self.t_figthers)
                if len(hit_list) > 0:
                    laser.kill()
                    for a in hit_list:
                        boom = Boom()
                        boom.sound.play(1)
                        boom.center_x = a.center_x
                        boom.center_y = a.center_y
                        self.booms.append(boom)
                        a.kill()
            list = arcade.check_for_collision_with_list(self.x_wing,self.t_figthers)
            if len(list) > 0:
                boom = Boom()
                boom.center_x = self.x_wing.center_x
                boom.center_y = self.x_wing.center_y
                self.alive = False
                self.booms.append(boom)
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.x_wing.center_x = x
        self.set_mouse_visible(False)
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            laser = Bullet()
            laser.center_x = self.x_wing.left
            laser.bottom = self.x_wing.top
            laser.sound.play(1)
            self.lasers.append(laser)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            laser1 = Bullet()
            laser1.center_x = self.x_wing.right
            laser1.bottom = self.x_wing.top
            laser1.sound.play(1)
            self.lasers.append(laser1)
space_warden = Window(WIDTH, HEIGHT, TITLE)
space_warden.set_up()
arcade.run()