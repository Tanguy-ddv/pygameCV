"""The decorator module contains the cv_transformation decorator, used to transform an in-place open-cv2 array transformation."""
from typing import Callable
from functools import wraps
import numpy as np
from pygame import Surface, surfarray as sa, pixelcopy, SRCALPHA, Rect

def make_surface_rgba(array: np.ndarray):
    """Returns a surface made from a [w, h, 4] numpy array with per-pixel alpha."""
    surface = Surface(array.shape[:2], SRCALPHA, 32) # Create a transparent surface with alpha channel
    pixelcopy.array_to_surface(surface, array[:, :, :3]) # set the rgb
    sa.pixels_alpha(surface)[:] = array[:, :, 3] # set the alpha
    return surface

def cv_transformation(func: Callable[[np.ndarray], None]):
    """Decorate a function to make it like a basic inplace surface transformation while it uses cv's format."""
    @wraps(func)
    def wrapper_cv(surface: Surface, rect: Rect = None, **kwargs):

        alpha = surface.get_alpha()

        if rect is None:
            subsurf = surface
        else:
            if not rect.colliderect(surface.get_rect()):
                return surface

            if surface.get_rect().contains(rect):
                subsurf = surface.subsurface(rect)
            
            else:
                subsurf = Surface(rect.size, 0 if alpha is None else SRCALPHA)
                subsurf.fill((0, 0, 0, 0))

                surface_rect = surface.get_rect()
                overlap_rect = rect.clip(surface_rect)

                target_position = overlap_rect.left - rect.left, overlap_rect.top - rect.top
                subsurf.blit(surface, target_position, overlap_rect)

        if alpha is None: # the image does not have any alpha channel.
            array_surf = (sa.pixels3d(subsurf)).swapaxes(1, 0)
            func(array_surf, **kwargs)
            new_surf = sa.make_surface(array_surf.swapaxes(1, 0))
        else:
            # Convert the surface in open cv's format, taking the alpha channel into account.
            subsurf = subsurf.convert_alpha()
            array_surf = np.dstack((sa.pixels3d(subsurf), sa.pixels_alpha(subsurf))).swapaxes(1, 0)
            # Call the function
            func(array_surf, **kwargs)
            # Convert it back using the alpha channel.
            new_surf = make_surface_rgba(array_surf.swapaxes(1, 0))

        if rect is None:
            return new_surf

        surface.blit(new_surf, rect)
        return surface
    
    return wrapper_cv