import pyxel


class Player:
    FRAMES = {
        "right": [(48, 112), (48, 128), (48, 144)],
        "left": [(0, 112), (0, 128), (0, 144)],
        "up": [(32, 112), (32, 128), (32, 144)],
        "down": [(16, 112), (16, 128), (16, 144)],
    }

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 0
        self.climbing = False
        self.direction = "down"
        self.moving = False

    def draw(self):
        frames = self.FRAMES[self.direction]
        if self.moving:
            index = (pyxel.frame_count // 6) % len(frames)
        else:
            index = 0
        u, v = frames[index]
        pyxel.blt(self.x, self.y, 0, u, v, 16, 16, colkey=1, scale=2)


class Enemy:
    FRAMES = [(48, 96), (64, 96), (80, 96)]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = "right"

    def touches(self, player):
        return self.x <= player.x + 13 and player.x + 2 <= self.x + 15 and self.y <= player.y + 19 and player.y - 8 <= self.y + 15

    def draw(self):
        index = (pyxel.frame_count // 6) % len(self.FRAMES)
        u, v = self.FRAMES[index]
        pyxel.blt(self.x, self.y, 0, u, v, 16, 16, colkey=1, scale=2)
