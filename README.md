# RoyGBiv

This python module is intended to provide a set of image analysis tools. This is very much a work in progress...

_by Giv Parvaneh_

## Requirements

- Python 2.6+
- Python Imaging Library (PIL)
- NumPy
- ColorMath

## Usage

```python
>>> from roygbiv import *
>>> roy = Roygbiv('test.png')
>>> roy.get_average_hex()
'#468489'
>>> roy.get_average_rgb()
(70, 132, 137)
```

## Available methods

- `get_average_hex()` return the average color in the image and return as a hex string
- `get_average_rgb()` return the average color in the image and return as RGB tuple
- `get_colors()` return a list of all prominent colors in the image with prominence weight value
- `get_colors_rgb()` return a list of all prominent colors in RGB
- `get_colors_hex()` return a list of all prominent colors in hex