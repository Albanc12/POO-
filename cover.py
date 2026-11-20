import pyxel

from ui import draw_big_text, format_time


class Cover:
    LETTERS = {
        " ": ["...", "...", "...", "...", "...", "...", "..."],
        "!": ["XX", "XX", "XX", "XX", "XX", "..", "XX"],
        "A": [".XXX.", "XX.XX", "XX.XX", "XXXXX", "XX.XX", "XX.XX", "XX.XX"],
        "C": [".XXXX", "XX...", "XX...", "XX...", "XX...", "XX...", ".XXXX"],
        "D": ["XXXX.", "XX.XX", "XX.XX", "XX.XX", "XX.XX", "XX.XX", "XXXX."],
        "E": ["XXXXX", "XX...", "XX...", "XXXX.", "XX...", "XX...", "XXXXX"],
        "F": ["XXXXX", "XX...", "XX...", "XXXX.", "XX...", "XX...", "XX..."],
        "G": [".XXXX", "XX...", "XX...", "XX.XX", "XX.XX", "XX.XX", ".XXXX"],
        "H": ["XX.XX", "XX.XX", "XX.XX", "XXXXX", "XX.XX", "XX.XX", "XX.XX"],
        "I": ["XXXX", ".XX.", ".XX.", ".XX.", ".XX.", ".XX.", "XXXX"],
        "L": ["XX...", "XX...", "XX...", "XX...", "XX...", "XXXXX", "XXXXX"],
        "M": ["XX...XX", "XXX.XXX", "XXXXXXX", "XX.X.XX", "XX...XX", "XX...XX", "XX...XX"],
        "O": [".XXX.", "XX.XX", "XX.XX", "XX.XX", "XX.XX", "XX.XX", ".XXX."],
        "R": ["XXXX.", "XX.XX", "XX.XX", "XXXX.", "XX.XX", "XX.XX", "XX.XX"],
        "T": ["XXXXXX", "..XX..", "..XX..", "..XX..", "..XX..", "..XX..", "..XX.."],
        "U": ["XX.XX", "XX.XX", "XX.XX", "XX.XX", "XX.XX", "XX.XX", ".XXX."],
        "V": ["XX.XX", "XX.XX", "XX.XX", "XX.XX", "XX.XX", ".XXX.", "..X.."],
    }
    SHADOWS = {6: 5, 7: 13, 8: 2, 9: 4, 10: 9, 11: 3, 12: 5, 13: 5, 14: 8}
    LIGHTS = {6: 7, 7: 7, 8: 14, 9: 10, 10: 7, 11: 7, 12: 6, 13: 7, 14: 7}

    def __init__(self):
        self.sheet = pyxel.Image(256, 256)
        self.sheet.blt(0, 0, pyxel.images[0], 0, 0, 256, 256)
        cells = [(48, 80), (96, 32), (96, 48), (128, 32), (144, 32), (144, 48), (144, 64), (48, 96), (64, 96), (80, 96), (208, 0), (224, 0)]
        for v in range(112, 208, 16):
            for u in range(0, 64, 16):
                cells.append((u, v))
        for u, v in cells:
            self.clean_cell(u, v)

    def clean_cell(self, u, v):
        bank = pyxel.images[0]
        for y in range(v, v + 16):
            for x in range(u, u + 16):
                if bank.pget(x, y) == 0 and not self.touches_color(bank, x, y, u, v):
                    self.sheet.pset(x, y, 1)

    def touches_color(self, bank, x, y, u, v):
        for ny in range(max(v, y - 1), min(v + 16, y + 2)):
            for nx in range(max(u, x - 1), min(u + 16, x + 2)):
                if bank.pget(nx, ny) > 1:
                    return True
        return False

    def draw_sprite(self, x, y, u, v, w, h, scale, flip=False, rotate=0):
        offset_x = w * (scale - 1) / 2
        offset_y = h * (scale - 1) / 2
        if flip:
            w = -w
        pyxel.blt(x + offset_x, y + offset_y, self.sheet, u, v, w, h, colkey=1, rotate=rotate, scale=scale)

    def draw_sky(self):
        pyxel.cls(12)
        pyxel.rect(0, 0, 512, 70, 5)
        pyxel.dither(0.5)
        pyxel.rect(0, 70, 512, 50, 5)
        pyxel.rect(0, 280, 512, 60, 6)
        pyxel.dither(1.0)
        pyxel.rect(0, 340, 512, 172, 6)

    def draw_rays(self, center_x, center_y, color):
        pyxel.dither(0.3)
        for i in range(12):
            angle = i * 30 + pyxel.frame_count / 3
            x1 = center_x + 800 * pyxel.cos(angle)
            y1 = center_y + 800 * pyxel.sin(angle)
            x2 = center_x + 800 * pyxel.cos(angle + 15)
            y2 = center_y + 800 * pyxel.sin(angle + 15)
            pyxel.tri(center_x, center_y, x1, y1, x2, y2, color)
        pyxel.dither(1.0)

    def draw_cloud(self, x, y, colors=(5, 6, 7)):
        outline, shade, light = colors
        puffs = [(0, 10, 13), (18, 2, 16), (38, 0, 18), (58, 8, 14), (30, 14, 14)]
        for dx, dy, r in puffs:
            pyxel.circ(x + dx, y + dy, r + 2, outline)
        for dx, dy, r in puffs:
            pyxel.circ(x + dx, y + dy, r, shade)
        for dx, dy, r in puffs:
            pyxel.circ(x + dx - 2, y + dy - 3, r - 2, light)

    def draw_clouds(self):
        for base_x, y in [(110, 214), (330, 70), (190, 316), (450, 340)]:
            x = (base_x + pyxel.frame_count // 4) % 640 - 80
            self.draw_cloud(x, y)

    def draw_far_ghosts(self):
        frame = pyxel.frame_count // 8 % 3
        pyxel.dither(0.5)
        for x, y in [(30, 130), (196, 300), (300, 196)]:
            bob = pyxel.sin(pyxel.frame_count * 6 + x) * 4
            self.draw_sprite(x, y + bob, 48 + frame * 16, 96, 16, 16, 2)
        pyxel.dither(1.0)

    def draw_hills(self):
        pyxel.elli(-80, 300, 280, 260, 11)
        pyxel.elli(300, 280, 300, 280, 11)
        pyxel.dither(0.5)
        pyxel.elli(-80, 300, 280, 260, 6)
        pyxel.elli(300, 280, 300, 280, 6)
        pyxel.dither(1.0)
        pyxel.elli(-40, 360, 260, 220, 0)
        pyxel.elli(-37, 363, 254, 214, 11)
        pyxel.elli(150, 340, 240, 240, 0)
        pyxel.elli(153, 343, 234, 234, 3)
        for x, y in [(40, 400), (80, 385), (60, 430), (230, 380), (270, 360), (300, 400), (210, 420)]:
            pyxel.elli(x, y, 14, 8, 3 if x < 150 else 11)

    def draw_tower(self):
        for row in range(6):
            for col in range(3):
                self.draw_sprite(416 + col * 32, 288 + row * 32, 80, 16, 16, 16, 2)
        self.draw_sprite(448, 288, 80, 32, 16, 16, 2)
        for row in range(1, 6):
            self.draw_sprite(448, 288 + row * 32, 80, 48, 16, 16, 2)
        self.draw_sprite(416, 256, 0, 64, 16, 16, 2)
        self.draw_sprite(448, 256, 16, 64, 16, 16, 2)
        self.draw_sprite(480, 256, 32, 64, 16, 16, 2)
        self.draw_sprite(412, 228, 128, 32, 16, 16, 2)

    def draw_ladder(self):
        self.draw_sprite(112, 192, 80, 32, 16, 16, 4)
        for row in range(1, 4):
            self.draw_sprite(112, 192 + row * 64, 80, 48, 16, 16, 4)

    def draw_water(self):
        offset = pyxel.frame_count // 2 % 32
        for x in range(-32, 544, 32):
            self.draw_sprite(x - offset, 480, 0, 80, 16, 16, 2)

    def draw_floor(self):
        self.draw_water()
        self.draw_sprite(0, 448, 0, 64, 16, 16, 2)
        for col in range(1, 15):
            self.draw_sprite(col * 32, 448, 16, 64, 16, 16, 2)
        self.draw_sprite(480, 448, 32, 64, 16, 16, 2)

    def draw_ground(self):
        self.draw_water()
        self.draw_sprite(0, 384, 0, 0, 48, 64, 2)
        for col in range(5):
            self.draw_sprite(96 + col * 32, 448, 16, 64, 16, 16, 2)
        self.draw_sprite(256, 448, 32, 64, 16, 16, 2)
        self.draw_sprite(352, 448, 0, 64, 16, 16, 2)
        self.draw_sprite(384, 448, 16, 64, 16, 16, 2)
        self.draw_sprite(56, 288, 144, 32, 16, 48, 2)
        self.draw_sprite(8, 352, 96, 16, 16, 16, 2)
        self.draw_sprite(196, 416, 64, 48, 16, 16, 2)

    def draw_heroes(self):
        climb = pyxel.frame_count // 8 % 3
        self.draw_sprite(92, 236 - climb * 2, 48, 112 + climb * 16, 16, 16, 6)
        jump = abs(pyxel.sin(pyxel.frame_count * 9)) * 14
        self.draw_sprite(440, 181 - jump, 0, 176, 16, 16, 5)

    def draw_ghosts(self):
        u = 48 + pyxel.frame_count // 6 % 3 * 16
        bob = pyxel.sin(pyxel.frame_count * 9) * 8
        for i in range(3):
            pyxel.line(352 + i * 6, 286 + i * 16 + bob, 384 + i * 10, 286 + i * 16 + bob, 7)
        self.draw_sprite(268, 262 + bob, u, 96, 16, 16, 5, flip=True)
        for x, y, speed in [(204, 372, 11), (338, 350, 8)]:
            bob = pyxel.sin(pyxel.frame_count * speed + x) * 8
            self.draw_sprite(x, y + bob, u, 96, 16, 16, 3, flip=x > 300)

    def draw_sparkle(self, x, y, size):
        size = size + pyxel.sin(pyxel.frame_count * 12 + x * 7) * 2
        pyxel.line(x - size, y, x + size, y, 7)
        pyxel.line(x, y - size, x, y + size, 7)
        pyxel.line(x - size // 2, y - size // 2, x + size // 2, y + size // 2, 10)
        pyxel.line(x - size // 2, y + size // 2, x + size // 2, y - size // 2, 10)
        pyxel.circ(x, y, 1, 7)

    def draw_star(self, x, y, radius, color):
        for i in range(5):
            angle = i * 72 - 90
            pyxel.tri(x, y, x + radius * pyxel.cos(angle), y + radius * pyxel.sin(angle),
                      x + radius / 2 * pyxel.cos(angle + 36), y + radius / 2 * pyxel.sin(angle + 36), color)
            pyxel.tri(x, y, x + radius * pyxel.cos(angle), y + radius * pyxel.sin(angle),
                      x + radius / 2 * pyxel.cos(angle - 36), y + radius / 2 * pyxel.sin(angle - 36), color)

    def draw_treasures(self):
        for i in range(5):
            x = 204 + i * 36
            y = 212 + pyxel.sin(i * 45) * 14 + pyxel.sin(pyxel.frame_count * 10 + i * 60) * 3
            self.draw_sprite(x, y, 96, 48, 16, 16, 2)
        self.draw_sprite(20, 222, 48, 80, 16, 16, 3)
        self.draw_sprite(372, 416, 96, 32, 16, 16, 2)
        for x, y, size in [(30, 226, 6), (70, 266, 4), (400, 414, 5), (430, 440, 3), (196, 206, 4), (384, 214, 5), (426, 226, 4), (90, 190, 3)]:
            self.draw_sparkle(x, y, size)

    def draw_letter(self, rows, x, y, block, color):
        blocks = []
        for row_index, row in enumerate(rows):
            for col_index, cell in enumerate(row):
                if cell == "X":
                    blocks.append((col_index, row_index))
        depth = block // 2
        border = block // 3
        for col, row in blocks:
            pyxel.rect(x + col * block - border, y + row * block - border, block + 2 * border + depth // 2, block + 2 * border + depth, 0)
        for col, row in blocks:
            pyxel.rect(x + col * block + depth // 2, y + row * block + depth, block, block, self.SHADOWS[color])
        for col, row in blocks:
            pyxel.rect(x + col * block, y + row * block, block, block, color)
        for col, row in blocks:
            if (col, row - 1) not in blocks:
                pyxel.rect(x + col * block, y + row * block + 2, block, block // 4, self.LIGHTS[color])
            if (col - 1, row) not in blocks:
                pyxel.rect(x + col * block + 2, y + row * block, block // 4, block, self.LIGHTS[color])

    def word_width(self, word, block):
        width = -block
        for letter in word:
            width += (len(self.LETTERS[letter][0]) + 1) * block
        return width

    def draw_word(self, word, center_x, y, block, colors):
        x = center_x - self.word_width(word, block) // 2
        for i, letter in enumerate(word):
            rows = self.LETTERS[letter]
            bounce = pyxel.sin(pyxel.frame_count * 8 + i * 45) * 3
            self.draw_letter(rows, x, y + bounce, block, colors[i % len(colors)])
            x += (len(rows[0]) + 1) * block

    def draw_logo(self):
        self.draw_word("LADDER", 256, 26, 9, [8, 10, 11, 12, 14, 9])
        self.draw_word("FIGHT", 256, 104, 12, [10])

    def draw_outlined_text(self, text, center_x, center_y, color, scale):
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (2, 2)]:
            draw_big_text(text, center_x + dx, center_y + dy, 0, scale)
        draw_big_text(text, center_x, center_y, color, scale)

    def draw_badges(self):
        pyxel.rect(14, 16, 72, 24, 0)
        pyxel.rect(16, 18, 68, 20, 8)
        draw_big_text("PYXEL", 50, 28, 7, 2)

        center_x, center_y = 464, 54
        for radius, color in [(42, 0), (38, 10)]:
            pyxel.circ(center_x, center_y, radius - 8, color)
            for i in range(16):
                angle = i * 22.5 + pyxel.frame_count / 2
                pyxel.tri(center_x + (radius - 10) * pyxel.cos(angle - 12), center_y + (radius - 10) * pyxel.sin(angle - 12),
                          center_x + (radius - 10) * pyxel.cos(angle + 12), center_y + (radius - 10) * pyxel.sin(angle + 12),
                          center_x + radius * pyxel.cos(angle), center_y + radius * pyxel.sin(angle), color)
        draw_big_text("4", center_x, center_y - 7, 8, 4)
        draw_big_text("LEVELS", center_x, center_y + 15, 8, 2)

    def draw_press_enter(self, text):
        pyxel.rect(116, 478, 280, 26, 0)
        pyxel.circ(116, 490, 13, 0)
        pyxel.circ(395, 490, 13, 0)
        if pyxel.frame_count % 30 < 20:
            draw_big_text(text, 256, 491, 10, 2)

    def draw_frame(self):
        for i in range(4):
            pyxel.rectb(i, i, 512 - 2 * i, 512 - 2 * i, 0)
        pyxel.rectb(4, 4, 504, 504, 7)

    def draw(self):
        self.draw_sky()
        self.draw_rays(256, 140, 7)
        self.draw_clouds()
        self.draw_far_ghosts()
        self.draw_hills()
        self.draw_tower()
        self.draw_ladder()
        self.draw_ground()
        self.draw_treasures()
        self.draw_ghosts()
        self.draw_heroes()
        self.draw_logo()
        self.draw_badges()
        self.draw_press_enter("PRESS ENTER TO PLAY")
        self.draw_frame()


class DeathCover(Cover):

    def __init__(self, game):
        super().__init__()
        self.game = game

    def draw_sky(self):
        pyxel.cls(2)
        pyxel.rect(0, 0, 512, 80, 1)
        pyxel.dither(0.5)
        pyxel.rect(0, 80, 512, 70, 1)
        pyxel.rect(0, 260, 512, 70, 8)
        pyxel.dither(1.0)
        pyxel.rect(0, 330, 512, 182, 8)

    def draw_sunset(self):
        pyxel.circ(256, 430, 150, 9)
        pyxel.circ(256, 430, 120, 10)
        for i in range(6):
            y = 318 + i * 20
            half = pyxel.sqrt(120 * 120 - (430 - y) ** 2)
            pyxel.rect(256 - half, y, 2 * half, 2 + i, 9)

    def draw_clouds(self):
        for base_x, y in [(40, 250), (300, 200), (420, 300), (150, 340)]:
            x = (base_x + pyxel.frame_count // 4) % 640 - 80
            self.draw_cloud(x, y, (2, 14, 15))

    def draw_hills(self):
        pyxel.elli(-90, 370, 330, 220, 0)
        pyxel.elli(-87, 373, 324, 214, 4)
        pyxel.elli(270, 360, 340, 240, 0)
        pyxel.elli(273, 363, 334, 234, 2)

    def draw_dizzy_boy(self):
        wobble = pyxel.sin(pyxel.frame_count * 10) * 10
        self.draw_sprite(208, 358, 16, 112, 16, 16, 6, rotate=wobble)
        for i in range(3):
            angle = pyxel.frame_count * 8 + i * 120
            x = 256 + 54 * pyxel.cos(angle)
            y = 360 + 12 * pyxel.sin(angle)
            self.draw_star(x, y, 11, 0)
            self.draw_star(x, y, 8, 10)

    def draw_laughing_ghost(self):
        u = 48 + pyxel.frame_count // 6 % 3 * 16
        bob = pyxel.sin(pyxel.frame_count * 9) * 8
        self.draw_sprite(330, 236 + bob, u, 96, 16, 16, 5, flip=True)
        pyxel.rect(404, 198 + bob, 90, 38, 0)
        pyxel.rect(406, 200 + bob, 86, 34, 7)
        pyxel.tri(404, 232 + bob, 420, 232 + bob, 392, 250 + bob, 0)
        pyxel.tri(408, 230 + bob, 418, 230 + bob, 397, 245 + bob, 7)
        draw_big_text("BOO!", 449, 217 + bob, 8, 3)

    def draw_hearts(self):
        left = 256 - self.game.max_lives * 56 // 2 + 4
        for i in range(self.game.max_lives):
            u = 208 if i < self.game.lives else 224
            if i == self.game.lives and pyxel.frame_count % 20 < 10:
                u = 208
            self.draw_sprite(left + i * 56, 140, u, 0, 16, 16, 3)
        if self.game.lives == 1:
            text = "1 LIFE LEFT"
        else:
            text = str(self.game.lives) + " LIVES LEFT"
        self.draw_outlined_text(text, 256, 212, 7, 2)

    def draw_stats(self):
        pyxel.dither(0.6)
        pyxel.rect(24, 240, 150, 96, 0)
        pyxel.dither(1.0)
        pyxel.rectb(24, 240, 150, 96, 14)
        draw_big_text("LEVEL " + str(self.game.level + 1), 99, 262, 10, 2)
        draw_big_text("TIME " + format_time(self.game.timer.seconds), 99, 288, 7, 2)
        draw_big_text("SCORE " + str(self.game.score), 99, 314, 7, 2)

    def draw(self):
        self.draw_sky()
        self.draw_rays(256, 430, 10)
        self.draw_sunset()
        self.draw_clouds()
        self.draw_hills()
        self.draw_floor()
        self.draw_dizzy_boy()
        self.draw_laughing_ghost()
        self.draw_stats()
        self.draw_word("OUCH!", 256, 26, 13, [10])
        self.draw_hearts()
        self.draw_press_enter("PRESS ENTER TO TRY AGAIN")
        self.draw_frame()


class GameOverCover(Cover):

    def __init__(self, game):
        super().__init__()
        self.game = game

    def draw_sky(self):
        pyxel.cls(1)
        pyxel.rect(0, 0, 512, 90, 0)
        pyxel.dither(0.5)
        pyxel.rect(0, 90, 512, 70, 0)
        pyxel.rect(0, 300, 512, 80, 5)
        pyxel.dither(1.0)

    def draw_stars(self):
        for i in range(60):
            x = i * 97 % 480 + 16
            y = i * 61 % 270 + 16
            if (pyxel.frame_count // 3 + i * 7) % 30 < 24:
                pyxel.rect(x, y, 2, 2, 7 if i % 3 else 10)
            if i % 8 == 0:
                self.draw_sparkle(x, y, 3)

    def draw_moon(self):
        pyxel.dither(0.3)
        pyxel.circ(452, 66, 50, 6)
        pyxel.dither(1.0)
        pyxel.circ(452, 66, 36, 0)
        pyxel.circ(452, 66, 34, 15)
        pyxel.circ(440, 56, 7, 13)
        pyxel.circ(462, 82, 5, 13)
        pyxel.circ(468, 54, 4, 13)

    def draw_hills(self):
        pyxel.elli(-90, 340, 350, 260, 0)
        pyxel.elli(-87, 343, 344, 254, 5)
        pyxel.elli(250, 330, 360, 280, 0)
        pyxel.elli(253, 333, 354, 274, 1)
        for x, y in [(34, 330), (130, 318), (370, 322), (452, 338)]:
            self.draw_small_grave(x, y)

    def draw_small_grave(self, x, y):
        pyxel.circ(x + 10, y, 12, 0)
        pyxel.rect(x - 2, y, 25, 26, 0)
        pyxel.circ(x + 10, y, 10, 13)
        pyxel.rect(x, y, 21, 24, 13)
        pyxel.line(x + 10, y - 4, x + 10, y + 12, 5)
        pyxel.line(x + 5, y + 1, x + 15, y + 1, 5)

    def draw_tombstone(self):
        pyxel.circ(256, 300, 58, 0)
        pyxel.rect(198, 300, 117, 150, 0)
        pyxel.circ(256, 300, 54, 13)
        pyxel.rect(202, 300, 109, 148, 13)
        pyxel.dither(0.5)
        pyxel.rect(300, 296, 11, 152, 5)
        pyxel.dither(1.0)
        pyxel.line(222, 262, 232, 280, 5)
        pyxel.line(232, 280, 226, 294, 5)
        draw_big_text("R.I.P.", 256, 330, 5, 4)
        draw_big_text("LADDER", 256, 372, 5, 2)
        draw_big_text("HERO", 256, 392, 5, 2)
        for x in range(204, 312, 12):
            pyxel.tri(x, 448, x + 6, 432 + x % 3 * 4, x + 12, 448, 3)

    def draw_orbiting_ghosts(self, front):
        u = 48 + pyxel.frame_count // 6 % 3 * 16
        for i in range(5):
            angle = pyxel.frame_count * 2 + i * 72
            depth = pyxel.sin(angle)
            if (depth > 0) == front:
                scale = 3 + depth
                x = 256 + 180 * pyxel.cos(angle) - 8 * scale
                y = 296 + 44 * depth - 8 * scale
                if not front:
                    pyxel.dither(0.5)
                self.draw_sprite(x, y, u, 96, 16, 16, scale, flip=pyxel.cos(angle + 90) > 0)
                pyxel.dither(1.0)

    def draw_crying_heroes(self):
        self.draw_sprite(56, 373, 16, 160, 16, 16, 5)
        self.draw_sprite(376, 373, 16, 112, 16, 16, 5)
        tear = pyxel.frame_count % 20
        for x, y in [(87, 408), (102, 408), (407, 413), (422, 413)]:
            pyxel.rect(x, y + tear, 3, 4, 6)
            pyxel.pset(x + 1, y + tear + 4, 12)

    def draw_stats(self):
        self.draw_outlined_text("FINAL SCORE " + str(self.game.score), 256, 206, 10, 3)
        text = "TIME " + format_time(self.game.timer.seconds) + "   LEVEL " + str(self.game.level + 1)
        self.draw_outlined_text(text, 256, 236, 7, 2)

    def draw(self):
        self.draw_sky()
        self.draw_stars()
        self.draw_moon()
        self.draw_hills()
        self.draw_floor()
        self.draw_orbiting_ghosts(False)
        self.draw_tombstone()
        self.draw_crying_heroes()
        self.draw_orbiting_ghosts(True)
        self.draw_word("GAME", 256, 22, 11, [13])
        self.draw_word("OVER", 256, 108, 11, [8])
        self.draw_stats()
        self.draw_press_enter("PRESS ENTER FOR THE MENU")
        self.draw_frame()
