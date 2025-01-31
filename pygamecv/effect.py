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
    col_indices = np.where(arr.any(axis=1))[0]
    first_col = col_indices[0] if col_indices.size > 0 else None
    last_col = col_indices[-1] if col_indices.size > 0 else None
    
    # Find the first and last rows with at least one True
    row_indices = np.where(arr.any(axis=0))[0]
    first_row = row_indices[0] if row_indices.size > 0 else None
    last_row = row_indices[-1] if row_indices.size > 0 else None
    
    return first_col, last_col, first_row, last_row

def _make_factor_and_rect_from_mask(surface: Surface, factor: float | int | np.ndarray, max_factor_value: int) -> tuple[np.ndarray | None, Rect | None]:
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
        return np.clip(factor[left: right+1, top:bottom+1].swapaxes(0, 1), 0, max_factor_value), Rect(left, top, right - left+1, bottom - top+1)

@cv_transformation
def _cv_saturate(rgb_array: np.ndarray, factor: np.ndarray):
    """
    Saturate the colors of the image based on a matrix factor.

    Params:
    ----
    - rgb_array: numpy.ndarray, the array representing an image.
    - factor: numpy.ndarray, the array representing how much the saturation effect should be applied. All values should be between 0. and 1.
    """
    mask = factor.astype(bool)
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[:,:, 2][mask] = 255 - (255 - hls_array[:,:, 2][mask]) * (1 - factor[mask])
    rgb_array[:, :, :3][mask] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)[mask]

@cv_transformation
def _cv_desaturate(rgb_array: np.ndarray, factor: np.ndarray):
    """
    Desaturate the colors of the image based on a matrix factor.

    Params:
    ----
    - rgb_array: numpy.ndarray, the array representing an image.
    - factor: numpy.ndarray, the array representing how much the desaturation effect should be applied. All values should be between 0. and 1.
    """
    mask = factor.astype(bool)
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[:,:, 2][mask] = hls_array[:,:, 2][mask] * (1 - factor[mask])
    rgb_array[:, :, :3][mask] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)[mask]

@cv_transformation
def _cv_set_saturation(rgb_array: np.ndarray, value: np.ndarray, mask: np.ndarray | None = None):
    """
    Set the saturation of the colors of the image based on a matrix value.

    Params:
    ----
    - rgb_array: numpy.ndarray, the array representing an image.
    - value: numpy.ndarray, the array representing the new value of the hue. saturations are integers between 0 and 255
    - mask: numpy.ndarray of bool | None, if specified, the pixels outside of the mask will not be changed.
    """
    if mask is None:
        mask = np.full_like(value, True).astype(bool)
    else:
        mask = mask.swapaxes(0, 1)
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[:,:, 2][mask] = value[mask]
    rgb_array[:, :, :3][mask] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)[mask]

@cv_transformation
def _cv_lighten(rgb_array: np.ndarray, factor: np.ndarray):
    """
    Lighten the colors of the image based on a matrix factor.

    Params:
    ----
    - rgb_array: numpy.ndarray, the array representing an image.
    - factor: numpy.ndarray, the array representing how much the lightening effect should be applied. All values should be between 0. and 1.
    """
    mask = factor.astype(bool)
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[:,:, 1][mask] = 255 - (255 - hls_array[:,:, 1][mask]) * (1 - factor[mask])
    rgb_array[:, :, :3][mask] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)[mask]

@cv_transformation
def _cv_darken(rgb_array: np.ndarray, factor: np.ndarray):
    """
    Darken the colors of the image based on a matrix factor.

    Params:
    ----
    - rgb_array: numpy.ndarray, the array representing an image.
    - factor: numpy.ndarray, the array representing how much the darkening effect should be applied. All values should be between 0. and 1.
    """
    mask = factor.astype(bool)
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[:,:, 1][mask] = hls_array[:,:, 1][mask] * (1 - factor[mask])
    rgb_array[:, :, :3][mask] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)[mask]

@cv_transformation
def _cv_set_luminosity(rgb_array: np.ndarray, value: np.ndarray, mask: np.ndarray | None = None):
    """
    Set the luminosity of the colors of the image based on a matrix value.

    Params:
    ----
    - rgb_array: numpy.ndarray, the array representing an image.
    - value: numpy.ndarray, the array representing the new value of the hue. Luminosities are integers between 0 and 255
    """
    if mask is None:
        mask = np.full_like(value, True).astype(bool)
    else:
        mask = mask.swapaxes(0, 1)
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[:,:, 1][mask] = value[mask]
    rgb_array[:, :, :3][mask] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)[mask]

