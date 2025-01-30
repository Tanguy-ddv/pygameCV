
from pygamecv.drawing import circle, ellipse, arc, pie, line, lines, rectangle, rounded_rectangle, polygon
from pygamecv.effects import saturate, desaturate, set_saturation, lighten, darken, set_luminosity, shift_hue, set_hue
from pygame import image, display, Rect, draw
import numpy as np
import os

def init(save_dir):
    display.init()
    display.set_mode((100, 100))
    img = image.load("Lenna.png")
    img_alpha = image.load("Lenna_alpha.png")
    os.makedirs(save_dir, exist_ok=True)
    return img, img_alpha

def test_circle(save_dir):
    img, img_alpha = init(save_dir)
    img = circle(img, (100, 200), 100, (255, 255, 0, 255), 50, True)
    img = circle(img, (200, 100), 100, (255, 0, 0, 255), 0, False)
    img = circle(img, (300, 300), 70, (0, 255, 0, 255), 50, False)
    img = circle(img, (400, 150), 100, (255, 0, 255, 255), 0, True)
    img = circle(img, (0, 0), 100, (0, 255, 255, 255), 50, True)
    img = circle(img, (500, 500), 100, (0, 255, 255, 255), 50, True)

    img_alpha = circle(img_alpha, (100, 200), 100, (255, 255, 0, 255), 50, True)
    img_alpha = circle(img_alpha, (200, 100), 100, (255, 0, 0, 255), 0, False)
    img_alpha = circle(img_alpha, (300, 300), 70, (0, 255, 0, 100), 50, False)
    img_alpha = circle(img_alpha, (400, 150), 100, (255, 0, 255, 255), 0, True)
    img_alpha = circle(img_alpha, (0, 0), 100, (0, 255, 255, 255), 50, True)
    img_alpha = circle(img_alpha, (500, 500), 100, (0, 255, 255, 255), 50, True)
    img_alpha = circle(img_alpha, (450, 400), 50, (0, 0, 255, 125), 0, True)

    image.save(img, os.path.join(save_dir, "circles.png"))
    image.save(img_alpha, os.path.join(save_dir, "circles_alpha.png"))

def test_ellipse(save_dir):
    img, img_alpha = init(save_dir)
    img = ellipse(img, (100, 200), 100, 100, (255, 255, 0, 255), 50, True, 0)
    img = ellipse(img, (200, 100), 100, 50, (255, 0, 0, 255), 0, False, -30)
    img = ellipse(img, (300, 300), 70, 10, (0, 255, 0, 255), 50, False, 45)
    img = ellipse(img, (400, 150), 100, 0, (255, 0, 255, 255), 0, True)
    img = ellipse(img, (0, 0), 100, 100, (0, 255, 255, 255), 50, True)
    img = ellipse(img, (500, 500), 100, 200, (0, 255, 255, 255), 50, True)

    img_alpha = ellipse(img_alpha, (100, 200), 100, 100, (255, 255, 0, 255), 50, True, 0)
    img_alpha = ellipse(img_alpha, (200, 100), 100, 50, (255, 0, 0, 255), 0, False, -30)
    img_alpha = ellipse(img_alpha, (300, 300), 70, 10, (0, 255, 0, 100), 50, False, 45)
    img_alpha = ellipse(img_alpha, (400, 150), 100, 0, (255, 0, 255, 255), 0, True)
    img_alpha = ellipse(img_alpha, (0, 0), 100, 100, (0, 255, 255, 255), 50, True)
    img_alpha = ellipse(img_alpha, (500, 500), 100, 200, (0, 255, 255, 125), 50, True)

    image.save(img, os.path.join(save_dir, "ellipses.png"))
    image.save(img_alpha, os.path.join(save_dir, "ellipses_alpha.png"))

def test_arc(save_dir):
    img, img_alpha = init(save_dir)
    img = arc(img, (100, 200), 100, 100, (255, 255, 0, 255), 50, True, 0, 0, 100)
    img = arc(img, (200, 100), 100, 50, (255, 0, 0, 255), 0, False, -30, 0, 200)
    img = arc(img, (300, 300), 70, 10, (0, 255, 0, 255), 20, False, 45, -10, -100)
    img = arc(img, (400, 150), 100, 0, (255, 0, 255, 255), 0, True, 0, 0, 360)

    img_alpha = arc(img_alpha, (100, 200), 100, 100, (255, 255, 0, 125), 50, True, 0, 0, 100)
    img_alpha = arc(img_alpha, (200, 100), 100, 50, (255, 0, 0, 255), 0, False, -30, 0, 200)
    img_alpha = arc(img_alpha, (300, 300), 70, 10, (0, 255, 0, 255), 20, False, 45, -10, -100)
    img_alpha = arc(img_alpha, (400, 150), 100, 0, (255, 0, 255, 100), 0, True, 0, 0, 360)

    image.save(img, os.path.join(save_dir, "arcs.png"))
    image.save(img_alpha, os.path.join(save_dir, "arcs_alpha.png"))

