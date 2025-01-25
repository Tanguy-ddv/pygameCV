"""The art._drawing submodule contains functions to draw something on an Art."""

import numpy as np
from pygame import Surface, Color, Rect
import cv2 as cv
from .decorator import cv_transformation
from .common import get_ellipse_rect

@cv_transformation
def _cv_circle(surf_array: np.ndarray, center: tuple[int, int], radius: int, color: Color, thickness: int, antialias):
    line_type = cv.LINE_AA if antialias else cv.LINE_8
    cv.circle(surf_array, center, radius, tuple(color), thickness, line_type, 0)
    return surf_array

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
    return surf_array

@cv_transformation
def _cv_line(
    surf_array: np.ndarray,
    p1: tuple[int, int],
    p2: tuple[int, int],
    color: Color,
    thickness: int,
    antialias: bool
):
    color = tuple(color)
    line_type = cv.LINE_AA if antialias else cv.LINE_8
    overlay = surf_array.copy()
    cv.line(surf_array, p1, p2, tuple(color), thickness, line_type, 0)
    if len(color) == 4:
        alpha = color[3]
        cv.addWeighted(surf_array, alpha/255, overlay, 1 - alpha/255, 0, surf_array)
    
@cv_transformation
def _cv_lines(
    surf_array: np.ndarray,
    points: list[tuple[int, int]],
    color: Color,
    thickness: int,
    antialias: bool,
    closed: bool
):
    color = tuple(color)
    line_type = cv.LINE_AA if antialias else cv.LINE_8
    pad_left = -min(0, min(point[0] for point in points))
    pad_right = max(0, max(point[0] - surf_array.shape[0] for point in points))
    pad_top = -min(0, min(point[1] for point in points))
    pad_bottom = max(0, max(point[1] - surf_array.shape[1] for point in points))
    padded_array = np.pad(surf_array, (
        (pad_left, pad_right), (pad_top, pad_bottom), (0, 0)
    ),
        mode='constant',
        constant_values=((0, 0), (0, 0), (0, 0)))
    overlay = padded_array.copy()
    points = np.array([[point[0] - pad_left, point[1] - pad_top] for point in points], np.int32)
    points = points.reshape((-1, 1, 2))  # Shape it into (n, 1, 2)
    cv.polylines(padded_array, [points], closed, color, thickness, line_type, 0)

    if len(color) == 4:
        alpha = color[3]
        cv.addWeighted(padded_array, alpha/255, overlay, 1 - alpha/255, 0, padded_array)
    surf_array[:, :, :] = padded_array[pad_left: padded_array.shape[0]-pad_right, pad_top: padded_array.shape[1] - pad_bottom]

def circle(surface: Surface, center: tuple[int, int], radius: int, color: Color, thickness: int, antialias: bool):
    if radius <= 1:
        return surface
    color = tuple(color)
    rect = get_ellipse_rect(center, radius, radius, thickness, 0)
    center = radius + thickness//2, radius + thickness//2
    return _cv_circle(surface, rect=rect, center=center, radius=radius, color=color, thickness=thickness if thickness else -1, antialias=antialias)

def ellipse(surface: Surface, center: tuple[int, int], radius_x: int, radius_y: int, color: Color, thickness: int, antialias: bool, angle: int = 0):
    if radius_x <= 0 or radius_y <= 0:
        return surface
    rect = get_ellipse_rect(center, radius_x, radius_y, thickness, angle)
    color = tuple(color)
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
    color = tuple(color)
    center = rect.width//2, rect.height//2
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
    if thickness:
        delta = 6//(antialias+1)
        points = list(cv.ellipse2Poly(center, (radius_x, radius_y), angle, start_angle, end_angle, delta)) + [np.array(center).astype(np.int32)]
        return _cv_lines(surface, points=points, color=color, thickness=thickness, antialias=antialias, closed=True)
    else:
        return arc(surface, center, radius_x, radius_y, color, thickness, antialias, angle, start_angle, end_angle)

def line(surface: Surface, p1: tuple[int, int], p2: tuple[int, int], color: Color, thickness: int, antialias: bool):
    if thickness <= 0:
        return surface
    left = min(p1[0], p2[0]) - thickness//2
    right = max(p1[0], p2[0]) + thickness//2 +1
    top = min(p1[1], p2[1]) - thickness//2
    bottom = max(p1[1], p2[1]) + thickness//2 + 1
    rect = Rect(left, top, right - left, bottom - top)
    p1 = p1[0] - left, p1[1] - top
    p2 = p2[0] - left, p2[1] - top
    return _cv_line(surface, rect, p1 = p1, p2 = p2, color=color, thickness=thickness, antialias=antialias)

def lines(surface: Surface, points: list[tuple[int, int]], color: Color, thickness: int, antialias: bool, closed: bool):
    left = min(point[0] for point in points) - thickness//2
    right = max(point[0] for point in points) + thickness//2 +1
    top = min(point[1] for point in points) - thickness//2
    bottom = max(point[1] for point in points) + thickness//2 + 1
    rect = Rect(left, top, right - left, bottom - top)
    points = [[point[0] - left, point[1] - top] for point in points]
    return _cv_lines(surface, rect, points=points, color=color, thickness=thickness, antialias=antialias, closed=closed)