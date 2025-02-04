"""The art._drawing submodule contains functions to draw something on an Art."""
import math
from typing import Sequence
import numpy as np
from pygame import Surface, Color, Rect, draw
import cv2 as cv
from .common import cv_transformation

def _get_rotated_rect(original_rect: Rect, angle: int) -> Rect:
    """
    Create a Rect that would contain a rotated Rect.
    
    Params:
    ---
    - original_rect: pygame.Rect, the initial rect that will be rotated.
    - angle: int, the angle (in degrees) with which the original_rect will be rotated.

    Returns:
    ---
    - new_rect: pygame.Rect, the Rect that would contain the oringial rect rotated.
    """
    theta = math.radians(angle)

    w, h = original_rect.width, original_rect.height
    cx, cy = original_rect.center
    
    new_width = int(w * abs(math.cos(theta)) + h * abs(math.sin(theta)))
    new_height = int(h * abs(math.cos(theta)) + w * abs(math.sin(theta)))
    
    new_rect = Rect(0, 0, new_width, new_height)
    new_rect.center = (cx, cy)
    
    return new_rect

def _get_ellipse_rect(center: tuple[int, int], radius_x: int, radius_y: int, thickness: int, angle: int) -> Rect:
    """
    Compute the pygame.Rect in which will fit an ellipse.

    Params:
    ---
    - center: tuple[int, int], the center of the ellipse.
    - radius_x: int, the horizontal (before rotation) semi-major axis.
    - radius_y: int, the vertical (before rotation) semi-minor axis.
    - thickness: int, the thickness of the pencil, in pixel, drawing the ellipse.
    - angle: int, in degrees, the angle by which the axis-aligned ellipse will be rotated.

    Returns:
    -----
    rect: pygame.Rect, the smallest pygame.Rect containing the ellipse.
    """
    rect = Rect(center[0] - radius_x - thickness//2, center[1] - radius_y - thickness//2, 2*radius_x + thickness+1, 2*radius_y + thickness+1)
    if angle != 0:
        # Rotate the rect to fit the rotated ellipsis.
        rect = _get_rotated_rect(rect, angle)
    return rect

def _angle_to_cv_angles(start_angle: int, end_angle: int) -> tuple[int, int]:
    """Transform start and end angle from an anticlockwise drawing expectation to cv's expectaion."""
    if start_angle < end_angle:
        return start_angle, end_angle
    return end_angle, start_angle - 360

@cv_transformation
def _cv_circle(surf_array: np.ndarray, center: tuple[int, int], radius: int, color: Color, thickness: int, antialias):
    """
    Draw a circle on an array using cv.

    Params:
    ----
    - surf_array: numpy.ndarray, the array on which the circle is drawn.
    - center: tuple[int, int], the center of the circle on the array.
    - radius: int, the radius of the circle
    - color: pygame.Color, the color of the circle.
    - thickness: int, the thickness of the draw, following cv's rule.
    - antialias: bool, specify whether the drawing should use antialiased lines or not.
    """
    color = tuple(color)
    if len(color) == 3:
        color = (*color, 255)
    line_type = cv.LINE_AA if antialias else cv.LINE_8
    cv.circle(surf_array, center, radius, color, thickness, line_type, 0)

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
    """
    Draw an ellipse on an array using cv.

    Params:
    ----
    - surf_array: numpy.ndarray, the array on which the ellipse is drawn.
    - center: tuple[int, int], the center of the ellipse on the array.
    - radius_x: int, the horizontal (before rotation) semi-major axis.
    - radius_y: int, the vertical (before rotation) semi-minor axis.
    - angle: int, in degrees, the angle by which the axis-aligned ellipse will be rotated.
    - start_angle: int, in degrees, the angle to start the drawing of the arc.
    - end_angle: int, in degrees, the angle to start the drawing of the arc.
    - color: pygame.Color, the color of the ellipse.
    - thickness: int, the thickness of the draw, following cv's rule.
    - antialias: bool, specify whether the drawing should use antialiased lines or not.
    """
    color = tuple(color)
    if len(color) == 3:
        color = (*color, 255)
    line_type = cv.LINE_AA if antialias else cv.LINE_8
    cv.ellipse(surf_array, center, (radius_x, radius_y), angle, start_angle, end_angle, color, thickness, line_type, 0)

@cv_transformation
def _cv_line(
    surf_array: np.ndarray,
    p1: tuple[int, int],
    p2: tuple[int, int],
    color: Color,
    thickness: int,
    antialias: bool
):
    """
    Draw a line on an array using cv.

    Params:
    ----
    - surf_array: numpy.ndarray, the array on which the line is drawn.
    - p1: tuple[int, int], the position of the starting point of the line.
    - p2: tuple[int, int], the position of the ending point of the line.
    - color: pygame.Color, the color of the line.
    - thickness: int, the thickness of the draw, following cv's rule.
    - antialias: bool, specify whether the line should be antialiased or not.
    """
    color = tuple(color)
    if len(color) == 3:
        color = (*color, 255)    
    line_type = cv.LINE_AA if antialias else cv.LINE_8
    overlay = surf_array.copy()
    cv.line(surf_array, p1, p2, tuple(color), thickness, line_type, 0)
    if len(color) == 4:
        alpha = color[3]
        cv.addWeighted(surf_array, alpha/255, overlay, 1 - alpha/255, 0, surf_array)
    
@cv_transformation
def _cv_lines(
    surf_array: np.ndarray,
    points: Sequence[tuple[int, int]],
    color: Color,
    thickness: int,
    antialias: bool,
    closed: bool
):
    """
    Draw a series of lines on an array using cv. This is faster than calling line multiple times.

    Params:
    ----
    - surf_array: numpy.ndarray, the array on which the lines are drawn.
    - points: Sequence[tuple[int, int]], the succesive points to be link by a line.
    - color: pygame.Color, the color of the lines.
    - thickness: int, the thickness of the draw, following cv's rule.
    - antialias: bool, specify whether the lines should be antialiased or not.
    - closed: bool, if True, the first and last points will be linked by a lines.
    """
    color = tuple(color)
    if len(color) == 3:
        color = (*color, 255)
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

@cv_transformation
def _cv_polygon(
    surf_array: np.ndarray,
    points: list[tuple[int, int]],
    color: Color,
    antialias: bool,
):
    """
    Draw a polygon on an array using cv.

    Params:
    ----
    - surf_array: numpy.ndarray, the array on which the polygon is drawn.
    - points: Sequence[tuple[int, int]], the succesive vertices of the polygon.
    - color: pygame.Color, the color of the polygon.
    - thickness: int, the thickness of the draw, following cv's rule.
    - antialias: bool, specify whether the lines should be antialiased or not.
    """
    color = tuple(color)
    if len(color) == 3:
        color = (*color, 255)
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
    cv.fillPoly(padded_array, [points], color, line_type, 0, [0, 0])

    if len(color) == 4:
        alpha = color[3]
        cv.addWeighted(padded_array, alpha/255, overlay, 1 - alpha/255, 0, padded_array)
    surf_array[:, :, :] = padded_array[pad_left: padded_array.shape[0]-pad_right, pad_top: padded_array.shape[1] - pad_bottom]

@cv_transformation
def _cv_rectangle(
    surf_array: np.ndarray,
    color: Color,
    thickness: int
):
    """
    Draw a rectangle on the border of the array.

    Params:
    ----
    - surf_array: numpy.ndarray, the array on which the polygon is drawn.
    - color: pygame.Color, the color of the polygon.
    - thickness: int, the thickness of the rectangle.
    """
    color = tuple(color)
    if len(color) == 3:
        color = (*color, 255)
    rectangle = np.full(surf_array.shape, np.array(tuple(color)), dtype=np.uint8)
    if thickness != 0:
        innner_shape = surf_array.shape[0] - 2*thickness, surf_array.shape[1] - 2*thickness, surf_array.shape[2]
        rectangle[thickness:-thickness, thickness:-thickness] = np.full(innner_shape, np.zeros((len(color),)))
    cv.addWeighted(surf_array, 1 - color[3]/255, rectangle, color[3]/255, 0, surf_array)

@cv_transformation
def _cv_rounded_rectangle(
    surf_array: np.ndarray,
    color: Color,
    thickness: int,
    antialias: bool,
    top_left: int,
    top_right: int,
    bottom_left: int,
    bottom_right: int,
):
    """
    Draw a rectangle with rounded corners on the border of the array.

    Params:
    ----
    - surf_array: numpy.ndarray, the array on which the polygon is drawn.
    - color: pygame.Color, the color of the polygon.
    - thickness: int, the thickness of the rectangle.
    - antialias: bool, specify whether the lines should be antialiased or not.
    - top_left: the radius of the top left corner.
    - top_right: the radius of the top right corner.
    - bottom_left: the radius of the bottom left corner.
    - bottom_right: the radius of the bottom right corner.
    """
    delta = 6//(antialias+1)
    color = tuple(color)
    if len(color) == 3:
        color = (*color, 255)
    line_type = cv.LINE_AA if antialias else cv.LINE_8
    w, h, _ = surf_array.shape
    top_left_points = list(cv.ellipse2Poly((top_left + thickness//2, top_left + thickness//2), (top_left, top_left), 0, 180, 270, delta))
    top_right_points = list(cv.ellipse2Poly((h - top_right - thickness//2, top_right + thickness//2), (top_right, top_right), 0, 0, -90, delta))
    bottom_right_points = list(cv.ellipse2Poly((h - bottom_right - thickness//2, w - bottom_right - thickness//2), (bottom_right, bottom_right), 0, 0, 90, delta))
    bottom_left_points = list(cv.ellipse2Poly((bottom_left + thickness//2, w - bottom_left - thickness//2), (bottom_left, bottom_left), 0, 90, 180, delta))
    points = np.array(top_left_points + top_right_points + bottom_right_points + bottom_left_points)
    overlay = surf_array.copy()
    points = points.reshape((-1, 1, 2))  # Shape it into (n, 1, 2)
    if thickness:
        cv.polylines(surf_array, [points], True, color, thickness, line_type, 0)
    else:
        cv.fillPoly(surf_array, [points], color, line_type, 0, [0, 0])

    if len(color) == 4:
        alpha = color[3]
        cv.addWeighted(surf_array, alpha/255, overlay, 1 - alpha/255, 0, surf_array)

def circle(surface: Surface, center: tuple[int, int], radius: int, color: Color, thickness: int, antialias: bool):
    """
    Draw a circle on an pygame.Surface using cv.

    Params:
    ----
    - surface: pygame.Surface, the surface on which the circle is drawn.
    - center: tuple[int, int], the center of the circle on the surface.
    - radius: int, the radius of the circle
    - color: pygame.Color, the color of the circle.
    - thickness: int, the thickness of the draw. If thickness == 0, the circle is filled, else, it is a thick line.
    - antialias: bool, specify whether the drawing should use antialiased lines or not.
    """
    if radius <= 1:
        return
    color = Color(color)
    if (surface.get_alpha() is None or color.a == 255) and not antialias:
        draw.circle(surface, color, center, radius + thickness//2, thickness)
    else:
        color = tuple(color)
        rect = _get_ellipse_rect(center, radius, radius, thickness, 0)
        center = radius + thickness//2, radius + thickness//2
        _cv_circle(surface, rect=rect, center=center, radius=radius, color=color, thickness=thickness if thickness else -1, antialias=antialias)

def ellipse(surface: Surface, center: tuple[int, int], radius_x: int, radius_y: int, color: Color, thickness: int, antialias: bool, angle: int = 0):
    """
    Draw an ellipse on an pygame.Surface using cv.

    Params:
    ----
    - surface: pygame.Surface, the surface on which the ellipse is drawn.
    - center: tuple[int, int], the center of the ellipse on the surface.
    - radius_x: int, the horizontal (before rotation) semi-major axis.
    - radius_y: int, the vertical (before rotation) semi-minor axis.
    - color: pygame.Color, the color of the ellipse.
    - thickness: int, the thickness of the draw. If thickness == 0, the ellipse is filled, else, it is a thick line.
    - antialias: bool, specify whether the drawing should use antialiased lines or not.
    - angle: int, in degrees, the angle by which the axis-aligned ellipse will be rotated.
    """
    if radius_x <= 0 or radius_y <= 0:
        return
    color = Color(color)
    if (surface.get_alpha() is None or color.a == 255) and not antialias and angle%90 == 0:
        rect = _get_ellipse_rect(center, radius_x - thickness//2, radius_y - thickness//2, thickness, angle)
        draw.ellipse(surface, color, rect, thickness)
    else:
            
        rect = _get_ellipse_rect(center, radius_x, radius_y, thickness, angle)
        color = tuple(color)
        center = rect.width//2, rect.height//2
        _cv_ellipse(
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
    """
    Draw an arc following an ellipse on an pygame.Surface using cv.

    Params:
    ----
    - surface: pygame.Surface, the surface on which the arc is drawn.
    - center: tuple[int, int], the center of the elliptical arc on the surface.
    - radius_x: int, the horizontal (before rotation) semi-major axis of the ellipse.
    - radius_y: int, the vertical (before rotation) semi-minor axis of the ellipse.
    - color: pygame.Color, the color of the arc.
    - thickness: int, the thickness of the draw. If thickness == 0, the arc is filled like a pie, else, it is a thick line.
    - antialias: bool, specify whether the drawing should use antialiased lines or not.
    - angle: int, in degrees, the angle by which the axis-aligned ellipse will be rotated.
    - start_angle: int, in degrees, the angle to start drawing.
    - end_angle: int, in degress, the angle to stop drawing.
    The arc is drawn clockwise from start_angle to end_angle.
    """

    start_angle, end_angle = _angle_to_cv_angles(start_angle, end_angle)
    rect = _get_ellipse_rect(center, radius_x, radius_y, thickness, angle)
    color = tuple(color)
    center = rect.width//2, rect.height//2
    _cv_ellipse(
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
    """
    Draw a pie following an ellipse on an pygame.Surface using cv.
    A pie is an arc where the start and end points are linked to the center of the ellipse.

    Params:
    ----
    - surface: pygame.Surface, the surface on which the pie is drawn.
    - center: tuple[int, int], the center of the elliptical pie on the surface.
    - radius_x: int, the horizontal (before rotation) semi-major axis of the ellipse.
    - radius_y: int, the vertical (before rotation) semi-minor axis of the ellipse.
    - color: pygame.Color, the color of the pie.
    - thickness: int, the thickness of the draw. If thickness == 0, the pie is filled, else, it is a thick line.
    - antialias: bool, specify whether the drawing should use antialiased lines or not.
    - angle: int, in degrees, the angle by which the axis-aligned ellipse will be rotated.
    - start_angle: int, in degrees, the angle to start drawing.
    - end_angle: int, in degress, the angle to stop drawing.
    The pie's arc is drawn clockwise from start_angle to end_angle.
    """
    start_angle, end_angle = _angle_to_cv_angles(start_angle, end_angle)

    if thickness:
        delta = 6//(antialias+1)
        points = list(cv.ellipse2Poly(center, (radius_x, radius_y), angle, start_angle, end_angle, delta)) + [np.array(center).astype(np.int32)]
        _cv_lines(surface, points=points, color=color, thickness=thickness, antialias=antialias, closed=True)
    else:
        arc(surface, center, radius_x, radius_y, color, thickness, antialias, angle, start_angle, end_angle)

def line(surface: Surface, p1: tuple[int, int], p2: tuple[int, int], color: Color, thickness: int, antialias: bool):
    """
    Draw a line on a  pygame.Surface using cv.

    Params:
    ----
    - surface: pygame.Surface, the surface on which the line is drawn.
    - p1: tuple[int, int], the position of the starting point of the line.
    - p2: tuple[int, int], the position of the ending point of the line.
    - color: pygame.Color, the color of the line.
    - thickness: int, the thickness of the draw. If thickness == 0, nothing is drawn.
    - antialias: bool, specify whether the line should be antialiased or not.
    """
    if thickness <= 0:
        return
    left = min(p1[0], p2[0]) - thickness//2
    right = max(p1[0], p2[0]) + thickness//2 
    top = min(p1[1], p2[1]) - thickness//2
    bottom = max(p1[1], p2[1]) + thickness//2
    rect = Rect(left, top, right - left + 1, bottom - top + 1)
    p1 = p1[0] - left, p1[1] - top
    p2 = p2[0] - left, p2[1] - top
    _cv_line(surface, rect, p1 = p1, p2 = p2, color=color, thickness=thickness, antialias=antialias)

def lines(surface: Surface, points: list[tuple[int, int]], color: Color, thickness: int, antialias: bool, closed: bool):
    """
    Draw several lines on a pygame.Surface using cv. It is faster than drawing multiple lines one by one.

    Params:
    ----
    - surface: pygame.Surface, the surface on which the line is drawn.
    - points: Sequence[tuple[int, int]], the succesive points to be link by a line.
    - color: pygame.Color, the color of the line.
    - thickness: int, the thickness of the draw. If thickness == 0, nothing is drawn.
    - antialias: bool, specify whether the line should be antialiased or not.
    - closed: bool, if True, the first and last points are linked with a line.
    """
    left = min(point[0] for point in points) - thickness//2
    right = max(point[0] for point in points) + thickness//2
    top = min(point[1] for point in points) - thickness//2
    bottom = max(point[1] for point in points) + thickness//2
    rect = Rect(left, top, right - left + 1, bottom - top + 1)
    points = [[point[0] - left, point[1] - top] for point in points]
    _cv_lines(surface, rect, points=points, color=color, thickness=thickness, antialias=antialias, closed=closed)

def rectangle(surface: Surface, rect: Rect, color: Color, thickness: int):
    """
    Draw a rectangle on a pygame.Surface using cv.

    Params:
    ----
    - surface: pygame.Surface, the surface on which the line is drawn.
    - rect: pygame.Rect, the rectangle representing the center line of the drawing (the drawing is extended in case of thickness)
    - color: pygame.Color, the color of the line.
    - thickness: int, the thickness of the draw. If thickness == 0, the rectangle is filled, else, it is a thick line.
    - antialias: bool, specify whether the line should be antialiased or not.
    """
    color = Color(color)
    rect = Rect(rect)
    rect.left -= thickness//2
    rect.top -= thickness//2
    rect.width += thickness
    rect.height += thickness
    if (surface.get_alpha() is None or color.a == 255) and thickness == 0:
        surface.fill(color, rect)
    elif (surface.get_alpha() is None or color.a == 255):
        draw.rect(surface, color, rect, thickness)
    else:
        _cv_rectangle(surface, rect, color=color, thickness=thickness)

def rounded_rectangle(surface: Surface, rect: Rect, color: Color, thickness: int, antialias: bool, top_left: int, top_right: int = None, bottom_left: int = None, bottom_right: int = None,):
    """
    Draw a rectangle with rounded corners on a pygame.Surface using cv.

    Params:
    ----
    - surface: pygame.Surface, the surface on which the line is drawn.
    - rect: pygame.Rect, the rectangle representing the center line of the drawing (the drawing is extended in case of thickness)
    - color: pygame.Color, the color of the line.
    - thickness: int, the thickness of the draw. If thickness == 0, the rectangle is filled, else, it is a thick line.
    - antialias: bool, specify whether the line should be antialiased or not.
    - top_left: int, the radius of the top left corner.
    - top_right: int | None = None, the radius of the top right corner. If None, uses the same value as the top left corner.
    - bottom_left: int | None = None, the radius of the bottom left corner. If None, uses the same value as the top left corner.
    - bottom_right: int | None = None, the radius of the bottom right corner. If None, uses the same value as the top left corner.
    """
    color = Color(color)
    if top_right is None:
        top_right = top_left
    if bottom_right is None:
        bottom_right = top_left
    if bottom_left is None:
        bottom_left = top_left
    rect = Rect(rect)
    rect.left -= thickness//2
    rect.top -= thickness//2
    rect.width += thickness
    rect.height += thickness
    if any( # If one of these conditions is satisfied, then pygame draws a quarter of circle that would be outside of the final rounded rect
        # Think if top_right = bottom_left = 100, bottom_right = top_left = 0, and width = height = 100.
            top_right + top_left <= rect.width,
            bottom_left + bottom_right <= rect.width,
            top_right + bottom_right <= rect.height,
            top_left + bottom_left <= rect.height,
        ):
            raise ValueError(f"""
                The specified radii cannot be used to draw as the cumulated radii is above
                the width or height, got {top_right}, {top_left}, {bottom_right}, {bottom_left}
                for a size of {rect.width, rect.height}."""
        )

    if ((surface.get_alpha() is None or color.a == 255) # there is no alpha component in the drawing
        and (not antialias or top_right == top_left == bottom_right == bottom_left == 0) # and there is no antialias or we don't care about it
        and ( # If one of these conditions is satisfied, then pygame draws a quarter of circle that would be outside of the final rounded rect
        # Think if top_right = bottom_left = 100, bottom_right = top_left = 0, and width = height = 100.
            top_right + top_left <= rect.width//2
            and bottom_left + bottom_right <= rect.width//2
            and top_right + bottom_right <= rect.height//2
            and top_left + bottom_left <= rect.height//2
        )
        ):
        draw.rect(surface, color, rect, thickness, top_left, top_left, top_right, bottom_left, bottom_right)
    else:
        rect = Rect(rect)
        _cv_rounded_rectangle(surface, rect, color=color, thickness=thickness, antialias=antialias,
                                    top_left=top_left, top_right=top_right, bottom_left=bottom_left, bottom_right=bottom_right)

def polygon(surface: Surface, points: list[tuple[int, int]], color: Color, thickness: int, antialias: bool):
    """
    Draw a polygon on a pygame.Surface using cv.

    Params:
    ----
    - surface: pygame.Surface, the surface on which the line is drawn.
    - points: Sequence[tuple[int, int]], the succesive vertices of the polygon.
    - color: pygame.Color, the color of the line.
    - thickness: int, the thickness of the draw. If thickness == 0, the polygon is filled
    - antialias: bool, specify whether the line should be antialiased or not.
    - closed: bool, if True, the first and last points are linked with a line.
    """
    color = Color(color)    
    left = min(point[0] for point in points) - thickness//2
    right = max(point[0] for point in points) + thickness//2 +1
    top = min(point[1] for point in points) - thickness//2
    bottom = max(point[1] for point in points) + thickness//2 + 1
    rect = Rect(left, top, right - left, bottom - top)
    points = [[point[0] - left, point[1] - top] for point in points]
    if thickness:
        _cv_lines(surface, rect, points=points, color=color, thickness=thickness, antialias=antialias, closed=True)
    else:
        _cv_polygon(surface, rect, points=points, color=color, antialias=antialias)
