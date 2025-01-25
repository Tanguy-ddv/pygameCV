
from pygamecv.drawing import circle, ellipse, arc, pie
from pygame import image
import os
img = image.load("Lenna.png")
dir = "test_results"
os.makedirs(dir, exist_ok=True)
img = circle(img, (100, 200), 100, (255, 255, 0, 255), 50, True)
img = circle(img, (200, 100), 100, (255, 0, 0, 255), 0, False)
img = circle(img, (300, 300), 70, (0, 255, 0, 255), 50, False)
img = circle(img, (400, 150), 100, (255, 0, 255, 255), 0, True)
#img = circle(img, (0, 0), 100, (0, 255, 255, 255), 50, True)
img = circle(img, (500, 500), 100, (0, 255, 255, 255), 50, True)
img = ellipse(img, (0, 0), 50, 100, (0, 255, 255, 255), 50, True)

image.save(img, os.path.join(dir, "circle.png"))