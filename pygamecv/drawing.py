"""The art._drawing submodule contains functions to draw something on an Art."""

import numpy as np
from pygame import Surface, draw, gfxdraw, Color
import cv2 as cv
from .decorator import cv_transformation
from .common import get_ellipse_rect, polygon_points_from_line, start_stop_arc

@cv_transformation
def _cv_circle(surf_array: np.ndarray, center: tuple[int, int], radius: int, color: Color, thickness: int, antialias):
    line_type = cv.LINE_AA if antialias else cv.LINE_8
    cv.circle(surf_array, center, radius, tuple(color), thickness, line_type, 0)

@cv_transformation
def _cv_ellipse(
    surf_array: np.ndarray,
    center: tuple[int, int],
    radius_x: int, radius_y: int,
    angle: int, start_angle: int, end_angle: int,
    color: Color,
    thickness: int,
    antialias: bool
):
    line_type = cv.LINE_AA if antialias else cv.LINE_8
    cv.ellipse(surf_array, center, (radius_x, radius_y), angle, start_angle, end_angle, tuple(color), thickness, line_type, 0)

def line(surface: Surface, p1: tuple[int, int], p2: tuple[int, int], color: Color, thickness: int, antialias: bool):
    if antialias:
        points = polygon_points_from_line(p1, p2, thickness)
        gfxdraw.aapolygon(surface, points, color)
        gfxdraw.filled_polygon(surface, points, color)
    else:
        draw.line(surface, color, p1, p2, thickness)
    return surface

def circle(surface: Surface, center: tuple[int, int], radius: int, color: Color, thickness: int, antialias: bool):
    color = Color(color)
    if antialias or (surface.get_alpha() and color.a != 255):
        rect = get_ellipse_rect(center, radius, radius, thickness, 0)
        center = radius + thickness//2, radius + thickness//2
        return _cv_circle(surface, rect=rect, center=center, radius=radius, color=tuple(color), thickness=thickness if thickness else -1, antialias=antialias)
    else:
        draw.circle(surface, color, center, radius, thickness)
        return surface

def ellipse(surface: Surface, center: tuple[int, int], radius_x: int, radius_y: int, color: Color, thickness: int, antialias: bool, angle: int = 0):
    if radius_x <= 0 or radius_y <= 0:
        return surface
    rect = get_ellipse_rect(center, radius_x, radius_y, thickness, angle)
    color = Color(color)
    if antialias or angle or (surface.get_alpha() and color.a != 255):
        center = rect.width//2, rect.height//2
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
    surface: Surface,
    center: tuple[int, int],
    radius_x: int,
    radius_y: int,
    color: Color,
    thickness: int,
    antialias: bool,
    angle: int,
    start_angle: int,
    end_angle: int
):
    rect = get_ellipse_rect(center, radius_x, radius_y, thickness, angle)
    if antialias or thickness == 0 or angle or (surface.get_alpha() and color.a != 255):
        color = Color(color)
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

def pie(
    surface: Surface,
    center: tuple[int, int],
    radius_x: int,
    radius_y: int,
    color: Color,
    thickness: int,
    antialias: bool,
    angle: int,
    start_angle: int,
    end_angle: int
):
    rect = get_ellipse_rect(center, radius_x, radius_y, thickness, angle)
    color = tuple(color)
    if thickness == 0:
        return _cv_ellipse(surface, rect, radius_x=radius_x, radius_y=radius_x, color=color, thickness=0, antialias=antialias, start_angle=start_angle, end_angle=end_angle)
    else:
        arc =  _cv_ellipse(surface, rect, radius_x=radius_x, radius_y=radius_x, color=color, thickness=thickness, antialias=antialias, start_angle=start_angle, end_angle=end_angle)
        p1, p2 = start_stop_arc(rect.center, radius_x, radius_y, start_angle, end_angle, angle)
        half_pie = line(arc, rect.center, p1, color, thickness)
        return line(half_pie, rect.center, p2, color, thickness)
