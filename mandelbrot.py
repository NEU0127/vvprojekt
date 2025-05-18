import numpy as np
from numba import jit

class Mandelbrot:
    """
    Třída generujicí mandelbrot množiny

    vlastnosti:
        x_min
        x_max
        y_min
        y_max
        width (šířka obrazu)
        height (výška obrazu)
        max_iter (maximum iterací pro určení diverg bodu)
    """

    def __init__(self, x_min: float, x_max: float, y_min: float, y_max: float,
                 width: int, height: int, max_iter: int):
        """
Inicializuje parametry generování Mandelbrotovy množiny
"""
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.width = width
        self.height = height
        self.max_iter = max_iter

    @staticmethod
    @jit(nopython=True)
    def _mandelbrot_calc(width, height, x_min, x_max, y_min, y_max, max_iter):
        """
        metoda pro výpočet Mandelbrotovy množiny
        """
        result = np.zeros((height, width), dtype=np.int32)
        for y in range(height):
            cy = y_min + (y / height) * (y_max - y_min)
            for x in range(width):
                cx = x_min + (x / width) * (x_max - x_min)
                z = 0 + 0j
                c = complex(cx, cy)
                iteration = 0
                while abs(z) <= 2 and iteration < max_iter:
                    z = z*z + c
                    iteration += 1
                result[y, x] = iteration
        return result

    def generate(self) -> np.ndarray:
        """
        generuje množinu jako 2D pole
        """
        return self._mandelbrot_calc(
            self.width, self.height,
            self.x_min, self.x_max,
            self.y_min, self.y_max,
            self.max_iter
        )