def test_pie(save_dir):
    img, img_alpha = init(save_dir)
    img = pie(img, (100, 200), 100, 100, (255, 255, 0, 255), 50, True, 0, 0, 100)
    img = pie(img, (200, 100), 100, 50, (255, 0, 0, 255), 0, False, -30, 0, 200)
    img = pie(img, (300, 300), 70, 10, (0, 255, 0, 255), 20, False, 45, -10, -100)
    img = pie(img, (400, 150), 100, 0, (255, 0, 255, 255), 0, True, 0, 0, 360)

    img_alpha = pie(img_alpha, (100, 200), 100, 100, (255, 255, 0, 125), 50, True, 0, 0, 100)
    img_alpha = pie(img_alpha, (200, 100), 100, 50, (255, 0, 0, 255), 0, False, -30, 0, 200)
    img_alpha = pie(img_alpha, (300, 300), 70, 10, (0, 255, 0, 255), 20, False, 45, -10, -100)
    img_alpha = pie(img_alpha, (400, 150), 100, 0, (255, 0, 255, 100), 0, True, 0, 0, 360)

    image.save(img, os.path.join(save_dir, "pies.png"))
    image.save(img_alpha, os.path.join(save_dir, "pies_alpha.png"))

def test_line(save_dir):
    img, img_alpha = init(save_dir)
    img = line(img, (100, 200), (100, 100), (255, 255, 0, 255), 50, True)
    img = line(img, (200, 100), (100, 50), (255, 0, 0, 255), 0, False)
    img = line(img, (300, 300), (70, 10), (0, 255, 0, 255), 20, False)
    img = line(img, (400, 150), (100, 0), (255, 0, 255, 255), 10, True)

    img_alpha = line(img_alpha, (100, 200), (100, 100), (255, 255, 0, 125), 50, True)
    img_alpha = line(img_alpha, (200, 100), (100, 50), (255, 0, 0, 255), 0, False)
    img_alpha = line(img_alpha, (300, 300), (70, 10), (0, 255, 0, 255), 20, False)
    img_alpha = line(img_alpha, (400, 150), (100, 0), (255, 0, 255, 70), 10, True)

    image.save(img, os.path.join(save_dir, "lines.png"))
    image.save(img_alpha, os.path.join(save_dir, "lines_alpha.png"))

def test_lines(save_dir):
    img, img_alpha = init(save_dir)
    img = lines(img, [(100, 200), (100, 100), (200, 300)], (255, 255, 0, 255), 50, True, True)
    img = lines(img, [(200, 100), (100, 50), (50, 50)], (255, 0, 0, 255), 5, False, True)
    img = lines(img, [(300, 300), (70, 10), (10, 10)], (0, 255, 0, 255), 20, False, False)
    img = lines(img, [(400, 150), (100, 0), (400, 400)], (255, 0, 255, 255), 10, True, False)

    img_alpha = lines(img_alpha, [(100, 200), (100, 100), (200, 300)], (255, 255, 0, 125), 50, True, True)
    img_alpha = lines(img_alpha, [(200, 100), (100, 50), (50, 50)], (255, 0, 0, 255), 5, False, True)
    img_alpha = lines(img_alpha, [(300, 300), (70, 10), (10, 10)], (0, 255, 0, 125), 20, False, False)
    img_alpha = lines(img_alpha, [(400, 150), (100, 0), (400, 400)], (255, 0, 255, 255), 10, True, False)

    image.save(img, os.path.join(save_dir, "liness.png"))
    image.save(img_alpha, os.path.join(save_dir, "liness_alpha.png"))

