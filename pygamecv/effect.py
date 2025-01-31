import cv2 as cv
from pygame import Surface, Rect
import numpy as np
from .common import cv_transformation

def _find_first_last_true_indices(arr: np.ndarray) -> tuple[int | None]:
    """
    Find the first and last indices of a non-zero value of a numpy array.
    
    Params:
    ----
    arr: np.ndarray, the array we explore.

    Returns:
    ----
    - first_col: int | None, the index of the first column containing at least one non-zero value.
    - last_col: int | None, the index of the last column containing at least one non-zero value.
    - first_row: int | None, the index of the first row containing at least one non-zero value.
    - last_row: int | None, the index of the last row containing at least one non-zero value.

    If all values inside the array are equal to 0, then each output is set to None.
    """

    # Find the first and last columns with at least one True
    col_indices = np.where(arr.any(axis=0))[0]
    first_col = col_indices[0] if col_indices.size > 0 else None
    last_col = col_indices[-1] if col_indices.size > 0 else None
    
    # Find the first and last rows with at least one True
    row_indices = np.where(arr.any(axis=1))[0]
    first_row = row_indices[0] if row_indices.size > 0 else None
    last_row = row_indices[-1] if row_indices.size > 0 else None
    
    return first_col, last_col, first_row, last_row

def _make_factor_and_rect_from_mask(surface: Surface, factor: float | int | np.ndarray) -> tuple[np.ndarray | None, Rect | None]:
    """
    Create a factor matrix and a Rect based on the mask. The Rect is the smallest Rect containing all non-zero values of the mask.

    Params:
    ----
    - surface: pygame.Surface, the surface is used to check the size of the mask and build the submask.
    It is the surface on which the effect will be applied.
    - factor: float | int | numpy.ndarray. The factor mask that will be applied to the surface later.
    If factor is a float or an int, the mask will be a constant matrix of the same shape than the surface.
    If factor is a numpy.ndarray, it must have the same shape than the surface. This array will be cropped
    to the smallest rectangle containing all non-zero values.

    Returns:
    ----
    - factor: numpy.ndarray | None, the matrix of factors. If None, the input factor was a matrix full of zero
    - rect: pygame.Rect | None, the rect to be used to subsurface the surface. If None, no subsurface will be done.

    Raises:
    ----
    - ValueError("This factor has the wrong shape.") if the factor is a numpy.ndarray with a different shape than the surface.
    """
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

@cv_transformation
def _cv_shift_hue(rgb_array: np.ndarray, factor: np.ndarray):
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[:,:, 0] = np.mod(hls_array[:,:, 0] + factor*180, 180)
    rgb_array[:, :, :3] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)

@cv_transformation
def _cv_set_hue(rgb_array: np.ndarray, value: np.ndarray):
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[:,:, 0] = np.mod(value, 180)
    rgb_array[:, :, :3] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)

def saturate(surface: Surface, factor: float | np.ndarray[float]):
    factor, rect = _make_factor_and_rect_from_mask(surface, factor)
    if factor is None:
        return surface
    else:
        return _cv_saturate(surface, rect, factor=factor)

def desaturate(surface: Surface, factor: float | np.ndarray[float]):
    factor, rect = _make_factor_and_rect_from_mask(surface, factor)
    if factor is None:
        return surface
    else:
        return _cv_desaturate(surface, rect, factor=factor)

def set_saturation(surface: Surface, value: float | np.ndarray):
    if isinstance(value, (float | int)):
        value = np.full(surface.get_size(), value)
    value = value.swapaxes(0, 1)*255
    return _cv_set_saturation(surface, None, value=value)

def lighten(surface: Surface, factor: float | np.ndarray[float]):
    factor, rect = _make_factor_and_rect_from_mask(surface, factor)
    if factor is None:
        return surface
    else:
        return _cv_lighten(surface, rect, factor=factor)

def darken(surface: Surface, factor: float | np.ndarray[float]):
    factor, rect = _make_factor_and_rect_from_mask(surface, factor)
    if factor is None:
        return surface
    else:
        return _cv_darken(surface, rect, factor=factor)

def set_luminosity(surface: Surface, value: float | np.ndarray):
    if isinstance(value, (float | int)):
        value = np.full(surface.get_size(), value)
    value = value.swapaxes(0, 1)*255
    return _cv_set_luminosity(surface, None, value=value)

def shift_hue(surface: Surface, factor: float | np.ndarray[float]):
    factor, rect = _make_factor_and_rect_from_mask(surface, factor)
    if factor is None:
        return surface
    else:
        return _cv_shift_hue(surface, rect, factor=factor)

def set_hue(surface: Surface, value: float | np.ndarray):
    if isinstance(value, (float | int)):
        value = np.full(surface.get_size(), value)
    value = value.swapaxes(0, 1)*180
    return _cv_set_hue(surface, None, value=value)
