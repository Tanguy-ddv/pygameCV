
from typing import Callable
from functools import wraps
import numpy as np
from pygame import Surface, surfarray as sa, image, pixelcopy, SRCALPHA, Rect, draw
from .common import make_surface_rgba


def cv_transformation(func: Callable[[np.ndarray], None]):
    """Decorate a function to make it like a basic inplace surface transformation while it uses cv's format."""
    @wraps(func)
    def wrapper_cv(surface: Surface, rect: Rect = None, **kwargs):

        if rect is None:
            subsurf = surface
        else:
            subsurf = surface.subsurface(rect.clip(surface.get_rect()))
        
        if surface.get_alpha() is None: # the image does not have any alpha channel.
            array_surf = np.ascontiguousarray((sa.pixels3d(subsurf)).swapaxes(1, 0))
            func(array_surf, **kwargs)
            new_surf = sa.make_surface(array_surf.swapaxes(1, 0))
        else:
            # Convert the surface in open cv's format, taking the alpha channel into account.
            array_surf = np.ascontiguousarray(np.dstack((sa.pixels3d(subsurf), sa.pixels_alpha(subsurf))).swapaxes(1, 0))
            # Call the function
            func(array_surf, **kwargs)
            # Convert it back using the alpha channel.
            new_surf = make_surface_rgba(array_surf.swapaxes(1, 0))

        if rect is None:
            return new_surf
        
        surface.blit(new_surf, rect)
        return surface
    
    return wrapper_cv