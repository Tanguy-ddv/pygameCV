
from pygamecv.drawing import circle, ellipse, arc, pie
from pygame import image, display
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

save_dir = "test_results"
test_circle(save_dir)