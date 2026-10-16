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
        self.hitbox_offset_x = 2
        self.hitbox_width = 12
        self.visual_height = 20
        self.head_height = 8
        self.jump_speed = 9

    def hitbox_left(self):
        return self.x + self.hitbox_offset_x

    def hitbox_right(self):
        return self.x + self.hitbox_offset_x + self.hitbox_width - 1

    def draw(self):
        frames = self.FRAMES[self.direction]
        if self.moving:
            index = (pyxel.frame_count // 6) % len(frames)
        else:
            index = 0
        u, v = frames[index]
        pyxel.blt(self.x, self.y, 0, u, v, 16, 16, colkey=1, scale=2)