def test_rectangle(save_dir):
    img, img_alpha = init(save_dir)
    img = rectangle(img, Rect((100, 200),  (200, 300)), (255, 255, 0, 255), 50)
    img = rectangle(img, Rect((200, 100), (50, 50)), (255, 0, 0, 255), 5)
    img = rectangle(img, Rect((300, 300), (10, 10)), (0, 255, 0, 255), 0)
    img = rectangle(img, Rect((400, 150), (400, 400)), (255, 0, 255, 255), 0)

    img_alpha = rectangle(img_alpha, Rect((100, 200),  (200, 300)), (255, 255, 0, 50), 50)
    img_alpha = rectangle(img_alpha, Rect((200, 100), (50, 50)), (255, 0, 0, 255), 5)
    img_alpha = rectangle(img_alpha, Rect((300, 300), (10, 10)), (0, 255, 0, 255), 0)
    img_alpha = rectangle(img_alpha, Rect((400, 150), (400, 400)), (255, 0, 255, 200), 0)

    image.save(img, os.path.join(save_dir, "rectangles.png"))
    image.save(img_alpha, os.path.join(save_dir, "rectangles_alpha.png"))

def test_rounded_rectangle(save_dir):
    img, img_alpha = init(save_dir)
    img = rounded_rectangle(img, Rect((100, 200),  (200, 300)), (255, 255, 0, 255), 0, True, 50)
    img = rounded_rectangle(img, Rect((200, 100), (50, 50)), (255, 0, 0, 255), 5, True, 0)
    img = rounded_rectangle(img, Rect((300, 300), (10, 10)), (0, 255, 0, 255), 0, False, 10, 10, 20, 20)
    img = rounded_rectangle(img, Rect((200, 150), (200, 200)), (255, 0, 255, 255), 0, True, 100, 0, 0, 100)

    img_alpha = rounded_rectangle(img_alpha, Rect((100, 200),  (200, 300)), (255, 255, 0, 50), 0, True, 100)
    img_alpha = rounded_rectangle(img_alpha, Rect((200, 100), (50, 50)), (255, 0, 0, 255), 5, True, 0)
    img_alpha = rounded_rectangle(img_alpha, Rect((300, 300), (10, 10)), (0, 255, 0, 255), 0, False, 10, 10, 20, 20)
    img_alpha = rounded_rectangle(img_alpha, Rect((200, 150), (200, 200)), (255, 0, 255, 200), 0, True, 100, 0, 0, 100)

    draw.rect(img_alpha, (0, 0, 0, 255), Rect((100, 200),  (200, 300)), 10)

    image.save(img, os.path.join(save_dir, "rounded_rectangles.png"))
    image.save(img_alpha, os.path.join(save_dir, "rounded_rectangles_alpha.png"))

def test_polygon(save_dir):
    img, img_alpha = init(save_dir)
    img = polygon(img, [(100, 200), (100, 100), (200, 300)], (255, 255, 0, 255), 50, True)
    img = polygon(img, [(200, 100), (100, 50), (50, 50)], (255, 0, 0, 255), 5, False)
    img = polygon(img, [(300, 300), (70, 10), (10, 10)], (0, 255, 0, 255), 0, False)
    img = polygon(img, [(400, 150), (100, 0), (400, 400)], (255, 0, 255, 255), 10, True)

    img_alpha = polygon(img_alpha, [(100, 200), (100, 100), (200, 300)], (255, 255, 0, 125), 50, True)
    img_alpha = polygon(img_alpha, [(200, 100), (100, 50), (50, 50)], (255, 0, 0, 255), 5, False)
    img_alpha = polygon(img_alpha, [(300, 300), (70, 10), (10, 10)], (0, 255, 0, 125), 20, False)
    img_alpha = polygon(img_alpha, [(400, 150), (100, 0), (400, 400)], (255, 0, 255, 255), 10, True)

    image.save(img, os.path.join(save_dir, "polygones.png"))
    image.save(img_alpha, os.path.join(save_dir, "polygones_alpha.png"))

def circle_mask(width, height) -> np.ndarray:
    x_grid, y_grid = np.ogrid[:width, :height]
    radius = min(width/2, height/2)
    mask = (x_grid - width/2 + 0.5)**2 + (y_grid - height/2 + 0.5)**2 < radius**2
    return mask.astype(float)

def test_circle(width, height):
    mask = circle_mask(width, height)
    print(mask)

