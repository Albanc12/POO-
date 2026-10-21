import pyxel

from levels import map1, map2, map3, map4
from player import Player, Enemy
from settings import FPS
from timer import Timer
from ui import draw_big_text, draw_hearts


def format_time(seconds):
    return str(seconds // 60) + ":" + str(seconds % 60).zfill(2)


class Screen:

    def __init__(self, world):
        self.world = world


class Menu(Screen):

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.world.game.new_game()
            self.world.screen = self.world.game

    def draw(self):
        pyxel.cls(1)

        frame_x, frame_y = 40, 180
        frame_width, frame_height = 432, 150
        pyxel.rectb(frame_x, frame_y, frame_width, frame_height, 7)
        pyxel.rectb(frame_x + 2, frame_y + 2, frame_width - 4, frame_height - 4, 5)

        center_x = frame_x + frame_width // 2
        center_y = frame_y + frame_height // 2

        title = "LADDER FIGHT"
        title_x = center_x - len(title) * 4 // 2
        title_y = center_y - 15
        pyxel.text(title_x + 1, title_y + 1, title, 0)
        pyxel.text(title_x, title_y, title, 10)

        if pyxel.frame_count % 30 < 20:
            subtitle = "Press ENTER to play"
            subtitle_x = center_x - len(subtitle) * 4 // 2
            subtitle_y = center_y + 15
            pyxel.text(subtitle_x, subtitle_y, subtitle, 7)


class Game(Screen):

    def __init__(self, world):
        super().__init__(world)
        self.key_count = 0
        self.max_lives = 3
        self.maps = [map1, map2, map3, map4]
        self.press_timer = 0
        self.timer = Timer(FPS)
        self.new_game()

    def new_game(self):
        self.key_count = 0
        self.lives = self.max_lives
        self.score = 0
        self.timer.start()
        self.load_level(0)

    def load_level(self, level):
        self.level = level
        self.map = self.maps[level]
        self.map.pressed = False
        self.player = Player(self.map.spawn_x, self.map.spawn_y)
        self.enemies = []
        for x, y in self.map.enemy_spawns:
            self.enemies.append(Enemy(x, y))
        self.level_start = self.timer.seconds
        self.timer.resume()

    def level_points(self):
        return max(0, 1000 - 10 * (self.timer.seconds - self.level_start))

    def touches_enemy(self):
        for enemy in self.enemies:
            if enemy.touches(self.player):
                return True
        return False

    def update(self):
        self.player.moving = False

        if pyxel.btnp(pyxel.KEY_P):
            self.world.screen = self.world.pause
            return

        if self.map.pressed:
            self.press_timer -= 1
            if self.press_timer <= 0:
                if self.level == len(self.maps) - 1:
                    self.world.win.start()
                    self.world.screen = self.world.win
                else:
                    self.world.level_complete.start()
                    self.world.screen = self.world.level_complete
            return

        self.timer.update()

        for enemy in self.enemies:
            if enemy.direction == "right":
                col = (enemy.x + 16) // 16

                if self.map.is_free(col, col, enemy.y, enemy.y + 15):
                    enemy.x += 1
                else:
                    enemy.direction = "left"
            else:
                col = (enemy.x - 1) // 16

                if self.map.is_free(col, col, enemy.y, enemy.y + 15):
                    enemy.x -= 1
                else:
                    enemy.direction = "right"

        center_x = self.player.x + 7
        y_middle = self.player.y + 10
        on_ladder = self.map.is_ladder(center_x, y_middle)

        if not on_ladder:
            self.player.climbing = False
        elif not self.player.climbing and (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_S)):
            self.player.climbing = True
            self.player.x = center_x // 16 * 16

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            col = (self.player.x + 15) // 16
            y_bottom = self.player.y + 19

            if self.map.is_free(col, col, self.player.y, y_bottom):
                self.player.x += 2
                self.player.direction = "right"
                self.player.moving = True
                self.player.climbing = False

        elif pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q):
            col = self.player.x // 16
            y_bottom = self.player.y + 19

            if self.map.is_free(col, col, self.player.y, y_bottom):
                self.player.x -= 2
                self.player.direction = "left"
                self.player.moving = True
                self.player.climbing = False

        elif self.player.climbing and (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z)):
            check_y = self.player.y - 10
            col_left = (self.player.x + 2) // 16
            col_right = (self.player.x + 13) // 16

            if self.map.is_ladder(center_x, y_middle - 2) and self.map.is_free(col_left, col_right, check_y, check_y):
                self.player.y -= 2
                self.player.direction = "up"
                self.player.moving = True

        elif self.player.climbing and (pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S)):
            feet_y = self.player.y + 22
            col_left = (self.player.x + 2) // 16
            col_right = (self.player.x + 13) // 16

            if self.map.has_ground(col_left, col_right, feet_y):
                self.player.climbing = False
            else:
                self.player.y += 2
                self.player.direction = "up"
                self.player.moving = True

        col_left = (self.player.x + 2) // 16
        col_right = (self.player.x + 13) // 16

        if self.player.climbing:
            self.player.vy = 0

            if pyxel.btnp(pyxel.KEY_SPACE):
                self.player.climbing = False
                self.player.vy = -9
        else:
            self.player.vy = min(self.player.vy + 1, 8)

            feet_y = self.player.y + 21
            on_ground = self.map.has_ground(col_left, col_right, feet_y)

            if pyxel.btnp(pyxel.KEY_SPACE) and on_ground:
                self.player.vy = -9

        step = 1 if self.player.vy > 0 else -1

        for _ in range(abs(self.player.vy)):
            if step == 1:
                feet_y = self.player.y + 21
                blocked = self.map.has_ground(col_left, col_right, feet_y)
            else:
                check_y = self.player.y - 9
                blocked = not self.map.is_free(col_left, col_right, check_y, check_y)

            if blocked:
                self.player.vy = 0
                break

            self.player.y += step

        center_x = self.player.x + 7
        feet_y = self.player.y + 21

        if self.map.is_deadly(col_left, col_right, feet_y) or self.touches_enemy():
            self.lives -= 1
            if self.lives == 0:
                self.world.screen = self.world.game_over
            else:
                self.world.screen = self.world.death
            return

        if self.player.vy == 0 and not self.player.climbing and self.map.is_button(center_x, feet_y):
            self.map.pressed = True
            self.press_timer = 15
            self.timer.stop()

    def draw(self):
        self.map.draw()
        for enemy in self.enemies:
            enemy.draw()
        self.player.draw()

        time_text = format_time(self.timer.seconds)
        score_text = "Score " + str(self.score)
        draw_big_text(time_text, 24 + len(time_text) * 4, 28, 7, 2)
        draw_hearts(self.lives, self.max_lives, 256, 20)
        draw_big_text(score_text, 488 - len(score_text) * 4, 28, 7, 2)

        for i in range(self.key_count):
            pyxel.blt((27 + i) * 16, 3 * 16, 0, 48, 80, 16, 16, colkey=1)


