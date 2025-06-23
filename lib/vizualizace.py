import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from lib.julia import Julia
from lib.mandelbrot import Mandelbrot

class Fraktal:
    """
    Třída pro vizualizování fraktálů

    vlastnosti
        fraktal_obj : objekt Mandelbrot nebo Julia
        fraktal_type : 'Julia' nebo 'Mandelbrot'
        c_real, c_imag : reálná a imaginární část konstanty c u Julia
        colormap : barevné schéma
        fig, ax : hlavní figura a osa
        slider_iter : slider pro nastavení maximálního počtu iterací
        slider_creal, slider_cimag : slidery pro parametry c u Julia
        radio_color : radio tlačítka pro volbu barevné mapy
        button_zoom_in, button_zoom_out : tlačítka pro zoomování
    """
    def __init__(self, fraktal_obj):
        """Inicializace vizualizace fraktálu"""
        self.fraktal_obj = fraktal_obj
        self.fraktal_type = 'Julia' if isinstance(fraktal_obj, Julia) else 'Mandelbrot'
        self.c_real = fraktal_obj.c.real if self.fraktal_type == 'Julia' else -0.8
        self.c_imag = fraktal_obj.c.imag if self.fraktal_type == 'Julia' else 0.156
        self.colormap = 'hot'
        self.create_figure()

    def create_figure(self):
        """vytvoření obrazce"""
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.25, bottom=0.35)
        self.update_fractal()

        # Slider pro iterace
        ax_iter = plt.axes([0.25, 0.25, 0.65, 0.03])
        self.slider_iter = Slider(ax_iter, 'Iterace', 50, 1000, valinit=self.fraktal_obj.max_iter, valstep=10)
        self.slider_iter.on_changed(self.update_from_sliders)

        # Slidery pro c
        if self.fraktal_type == 'Julia':
            ax_creal = plt.axes([0.25, 0.20, 0.65, 0.03])
            self.slider_creal = Slider(ax_creal, 'Re(c)', -1.5, 1.5, valinit=self.c_real, valstep=0.01)
            self.slider_creal.on_changed(self.update_from_sliders)

            ax_cimag = plt.axes([0.25, 0.15, 0.65, 0.03])
            self.slider_cimag = Slider(ax_cimag, 'Im(c)', -1.5, 1.5, valinit=self.c_imag, valstep=0.01)
            self.slider_cimag.on_changed(self.update_from_sliders)

        # tlačítka pro volbu barvy
        ax_color = plt.axes([0.88, 0.3, 0.1, 0.2])
        self.radio_color = RadioButtons(ax_color, ('hot', 'plasma', 'inferno', 'viridis', 'magma'))
        self.radio_color.on_clicked(self.update_colormap)

        # Zoom tlačítka
        ax_zoom_in = plt.axes([0.025, 0.3, 0.1, 0.04])
        self.button_zoom_in = Button(ax_zoom_in, 'Zoom +')
        self.button_zoom_in.on_clicked(self.zoom_in)

        ax_zoom_out = plt.axes([0.025, 0.25, 0.1, 0.04])
        self.button_zoom_out = Button(ax_zoom_out, 'Zoom -')
        self.button_zoom_out.on_clicked(self.zoom_out)

        plt.show()

    def update_fractal(self):
        """Překreslení po změně c"""
        if self.fraktal_type == 'Julia':
            self.fraktal_obj.c = complex(self.c_real, self.c_imag)
        data = self.fraktal_obj.generate()
        self.ax.clear()
        self.im = self.ax.imshow(
            data, cmap=self.colormap,
            extent=[self.fraktal_obj.x_min, self.fraktal_obj.x_max,
                    self.fraktal_obj.y_min, self.fraktal_obj.y_max]
        )
        self.ax.set_title(f'{self.fraktal_type} Set')
        self.ax.set_xlabel("Re")
        self.ax.set_ylabel("Im")
        self.fig.canvas.draw_idle()

    def update_from_sliders(self, val):
        """aktualizace parametrů"""
        self.fraktal_obj.max_iter = int(self.slider_iter.val)
        if self.fraktal_type == 'Julia':
            self.c_real = self.slider_creal.val
            self.c_imag = self.slider_cimag.val
        self.update_fractal()

    def update_colormap(self, label):
        """aktualizace barvy"""
        self.colormap = label
        self.update_fractal()

    def zoom_in(self, event):
        """přiblížení"""
        self.zoom(factor=1)

    def zoom_out(self, event):
        """oddálení"""
        self.zoom(factor=1)

    def zoom(self, factor):
        """funkce pro zoom out a zoom in"""
        x_center = (self.fraktal_obj.x_min + self.fraktal_obj.x_max) / 2
        y_center = (self.fraktal_obj.y_min + self.fraktal_obj.y_max) / 2
        x_range = (self.fraktal_obj.x_max - self.fraktal_obj.x_min) * factor / 2
        y_range = (self.fraktal_obj.y_max - self.fraktal_obj.y_min) * factor / 2
        self.fraktal_obj.x_min = x_center - x_range
        self.fraktal_obj.x_max = x_center + x_range
        self.fraktal_obj.y_min = y_center - y_range
        self.fraktal_obj.y_max = y_center + y_range
        self.update_fractal()