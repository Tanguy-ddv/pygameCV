
from pygamecv.drawing import circle, ellipse, arc, pie, line, lines, rectangle, rounded_rectangle, polygon
from pygame import image, display, Rect, draw
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


save_dir = "test_results"
# test_circle(save_dir)
# test_ellipse(save_dir)
# test_arc(save_dir)
# test_pie(save_dir)
# test_line(save_dir)
# test_lines(save_dir)
# test_rounded_rectangle(save_dir)
test_polygon(save_dir)