@cv_transformation
def _cv_shift_hue(rgb_array: np.ndarray, value: np.ndarray):
    """
    Shift the hue of the colors of the image based on a matrix factor.

    Params:
    ----
    - rgb_array: numpy.ndarray, the array representing an image.
    - value: numpy.ndarray, the array representing how much the shift effect should be applied. All hues are integers between 0° and 180°
    """
    mask = value.astype(bool)
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[mask, 0] = np.mod(hls_array[mask, 0] + value[mask], 180)
    rgb_array[mask, :3] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)[mask]

@cv_transformation
def _cv_set_hue(rgb_array: np.ndarray, value: np.ndarray, mask: np.ndarray | None = None):
    """
    Set the hue of the colors of the image based on a matrix value.

    Params:
    ----
    - rgb_array: numpy.ndarray, the array representing an image.
    - value: numpy.ndarray, the array representing the new value of the hue. Hues are integers between 0° and 180°
    """
    if mask is None:
        mask = np.full_like(value, True).astype(bool)
    else:
        mask = mask.swapaxes(0, 1)
    hls_array = cv.cvtColor(rgb_array, cv.COLOR_RGB2HLS)
    hls_array[mask, 0] = np.mod(value[mask], 180)
    rgb_array[mask, :3] = cv.cvtColor(hls_array, cv.COLOR_HLS2RGB)[mask]

def saturate(surface: Surface, factor: float | np.ndarray):
    """
    Saturate the colors of a pygame.Surface by a saturation factor.
    
    Params:
    ----
    - surface: pygame.Surface, the surface to modify.
    - factor: float | numpy.ndarray, the factor to use to saturate the surface.
    if factor is a float, all the surface is saturated by the same factor.
    if factor is a numpy.ndarray, it must have the same shape as the surface.
    In this case, each pixel will be saturated according to the factor.

    Raises:
    ----
    - ValueError("This factor has the wrong shape.") if the factor is a numpy.ndarray with a different shape than the surface.
    """
    factor, rect = _make_factor_and_rect_from_mask(surface, factor, 1)
    if not factor is None:
        _cv_saturate(surface, rect, factor=factor)

def desaturate(surface: Surface, factor: float | np.ndarray):
    """
    Desaturate the colors of a pygame.Surface by a desaturation factor.
    
    Params:
    ----
    - surface: pygame.Surface, the surface to modify.
    - factor: float | numpy.ndarray, the factor to use to desaturate the surface.
    if factor is a float, all the surface is desaturated by the same factor.
    if factor is a numpy.ndarray, it must have the same shape as the surface.
    In this case, each pixel will be desaturated according to the factor.
    
    Raises:
    ----
    - ValueError("This factor has the wrong shape.") if the factor is a numpy.ndarray with a different shape than the surface.
    """
    factor, rect = _make_factor_and_rect_from_mask(surface, factor, 1)
    if not factor is None:
        _cv_desaturate(surface, rect, factor=factor)

def set_saturation(surface: Surface, value: float | np.ndarray, mask: np.ndarray | None = None):
    """
    Set the saturation of the color of each pixel to a new value.
    
    Params:
    ----
    - surface: pygame.Surface, the surface to modify.
    - value: int | numpy.ndarray, the value used to set the surface's colors saturation.
    if value is a float, all the surface is set to the same value.
    if value is a numpy.ndarray, it must have the same shape as the surface.
    In this case, each pixel's saturation will be set according to the value.
    Saturations are integers between 0 and 255.
    - mask: numpy.ndarray of bool | None = None. If specified, only the pixels in the mask will be changed.

    Raises:
    ----
    - ValueError("This factor has the wrong shape.") if the factor is a numpy.ndarray with a different shape than the surface.
    - ValueError("This mask has the wrong shape") if the mask is a numpy.ndarray with a different shape than the surface
    """
    if isinstance(value, (float | int)):
        value = np.full(surface.get_size(), value)
    elif value.shape != surface.get_size():
        raise ValueError("This factor has the wrong shape.")
    elif not mask is None and mask.shape != surface.get_size():
        raise ValueError("This mask has the wrong shape")
    value = np.clip(value, 0, 255).astype(np.int8).swapaxes(0, 1)
    _cv_set_saturation(surface, None, value=value, mask=mask)

