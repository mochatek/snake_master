import arcade
from random import randint
from sys import platform
if platform == "linux" or platform == "linux2" or platform == "darwin":
    head_png = 'res/head.png'
    body_png = 'res/Body.png'
    tail_png = 'res/Tail.png'
    frog_png = 'res/Frog.png'
else:
    head_png = 'res\head.png'
    body_png = 'res\Body.png'
    tail_png = 'res\Tail.png'
    frog_png = 'res\Frog.png'

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
TITLE = 'Snake Master'

class Snake(arcade.Sprite):
    def __init__(self, xy, angle, part):
        super().__init__()
        self.textures = []
        texture = arcade.load_texture(head_png)
        self.textures.append(texture)
        texture = arcade.load_texture(body_png)
        self.textures.append(texture)
        texture = arcade.load_texture(tail_png)
        self.textures.append(texture)
        self.scale = 0.25
        self.center_x = xy[0]
        self.center_y = xy[1]
        self.angle = angle
        self.set_texture(part)

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
        self.snake = None
        self.frame = None
        self.change_x = None
        self.change_y = None
        self.angle = None
        self.frog = None
        self.score = None
        self.game = None

    def setup(self):
        self.frame = 1
        self.score = 0
        self.change_x = 0
        self.change_y = 0
        self.angle = -90
        self.snake = arcade.SpriteList()
        self.frog = arcade.SpriteList()
        self.snake.append(Snake((96,224), -90, 2))
        self.snake.append(Snake((112,224), -90, 1))
        self.snake.append(Snake((128,224), -90, 0))
        self.frog.append(arcade.Sprite(frog_png, 0.25, center_x=320, center_y=320))
        self.game = 'Running'

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(str(self.score),305,320, arcade.color.WHITE,50)
        self.frog.draw()
        self.snake.draw()
        if self.game == 'Over':
            arcade.draw_text('GAME OVER',260,260, arcade.color.ORANGE,25)

    def on_update(self, delta_time):
        if self.game == 'Running':
            self.snake.update()
            self.frog.update()
            self.frame += 1
            if self.snake[-1].left > 640:
                self.snake[-1].center_x = 0
            elif self.snake[-1].right < 0:
                self.snake[-1].center_x = 640
            if self.snake[-1].top > 640:
                self.snake[-1].center_y = 0
            elif self.snake[-1].bottom < 0:
                self.snake[-1].center_y = 640

            eat_list = arcade.check_for_collision_with_list(self.snake[-1], self.frog)
            if len(eat_list) > 0:
                for frog in eat_list:
                    frog.remove_from_sprite_lists()
                    self.score += 1
                    self.snake[0].set_texture(1)
                    self.snake.insert(0,Snake((self.snake[0].center_x - self.change_x, self.snake[0].center_y - self.change_y), self.angle, 2))

            hit_list = arcade.check_for_collision_with_list(self.snake[-1], self.snake)
            if len(hit_list) > 0:
                self.game = 'Over'

            if (self.change_x != 0 or self.change_y != 0) and self.frame % 5 == 0:
                self.snake[-1].set_texture(1)
                self.snake.append(Snake((self.snake[-1].center_x + self.change_x, self.snake[-1].center_y + self.change_y), self.angle, 0))
                self.snake[0].kill()
                self.snake[0].set_texture(2)

            if self.frame % 120 == 0:
                if len(self.frog) > 1:
                    self.frog[0].remove_from_sprite_lists()
                frog = arcade.Sprite(frog_png, 0.25)
                frog.center_x = randint(40, 600)
                frog.center_y = randint(40, 640)
                self.frog.append(frog)


    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            if self.change_y >= 0:
                self.change_y = 16
                self.change_x = 0
                self.angle = 0
        elif symbol == arcade.key.DOWN:
            if self.change_y <= 0:
                self.change_y = -16
                self.change_x = 0
                self.angle = -180
        elif symbol == arcade.key.RIGHT:
            if self.change_x >= 0:
                self.change_y = 0
                self.change_x = 16
                self.angle = -90
        elif symbol == arcade.key.LEFT:
            if self.change_x <= 0:
                self.change_y = 0
                self.change_x = -16
                self.angle = 90

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()