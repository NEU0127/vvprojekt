# Projekt předmětu Vědecké Výpočty v Pythonu

Toto je repozitář pro odevzdávání projektu do předmětu Vědecké Výpočty v Pythonu.  
Autor: Filip Neumann a NEU0127.

Projekt se zaměřuje na vizualizaci fraktálů pomocí knihovny implementované v jazyce Python.

## 📁 Struktura projektu

- `lib/` – Knihovna s implementací
  - `mandelbrot.py` – generátor Mandelbrotovy množiny
  - `julia.py` – generátor Juliových množin
  - `vizualizace.py` – třída pro vizualizaci pomocí `matplotlib` (slider pro iterace, změna barev, zoom)
  
- `examples.ipynb` – Jupyter notebook s provedením vizualizace  
- `README.md` – Tento soubor s popisem projektu

## ⚙️ Funkcionalita

- Generování fraktálů (Mandelbrot, Julia) na základě zadaného rozsahu a rozlišení
- Nastavení maximálního počtu iterací
- Zoomování pomocí kolečka myši
- Slider pro nastavení počtu iterací
- Výběr barevného schématu zobrazení