import cv2 as cv
from pygame import Surface, Rect
import numpy as np
from .decorator import cv_transformation

def _find_first_last_true_indices(arr: np.ndarray):

    # Find the first and last columns with at least one True
    col_indices = np.where(arr.any(axis=0))[0]
    first_col = col_indices[0] if col_indices.size > 0 else None
    last_col = col_indices[-1] if col_indices.size > 0 else None
    
    # Find the first and last rows with at least one True
    row_indices = np.where(arr.any(axis=1))[0]
    first_row = row_indices[0] if row_indices.size > 0 else None
    last_row = row_indices[-1] if row_indices.size > 0 else None
    
    return first_col, last_col, first_row, last_row

def _make_rect_and_factor_from_mask(surface: Surface, factor: float | int | np.ndarray):
    if isinstance(factor, (float | int)):
        factor = np.full(surface.get_size(), factor).swapaxes(0, 1)
        return factor, None
    else:
        if factor.shape != surface.get_size():
            raise ValueError("This factor has the wrong shape.")
        left, right, top, bottom = _find_first_last_true_indices(factor)
        if any(edge is None for edge in [left, right, top, bottom]):
            return None, None
        return factor[left: right, top:bottom].swapaxes(0, 1), Rect(left, top, right - left, bottom - top)

@cv_transformation
def _cv_saturate(rgb_array: np.ndarray, factor: np.ndarray):
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[:,:, 2] = 255 - (255 - hls_array[:,:, 2]) * (1 - factor)
    rgb_array[:, :, :3] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)

@cv_transformation
def _cv_desaturate(rgb_array: np.ndarray, factor: np.ndarray):
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[:,:, 2] = hls_array[:,:, 2] * (1 - factor)
    rgb_array[:, :, :3] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)

@cv_transformation
def _cv_set_saturation(rgb_array: np.ndarray, value: np.ndarray):
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[:,:, 2] = value
    rgb_array[:, :, :3] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)

def saturate(surface: Surface, factor: float | np.ndarray[float]):
    factor, rect = _make_rect_and_factor_from_mask(surface, factor)
    if factor is None:
        return surface
    else:
        return _cv_saturate(surface, rect, factor=factor)

def desaturate(surface: Surface, factor: float | np.ndarray[float]):
    factor, rect = _make_rect_and_factor_from_mask(surface, factor)
    if factor is None:
        return surface
    else:
        return _cv_desaturate(surface, rect, factor=factor)

def set_saturation(surface: Surface, value: float | np.ndarray):
    if isinstance(value, (float | int)):
        value = np.full(surface.get_size(), value)
    value = value.swapaxes(0, 1)*255
    return _cv_set_saturation(surface, None, value=value)

@cv_transformation
def _cv_lighten(rgb_array: np.ndarray, factor: np.ndarray):
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[:,:, 1] = 255 - (255 - hls_array[:,:, 1]) * (1 - factor)
    rgb_array[:, :, :3] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)

@cv_transformation
def _cv_darken(rgb_array: np.ndarray, factor: np.ndarray):
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[:,:, 1] = hls_array[:,:, 1] * (1 - factor)
    rgb_array[:, :, :3] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)

@cv_transformation
def _cv_set_luminosity(rgb_array: np.ndarray, value: np.ndarray):
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[:,:, 1] = value
    rgb_array[:, :, :3] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)

def lighten(surface: Surface, factor: float | np.ndarray[float]):
    factor, rect = _make_rect_and_factor_from_mask(surface, factor)
    if factor is None:
        return surface
    else:
        return _cv_lighten(surface, rect, factor=factor)

def darken(surface: Surface, factor: float | np.ndarray[float]):
    factor, rect = _make_rect_and_factor_from_mask(surface, factor)
    if factor is None:
        return surface
    else:
        return _cv_darken(surface, rect, factor=factor)

def set_luminosity(surface: Surface, value: float | np.ndarray):
    if isinstance(value, (float | int)):
        value = np.full(surface.get_size(), value)
    value = value.swapaxes(0, 1)*255
    return _cv_set_luminosity(surface, None, value=value)
