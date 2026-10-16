import pyxel

from screens import Menu, Game, Pause, LevelComplete, Death, GameOver, Win
from settings import FPS, WIDTH, HEIGHT


class World:

    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="Ladder Fight", fps=FPS)
        pyxel.load("U3.pyxres")
        self.menu = Menu(self)
        self.game = Game(self)
        self.pause = Pause(self)
        self.level_complete = LevelComplete(self)
        self.death = Death(self)
        self.game_over = GameOver(self)
        self.win = Win(self)
        self.screen = self.menu
        pyxel.run(self.update, self.draw)

    def update(self):
        self.screen.update()

    def draw(self):
        pyxel.cls(0)
        self.screen.draw()


if __name__ == "__main__":
    World()
