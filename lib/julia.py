import numpy as np
from numba import njit, prange

class Julia:
    """
    Třída pro generování Julia množiny

    vlastnosti:
        x_min
        x_max
        y_min
        y_max
        width (šířka obrazu)
        height (výška obrazu)
        max_iter (maximum iterací pro určení diverg bodu)
        c (komplexní konstanta)
    """

    def __init__(self, x_min: float, x_max: float, y_min: float, y_max: float,
                 width: int, height: int, max_iter: int, c: complex):
        """
        Inicializuje parametry generování Juliovy množiny
        """
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.width = width
        self.height = height
        self.max_iter = max_iter
        self.c = c

    def generate(self) -> np.ndarray:
        """
        generuje množinu jako 2D pole
        """
        return self._julia_calc(
            self.width, self.height,
            self.x_min, self.x_max,
            self.y_min, self.y_max,
            self.max_iter,
            self.c
        )
    @staticmethod
    @njit(parallel=True)
    def _julia_calc(width, height, x_min, x_max, y_min, y_max, max_iter, c):
        """
        metoda pro výpočet Juliovy množiny.
        """
        result = np.zeros((height, width), dtype=np.int32)
        for y in prange(height):
            zy = y_min + (y / height) * (y_max - y_min)
            for x in range(width):
                zx = x_min + (x / width) * (x_max - x_min)
                z = complex(zx, zy)
                iteration = 0
                while abs(z) <= 2 and iteration < max_iter:
                    z = z * z + c
                    iteration += 1
                result[y, x] = iteration
        return result