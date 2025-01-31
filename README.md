# **PygameCV**

**PygameCV** is a set of function allowing the a game developper using pygame to enhance its game by using cv's drawing functions and other effects to modify a Surface.

## Tutorial

### Importation

First thing first, ensure to have **PygameCV** installed on your python environement. For that, run the following command:

```bash
pip install pygame-cv
```

Then, import **PygameCV** with

```python
import pygamecv
```

### Drawing

You are now able to use pygamecv on your surfaces! For example, you might want to draw an ellipse, like that:

```python

    import pygame
    import pygamecv

    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    img = pygame.image.load("Lenna.png")
    pygamecv.ellipse(
        surface=img,
        center=(100, 200),
        radius_x=50,
        radius_y=40,
        color=(0, 255, 255),
        thickness=10, # This is pygame.draw's 'width' argument
        antialias=True,
        angle=0,
    )
    ... # The remaining of your game.

```

Which will output the following:

![Ellipse](images/ellipse.png)

You could also be tempted to draw a rectangle, but with some transparency, like this:

```python

    import pygame
    import pygamecv

    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    img = pygame.image.load("images/Lenna.png")
    pygamecv.rectangle(
        surface=img,
        rect=(200, 200, 150, 300),
        color=(0, 255, 255, 100),
        thickness=0
    )
    ... # The remaining of your game.

```

which will do the following modification:
![Rectangle](images/rectangle.png)

Finally, you can need to draw a rectangle with rounded, antialiased corners, like the following:

```python

    import pygame
    import pygamecv

    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    img = pygame.image.load("images/Lenna.png")
    pygamecv.rounded_rectangle(
        surface=img,
        rect=(200, 200, 150, 300),
        color=(0, 255, 255, 255),
        thickness=20,
        antialias=True,
        top_left=15, # angle of the top left corner and all other unspecified corners
        bottom_right=135,

    )
    ... # The remaining of your game.

```

which will look like that

![Rounded Rectangle](images/rounded_rectangle.png)

### Effect

That's cool, but what you really need it to apply some effect on the image. For example, you want to saturate it.

```python

    import pygame
    import pygamecv

    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    img = pygame.image.load("images/Lenna.png")
    pygamecv.saturate(
        surface=img,
        factor=1
    )
    ... # The remaining of your game.

```

Which will give you

![Saturation](images/saturation.png)

Great! But now you would like to shift the hue of the image, and to darken the image.

```python

    import pygame
    import pygamecv

    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    img = pygame.image.load("images/Lenna.png")
    pygamecv.shift_hue(
        surface=img,
        value=90
    )
    pygamecv.darken(
        surface=img,
        factor=0.5
    )
    ... # The remaining of your game.

```

whose result is
![Darken and shift hue](images/darken_shift_hue.png)

Alright alright, now you want to gradually darken the edges of the image. For that, we use a numpy array as factor and not a float.

```python

    import pygame
    import pygamecv
    import numpy as np

    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    img = pygame.image.load("images/Lenna.png")

    def gradient_factor(width, height, min_radius) -> np.ndarray:
        x_grid, y_grid = np.ogrid[:width, :height]
        dist_to_center = np.sqrt((x_grid - width/2 + 0.5)**2 + (y_grid - height/2 + 0.5)**2)
        unchanged = dist_to_center < min_radius
        max_radius = np.sqrt((width/2 - 0.5)**2 + (height/2-0.5)**2)
        factor = (dist_to_center - min_radius)/(max_radius - min_radius)
        factor[unchanged] = 0
        return factor

    factor=gradient_factor(*img.get_size(), min_radius=50)

    pygamecv.darken(
        surface=img,
        factor=factor
    )
    ... # The remaining of your game.

```

Which will give you this beautfiul vignette effect:
![Vignette](images/circle_darkened.png)

Finally, you decide that you need to set a value for the saturation of all pixels outside of a circle. Right, let's do it, using masks.

```python

    import pygame
    import pygamecv
    import numpy as np

    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    img = pygame.image.load("images/Lenna.png")

    def circle_mask(width, height, radius) -> np.ndarray:
        x_grid, y_grid = np.ogrid[:width, :height]
        dist_to_center = np.sqrt((x_grid - width/2 + 0.5)**2 + (y_grid - height/2 + 0.5)**2)
        return dist_to_center < radius
 
    mask = circle_mask(*img.get_size(), 100)

    pygamecv.set_saturation(
        surface=img,
        value=0,
        mask=mask
    )
    ... # The remaining of your game.

```

Which removes the color saturation of the center, like that:
![Saturation with mask](images/circle_saturation.png)

### Other needs

You are telling me that now, you what to other cv functions. For that, you will need to define your own function,
using the decorator ```pygamecv.common.cv_transformation```. This decorator transform a cv function
into a pygame surface transformation.

Here, _cv_your_function transforms in-place img.
The decorator turn it from an in-place array to array into an in-place surface-to-surface transformation, with a rect argument.
If the rect is specified, the array to be transformed is taken from a subsurface, extracted by the rect. Otherwise, it is from the whole surface. 
Then, you can define another function to call it. It is adviced to do so if you need to compute a rectangle from the input of the function, that's how it is done for circles or ellipses, for example.

```python

    import pygame
    import pygamecv
    import numpy as np

    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    img = pygame.image.load("images/Lenna.png")

    @pygamecv.cv_transformation
    def _cv_your_function(img: numpy.ndarray, **kwargs):
        ...
    
    def your_function(surface: pygame.Surface, **kwargs):
        rect = ...
        _cv_your_function(surface, rect, **kwargs)
    
    your_function(img, (11, 11), 20)

```

## Warning

Modify a Surface using cv may be long, as copying the value of the pixels needs to be done twice. For this purpose, restricting the array to the smallest Rect speeds up the computations. If you need to modify a big surface, it will take time.

## Contributing

Everyone is welcome to contribute to this project by proposing new features and optimizations! Your feedbacks will be appreciated.

## License

This project is licensed under a GNU GENERAL PUBLIC LICENSE, please refer to [the license file](LICENSE)

