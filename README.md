# RoyGBiv

This python module is intended to provide a set of image analysis tools. This is very much a work in progress...

_by Giv Parvaneh_

## Requirements

Python 2.6+

PIL (Python Imaging Library) http://www.pythonware.com/products/pil/

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

- `get_average_hex()` return the average color in the image and return as a hexidecimal string

- `get_avaerage_rgb()` return the average color in the image and return as RGB tuple