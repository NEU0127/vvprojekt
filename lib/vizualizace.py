import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
import numpy as np

class Fraktal:
    """
    Třída pro vizualizování fraktálů

    vlastnosti
        fraktal (generuje data fraktálu pomocí generate)
        cmap (barva)
        data (počet iterací)
        ax osa
        img
        slider_iter (Slider pro pohyb s max iteracemi)
        radio (tlačítka pro změnu barvy)
    """

    def __init__(self, fraktal_obj, cmap: str = "hot"):
        """
        Inicializuje vizualizaci fraktálu.
        """
        self.fraktal = fraktal_obj
        self.cmap = cmap
        self.data = self.fraktal.generate()
        
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.1, bottom=0.25, right=0.85)
        
        self.img = self.ax.imshow(
            self.data,
            cmap=self.cmap,
            extent=(self.fraktal.x_min, self.fraktal.x_max, self.fraktal.y_min, self.fraktal.y_max)
        )
        self.ax.set_title("vizualizace")
        self.ax.set_xlabel("Re")
        self.ax.set_ylabel("Im")
        self.fig.colorbar(self.img, ax=self.ax, label="Počet iterací")
        """ slider pro pohyb s max iteracemi """
        ax_iter = plt.axes([0.15, 0.1, 0.55, 0.03])
        self.slider_iter = Slider(
            ax_iter, "Max iterací",
            valmin=10, valmax=1000,
            valinit=self.fraktal.max_iter,
            valstep=10
        )
        self.slider_iter.on_changed(self.update_iter)

        """"tlačítka pro změnu barvy"""
        ax_radio = plt.axes([0.88, 0.3, 0.1, 0.2])
        self.radio = RadioButtons(ax_radio, ('hot', 'plasma', 'inferno', 'viridis', 'magma'))
        self.radio.on_clicked(self.update_cmap)

        """zoomování pomocí myši"""
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)

        plt.show()

    def update_iter(self, val):
        """volání slideru"""
        self.fraktal.max_iter = int(val)
        self._redraw()

    def update_cmap(self, label):
        """volání změny barvy"""
        self.cmap = label
        self.img.set_cmap(self.cmap)
        self.fig.canvas.draw_idle()

    def on_scroll(self, event):
        """volání zoomování"""
        base_scale = 1.2
        if event.button == 'up':
            scale_factor = 1 / base_scale
        elif event.button == 'down':
            scale_factor = base_scale
        else:
            return

        xdata = event.xdata
        ydata = event.ydata
        if xdata is None or ydata is None:
            return

        x_min, x_max = self.fraktal.x_min, self.fraktal.x_max
        y_min, y_max = self.fraktal.y_min, self.fraktal.y_max

        new_width = (x_max - x_min) * scale_factor
        new_height = (y_max - y_min) * scale_factor

        new_x_min = xdata - (xdata - x_min) * scale_factor
        new_x_max = xdata + (x_max - xdata) * scale_factor
        new_y_min = ydata - (ydata - y_min) * scale_factor
        new_y_max = ydata + (y_max - ydata) * scale_factor

        self.fraktal.x_min = new_x_min
        self.fraktal.x_max = new_x_max
        self.fraktal.y_min = new_y_min
        self.fraktal.y_max = new_y_max

        self._redraw()

    def _redraw(self):
        """
        překresluje
        """
        self.data = self.fraktal.generate()
        self.img.set_data(self.data)
        self.img.set_extent((self.fraktal.x_min, self.fraktal.x_max,
                             self.fraktal.y_min, self.fraktal.y_max))
        self.img.set_clim(0, self.fraktal.max_iter)
        self.fig.canvas.draw_idle()

