"""The art._drawing submodule contains functions to draw something on an Art."""

import numpy as np
from pygame import Surface, surfarray as sa, Rect, draw
import cv2 as cv
from .decorator import cv_transformation
from .common import get_ellipse_rect

@cv_transformation
def _cv_circle(surf_array: np.ndarray, center: tuple[int, int], radius: int, color: tuple[int, int, int, int], thickness: int):
    cv.circle(surf_array, center, radius, color, thickness, cv.LINE_AA, 0)

def circle(surface: Surface, center: tuple[int, int], radius: int, color: tuple[int, int, int, int], thickness: int, antialias: bool):
    if antialias:
        rect = Rect(center[0] - radius, center[1] - radius, 2*radius+1, 2*radius+1)
        center = radius + thickness//2, radius + thickness//2
        return _cv_circle(surface, rect=rect, center=center, radius=radius, color=color, thickness=thickness if thickness else -1)
    else:
        draw.circle(surface, color, center, radius, thickness)
        return surface

@cv_transformation
def _cv_ellipse(
    surf_array: np.ndarray,
    center: tuple[int, int],
    radius_x: int, radius_y: int,
    angle: int, start_angle: int, end_angle: int,
    color: tuple[int, int, int, int],
    thickness: int,
    antialias: bool
):
    line_type = cv.LINE_AA if antialias else cv.LINE_8
    cv.ellipse(surf_array, center, (radius_x, radius_y), angle, start_angle, end_angle, color, thickness, line_type, 0)

def ellipse(surface: Surface, center: tuple[int, int], radius_x: int, radius_y: int, color: tuple[int, int, int, int], thickness: int, antialias: bool, angle: int = 0):
    rect = get_ellipse_rect(center, radius_x, radius_y, thickness, angle)

    if antialias or angle:
        center = radius_x + thickness//2, radius_y + thickness//2
        return _cv_ellipse(
            surface,
            rect,
            center=center,
            radius_x=radius_x, radius_y=radius_y,
            color=color,
            thickness=thickness if thickness else -1,
            angle=angle, start_angle=0, end_angle=360,
            antialias=antialias
        )
    else:
        draw.ellipse(surface, color, rect, thickness)
        return surface

def arc(
    surface, 
    center: tuple[int, int],
    radius_x: int,
    radius_y: int,
    color: tuple[int, int, int, int],
    thickness: int,
    antialias: bool,
    angle: int,
    start_angle: int,
    end_angle: int
):
    rect = get_ellipse_rect(center, radius_x, radius_y, thickness, angle)
    if antialias or thickness == 0 or angle:
        center = radius_x + thickness//2, radius_y + thickness//2
        return _cv_ellipse(
            surface,
            rect,
            center=center,
            radius_x=radius_x, radius_y=radius_y,
            color=color,
            thickness=thickness if thickness else -1,
            angle=angle, start_angle=start_angle, end_angle=end_angle,
            antialias=antialias
        )
    else:
        draw.arc(surface, color, rect, start_angle, end_angle, thickness)

