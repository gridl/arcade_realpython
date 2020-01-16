import random

import arcade

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Arcade Space Shooter'
SCALING = 2.0


class FlyingSprite(arcade.Sprite):
    def update(self):
        super().update()

        if self.right < 0:
            self.remove_from_sprite_lists()


class SpaceShooter(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.enemies_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

    def setup(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.player = arcade.Sprite('images/jet.png', SCALING)
        self.player.center_y = self.height / 2
        self.player.left = 10

        self.all_sprites.append(self.player)

        arcade.schedule(self.add_enemy, 0.25)
        arcade.schedule(self.add_cloud, 1.0)
        self.paused = False

    def add_enemy(self, delta_time: float):
        enemy = FlyingSprite('images/missile.png', SCALING)
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)
        enemy.velocity = (random.randint(-20, -5), 0)

        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)

    def add_cloud(self, delta_time: float):
        cloud = FlyingSprite('images/cloud.png', SCALING)
        cloud.left = random.randint(self.width, self.width + 80)
        cloud.top = random.randint(10, self.height -10)
        cloud.velocity = (random.randint(-5, -2), 0)

        self.clouds_list.append(cloud)
        self.all_sprites.append(cloud)

    def on_draw(self):
        arcade.start_render()
        self.all_sprites.draw()

    def on_update(self, delta_time: float):
        if self.paused:
            return

        self.all_sprites.update()

        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.Q:
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol in (arcade.key.I, arcade.key.UP):
            self.player.change_y = 5

        if symbol in (arcade.key.K, arcade.key.DOWN):
            self.player.change_y = -5

        if symbol in (arcade.key.J, arcade.key.LEFT):
            self.player.change_x = -5

        if symbol in (arcade.key.L, arcade.key.RIGHT):
            self.player.change_x = 5

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in (arcade.key.I, arcade.key.K,
                      arcade.key.UP, arcade.key.DOWN):
            self.player.change_y = 0

        if symbol in (arcade.key.J, arcade.key.L,
                      arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0


if __name__ == '__main__':
    app = SpaceShooter(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    app.setup()
    arcade.run()
