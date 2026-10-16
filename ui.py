import pyxel


def draw_big_text(text, center_x, center_y, color, scale):
    width = len(text) * 4
    img = pyxel.Image(width, 6)
    img.cls(1)
    img.text(0, 0, text, color)
    pyxel.blt(center_x - width // 2, center_y - 3, img, 0, 0, width, 6, colkey=1, scale=scale)


def draw_hearts(lives, max_lives, center_x, y):
    left = center_x - max_lives * 18 // 2
    for i in range(max_lives):
        u = 208 if i < lives else 224
        pyxel.blt(left + i * 18, y, 0, u, 0, 16, 16, colkey=1)