def lighten(surface: Surface, factor: float | np.ndarray):
    """
    Lighten the colors of a pygame.Surface by a lightening factor.
    
    Params:
    ----
    - surface: pygame.Surface, the surface to modify.
    - factor: float | numpy.ndarray, the factor to use to lighten the surface.
    if factor is a float, all the surface is lightened by the same factor.
    if factor is a numpy.ndarray, it must have the same shape as the surface.
    In this case, each pixel will be lightened according to the factor.

    Raises:
    ----
    - ValueError("This factor has the wrong shape.") if the factor is a numpy.ndarray with a different shape than the surface.
    """
    factor, rect = _make_factor_and_rect_from_mask(surface, factor, 1)
    if not factor is None:
        _cv_lighten(surface, rect, factor=factor)

def darken(surface: Surface, factor: float | np.ndarray):
    """
    Darken the colors of a pygame.Surface by a darkening factor.
    
    Params:
    ----
    - surface: pygame.Surface, the surface to modify.
    - factor: float | numpy.ndarray, the factor to use to darken the surface.
    if factor is a float, all the surface is darkened by the same factor.
    if factor is a numpy.ndarray, it must have the same shape as the surface.
    In this case, each pixel will be darkened according to the factor.

    Raises:
    ----
    - ValueError("This factor has the wrong shape.") if the factor is a numpy.ndarray with a different shape than the surface.
    """
    factor, rect = _make_factor_and_rect_from_mask(surface, factor, 1)
    if not factor is None:
         _cv_darken(surface, rect, factor=factor)

def set_luminosity(surface: Surface, value: float | np.ndarray, mask: np.ndarray | None = None):
    """
    Set the luminosity of the color of each pixel to a new value.
    
    Params:
    ----
    - surface: pygame.Surface, the surface to modify.
    - value: int | numpy.ndarray, the value used to set the surface's colors luminosity.
    if value is a float, all the surface is set to the same value.
    if value is a numpy.ndarray, it must have the same shape as the surface.
    In this case, each pixel's luminosity will be set according to the value.
    Luminosities are integers between 0 and 255.
    - mask: numpy.ndarray of bool | None = None. If specified, only the pixels in the mask will be changed.

    Raises:
    ----
    - ValueError("This factor has the wrong shape.") if the factor is a numpy.ndarray with a different shape than the surface.
    - ValueError("This mask has the wrong shape") if the mask is a numpy.ndarray with a different shape than the surface
    """
    if isinstance(value, (float | int)):
        value = np.full(surface.get_size(), value)
    elif value.shape != surface.get_size():
        raise ValueError("This factor has the wrong shape.")
    elif not mask is None and mask.shape != surface.get_size():
        raise ValueError("This mask has the wrong shape")
    value = np.clip(value, 0, 255).astype(np.int8).swapaxes(0, 1)
    _cv_set_luminosity(surface, None, value=value, mask=mask)

def shift_hue(surface: Surface, value: int | np.ndarray):
    """
    Shift the hue of the colors of a pygame.Surface by a value.
    
    Params:
    ----
    - surface: pygame.Surface, the surface to modify.
    - value: int | numpy.ndarray, the value used to shift the surface.
    if value is a float, all the surface is shifted by the same value.
    if value is a numpy.ndarray, it must have the same shape as the surface.
    In this case, each pixel will be shifted according to the value.
    Hues are integers between 0° and 180°
    """
    value, rect = _make_factor_and_rect_from_mask(surface, value, 180)
    if not value is None:
        _cv_shift_hue(surface, rect, value=value)

def set_hue(surface: Surface, value: int | np.ndarray, mask: np.ndarray | None = None):
    """
    Set the hue of the color of each pixel to a new value.
    
    Params:
    ----
    - surface: pygame.Surface, the surface to modify.
    - value: int | numpy.ndarray, the value used to set the surface's colors hue.
    if value is a float, all the surface is set to the same value.
    if value is a numpy.ndarray, it must have the same shape as the surface.
    In this case, each pixel's hue will be set according to the value.
    Hues are integers between 0° and 180°
    - mask: numpy.ndarray of bool | None = None. If specified, only the pixels in the mask will be changed.

    Raises:
    ----
    - ValueError("This factor has the wrong shape.") if the factor is a numpy.ndarray with a different shape than the surface.
    - ValueError("This mask has the wrong shape") if the mask is a numpy.ndarray with a different shape than the surface.
    """
    if isinstance(value, (float | int)):
        value = np.full(surface.get_size(), value)
    elif value.shape != surface.get_size():
        raise ValueError("This factor has the wrong shape.")
    elif not mask is None and mask.shape != surface.get_size():
        raise ValueError("This mask has the wrong shape")
    value = np.mod(value, 180).swapaxes(0, 1)
    _cv_set_hue(surface, None, value=value, mask=mask)
