# RoyGBiv

This python module is intended to provide a set of image analysis tools. This is very much a work in progress...

_by Giv Parvaneh_ 
- Demo: http://roygbiv.givp.org/

## Requirements

- Python 2.6+
- Python Imaging Library (PIL)
- NumPy
- ColorMath

Then ```pip install RoyGBiv```

## Usage

```python
>>> from roygbiv import *
>>> roy = Roygbiv('test.png')
>>> roy.get_average_hex()
'#468489'
>>> roy.get_average_rgb()
(70, 132, 137)
>>> roy.get_palette_rgb()
[(87, 145, 138), (52, 126, 140), (44, 97, 117), (154, 168, 145), (199, 194, 158)]
>>> roy.get_palette_hex()
['#57918a', '#347e8c', '#2c6175', '#9aa891', '#c7c29e']
```

## Available methods

- `get_average_hex()` return the average color in the image and return as a hex string
- `get_average_rgb()` return the average color in the image and return as RGB tuple
- `get_palette()` return a list of all prominent colors in the image with prominence weight value
- `get_palette_rgb()` return a list of all prominent colors in RGB
- `get_palette_hex()` return a list of all prominent colors in hex

## Credits

A lot of this code is borrowed from the most excellent [Colorific](https://github.com/99designs/colorific/ "Colorific") project but modified to work with Python 2.6 + other tweaks