
import math
import numpy as np
from pygame import Surface, surfarray as sa, image, pixelcopy, SRCALPHA, Rect, draw


def get_rotated_rect(original_rect: Rect, angle: int):
    """Return the rect after rotation."""
    theta = math.radians(angle)

    w, h = original_rect.width, original_rect.height
    cx, cy = original_rect.center
    
    new_width = w * abs(math.cos(theta)) + h * abs(math.sin(theta))
    new_height = h * abs(math.cos(theta)) + w * abs(math.sin(theta))
    
    new_rect = Rect(0, 0, new_width, new_height)
    new_rect.center = (cx, cy)
    
    return new_rect

def get_ellipse_rect(center, radius_x, radius_y, thickness, angle):
    """Compute the rect necessary to draw an ellipse."""
    rect = Rect(center[0] - radius_x, center[1] - radius_y, 2*radius_x + thickness+1, 2*radius_y + thickness+1)
    if angle != 0:
        # Rotate the rect to fit the rotated ellipsis.
        rect = get_rotated_rect(rect, angle)
    return rect

def  make_surface_rgba(array: np.ndarray):
    """Returns a surface made from a [w, h, 4] numpy array with per-pixel alpha."""
    surface = Surface(array.shape[:2], SRCALPHA, 32) # Create a transparent surface with alpha channel
    pixelcopy.array_to_surface(surface, array[:, :, :3]) # set the rgb
    sa.pixels_alpha(surface)[:] = array[:, :, 3] # set the alpha
    return surface