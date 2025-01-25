
import math
import numpy as np
from pygame import Surface, surfarray as sa, image, pixelcopy, SRCALPHA, Rect, draw


def get_rotated_rect(original_rect: Rect, angle: int):
    """Return the rect after rotation."""
    theta = math.radians(angle)

    w, h = original_rect.width, original_rect.height
    cx, cy = original_rect.center
    
    new_width = int(w * abs(math.cos(theta)) + h * abs(math.sin(theta)))
    new_height = int(h * abs(math.cos(theta)) + w * abs(math.sin(theta)))
    
    new_rect = Rect(0, 0, new_width, new_height)
    new_rect.center = (cx, cy)
    
    return new_rect

def get_ellipse_rect(center, radius_x, radius_y, thickness, angle):
    """Compute the rect necessary to draw an ellipse."""
    rect = Rect(center[0] - radius_x - thickness//2, center[1] - radius_y - thickness//2, 2*radius_x + thickness+1, 2*radius_y + thickness+1)
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

def polygon_points_from_line(p1: tuple[int, int], p2: tuple[int, int], thickness: int):
    """Calculate the points needed to draw a thick line as a polygon."""
    d = (p2[0] - p1[0], p2[1] - p1[1])
    dis = math.hypot(*d)
    deltas = (-d[1]/dis*thickness/2, d[0]/dis*thickness/2)

    p1_1 = (p1[0] - deltas[0], p1[1] - deltas[1])
    p1_2 = (p1[0] + deltas[0], p1[1] + deltas[1])
    p2_1 = (p2[0] - deltas[0], p2[1] - deltas[1])
    p2_2 = (p2[0] + deltas[0], p2[1] + deltas[1])

    return p1_1, p1_2, p2_1, p2_2

def start_stop_arc(center, radius_x, radius_y, start_angle, end_angle, angle):
     
    def get_rotated_point(center, radius_x, radius_y, edge_angle, angle):
        angle_rad = math.radians(edge_angle)
        rotation_rad = math.radians(angle)
        
        x = radius_x * math.cos(angle_rad)
        y = radius_y * math.sin(angle_rad)
        
        rotated_x = x * math.cos(rotation_rad) - y * math.sin(rotation_rad)
        rotated_y = x * math.sin(rotation_rad) + y * math.cos(rotation_rad)
        
        return (int(center[0] + rotated_x), int(center[1] + rotated_y))
    
    return get_rotated_point(center, radius_x, radius_y, start_angle, angle), get_rotated_point(center, radius_x, radius_y, end_angle, angle)