def test_saturatation(save_dir):
    img, _ = init(save_dir)
    img = saturate(img, 0.5)
    image.save(img, os.path.join(save_dir, "saturation50.png"))

    img, _ = init(save_dir)
    img = saturate(img, 0.1)
    image.save(img, os.path.join(save_dir, "saturation10.png"))

    img, _ = init(save_dir)
    img = saturate(img, 1)
    image.save(img, os.path.join(save_dir, "saturation100.png"))

    img, _ = init(save_dir)
    mask = circle_mask(*img.get_size())
    img =saturate(img, mask)
    image.save(img, os.path.join(save_dir, "saturationcircle.png"))

    img, _ = init(save_dir)
    img = desaturate(img, 0.5)
    image.save(img, os.path.join(save_dir, "desaturation50.png"))

    img, _ = init(save_dir)
    img = desaturate(img, 0.1)
    image.save(img, os.path.join(save_dir, "desaturation10.png"))

    img, _ = init(save_dir)
    img = desaturate(img, 1)
    image.save(img, os.path.join(save_dir, "desaturation100.png"))

    img, _ = init(save_dir)
    mask = circle_mask(*img.get_size())
    img = desaturate(img, mask)
    image.save(img, os.path.join(save_dir, "desaturationcircle.png"))

    img, _ = init(save_dir)
    img = set_saturation(img, 0.5)
    image.save(img, os.path.join(save_dir, "set_saturation50.png"))

    img, _ = init(save_dir)
    img = set_saturation(img, 1)
    image.save(img, os.path.join(save_dir, "set_saturation100.png"))

    img, _ = init(save_dir)
    mask = circle_mask(*img.get_size())
    img = set_saturation(img, mask)
    image.save(img, os.path.join(save_dir, "set_sturationcircle.png"))

def test_luminosity(save_dir):
    img, _ = init(save_dir)
    img = lighten(img, 0.5)
    image.save(img, os.path.join(save_dir, "lighten50.png"))

    img, _ = init(save_dir)
    img = lighten(img, 0.1)
    image.save(img, os.path.join(save_dir, "lighten10.png"))

    img, _ = init(save_dir)
    img = lighten(img, 1)
    image.save(img, os.path.join(save_dir, "lighten100.png"))

    img, _ = init(save_dir)
    mask = circle_mask(*img.get_size())
    img = lighten(img, mask)
    image.save(img, os.path.join(save_dir, "lightencircle.png"))

    img, _ = init(save_dir)
    img = darken(img, 0.5)
    image.save(img, os.path.join(save_dir, "darken50.png"))

    img, _ = init(save_dir)
    img = darken(img, 0.1)
    image.save(img, os.path.join(save_dir, "darken10.png"))

    img, _ = init(save_dir)
    img = darken(img, 1)
    image.save(img, os.path.join(save_dir, "darken100.png"))

    img, _ = init(save_dir)
    mask = circle_mask(*img.get_size())
    img = darken(img, mask)
    image.save(img, os.path.join(save_dir, "darkencircle.png"))

    img, _ = init(save_dir)
    img = set_luminosity(img, 0.5)
    image.save(img, os.path.join(save_dir, "set_luminosity50.png"))

    img, _ = init(save_dir)
    img = set_luminosity(img, 1)
    image.save(img, os.path.join(save_dir, "set_luminosity100.png"))

    img, _ = init(save_dir)
    mask = circle_mask(*img.get_size())
    img = set_luminosity(img, mask)
    image.save(img, os.path.join(save_dir, "set_luminositycircle.png"))

def test_hue(save_dir):
    
    img, _ = init(save_dir)
    img = shift_hue(img, 0.5)
    image.save(img, os.path.join(save_dir, "huet50.png"))

    img, _ = init(save_dir)
    img = shift_hue(img, 0.1)
    image.save(img, os.path.join(save_dir, "hue10.png"))

    img, _ = init(save_dir)
    img = shift_hue(img, 1)
    image.save(img, os.path.join(save_dir, "hue100.png"))

    img, _ = init(save_dir)
    mask = circle_mask(*img.get_size())
    img = shift_hue(img, mask/2)
    image.save(img, os.path.join(save_dir, "huecircle.png"))

    img, _ = init(save_dir)
    img = set_hue(img, 0.2)
    image.save(img, os.path.join(save_dir, "set_hue50.png"))

    img, _ = init(save_dir)
    img = set_hue(img, 0.6)
    image.save(img, os.path.join(save_dir, "set_hue100.png"))

    img, _ = init(save_dir)
    mask = circle_mask(*img.get_size())
    img = set_hue(img, mask/2)
    image.save(img, os.path.join(save_dir, "set_huecircle.png"))


save_dir = "test_results"
# test_circle(save_dir)
# test_ellipse(save_dir)
# test_arc(save_dir)
# test_pie(save_dir)
# test_line(save_dir)
# test_lines(save_dir)
# test_rounded_rectangle(save_dir)
# test_polygon(save_dir)
# test_circle(15, 7)
# test_saturatation(save_dir)
# test_luminosity(save_dir)
test_hue(save_dir)