class LevelComplete(Screen):
    OPTIONS = ["Next level", "Restart level", "Menu"]

    def start(self):
        self.choice = 0
        self.seconds = self.world.game.timer.seconds
        self.points = self.world.game.level_points()

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_Z):
            self.choice = (self.choice - 1) % len(self.OPTIONS)
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.choice = (self.choice + 1) % len(self.OPTIONS)
        elif pyxel.btnp(pyxel.KEY_RETURN):
            game = self.world.game

            if self.choice == 0:
                game.score += self.points
                game.load_level(game.level + 1)
                self.world.screen = game
            elif self.choice == 1:
                game.load_level(game.level)
                self.world.screen = game
            else:
                self.world.screen = self.world.menu

    def draw(self):
        pyxel.cls(0)
        game = self.world.game
        draw_big_text("Level " + str(game.level + 1) + " complete", 256, 120, 10, 3)
        draw_big_text("Time  " + format_time(self.seconds), 256, 200, 7, 2)
        draw_big_text("Score  +" + str(self.points), 256, 230, 7, 2)

        for i, option in enumerate(self.OPTIONS):
            color = 10 if i == self.choice else 5
            text = "> " + option if i == self.choice else option
            draw_big_text(text, 256, 320 + i * 35, color, 2)


class Pause(Screen):

    def update(self):
        if pyxel.btnp(pyxel.KEY_P):
            self.world.screen = self.world.game

    def draw(self):
        self.world.game.draw()
        pyxel.dither(0.7)
        pyxel.rect(0, 0, 512, 512, 0)
        pyxel.dither(1.0)

        center_x, center_y = 256, 256
        draw_big_text("Pause", center_x + 2, center_y - 13, 0, 2)
        draw_big_text("Pause", center_x, center_y - 15, 10, 2)

        if pyxel.frame_count % 30 < 20:
            draw_big_text("Press P to play", center_x, center_y + 15, 7, 2)


class Death(Screen):

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            game = self.world.game
            game.player = Player(game.map.spawn_x, game.map.spawn_y)
            self.world.screen = game

    def draw(self):
        pyxel.cls(0)
        game = self.world.game
        draw_big_text("You died", 256, 150, 8, 3)
        draw_hearts(game.lives, game.max_lives, 256, 222)
        draw_big_text("Time  " + format_time(game.timer.seconds), 256, 265, 7, 2)
        draw_big_text("Score  " + str(game.score), 256, 300, 7, 2)

        if pyxel.frame_count % 30 < 20:
            draw_big_text("Press ENTER to try again", 256, 380, 7, 2)


class GameOver(Screen):

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.world.screen = self.world.menu

    def draw(self):
        pyxel.cls(0)
        draw_big_text("Game Over", 256, 200, 10, 3)
        draw_big_text("Press ENTER to return to menu", 256, 300, 7, 2)


class Win(Screen):

    def start(self):
        game = self.world.game
        self.seconds = game.timer.seconds
        self.score = game.score + game.level_points()

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.world.screen = self.world.menu

    def draw(self):
        pyxel.cls(0)
        draw_big_text("You win !", 256, 150, 10, 3)
        draw_big_text("Total time  " + format_time(self.seconds), 256, 240, 7, 2)
        draw_big_text("Total score  " + str(self.score), 256, 275, 7, 2)
        draw_big_text("Press ENTER to return to menu", 256, 360, 7, 2)
