import pyxel


class Map:
    TILES = {
        "1": (0, 80), "j": (0, 96),
        "2": (0, 64), "a": (16, 64), "b": (32, 64),
        "3": (48, 0), "c": (48, 16),
        "4": (96, 64), "5": (64, 16), "6": (80, 16),
        "7": (112, 0), "8": (128, 32), "9": (144, 16),
        "x": (80, 32), "y": (80, 48), "l": (48, 64),
    }

    PASSABLE = {".", "x", "y", "4"}
    LADDER = {"x", "y"}
    ONE_WAY = {"4"}
    DEADLY = {"1"}

    def __init__(self, ascii_rows):
        self.spawn_x = 32
        self.spawn_y = 32
        self.rows = []
        self.enemy_spawns = []
        self.pressed = False

        for y, row in enumerate(ascii_rows):
            if "S" in row:
                self.spawn_x = row.index("S") * 16
                self.spawn_y = (y + 1) * 16 - 21
                row = row.replace("S", ".")

            for x, tile in enumerate(row):
                if tile == "E":
                    self.enemy_spawns.append((x * 16, y * 16))
            row = row.replace("E", ".")

            self.rows.append(row)

    def draw(self):
        for y, row in enumerate(self.rows):
            for x, tile in enumerate(row):
                if tile not in ".i":
                    u, v = self.TILES[tile]
                    if tile == "8" and self.pressed:
                        v = 48
                    pyxel.blt(x * 16, y * 16, 0, u, v, 16, 16, colkey=1)

    def is_free(self, col_min, col_max, y_top, y_bottom):
        for col in range(col_min, col_max + 1):
            for row in range(y_top // 16, y_bottom // 16 + 1):
                tile = self.rows[row][col]
                if tile in self.PASSABLE:
                    continue
                if tile == "8" and row == y_bottom // 16 and y_bottom % 16 < 11:
                    continue
                return False
        return True

    def is_ladder(self, x, y):
        return self.rows[y // 16][x // 16] in self.LADDER

    def is_button(self, x, feet_y):
        return self.rows[feet_y // 16][x // 16] == "8" and feet_y % 16 >= 11

    def is_deadly(self, col_min, col_max, feet_y):
        for col in range(col_min, col_max + 1):
            if self.rows[feet_y // 16][col] in self.DEADLY:
                return True
        return False

    def has_ground(self, col_min, col_max, feet_y):
        for col in range(col_min, col_max + 1):
            if self.rows[feet_y // 16][col] in self.ONE_WAY and feet_y % 16 == 0:
                return True
        return not self.is_free(col_min, col_max, feet_y, feet_y)
