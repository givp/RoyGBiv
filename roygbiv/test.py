from roygbiv import *

roy = Roygbiv('test.png')
assert roy.get_average_hex() == '#468489'
assert roy.get_average_rgb() == (70, 132, 137)
assert roy.get_palette_rgb() == [(87, 145, 138), (52, 126, 140), (44, 97, 117), (154, 168, 145), (199, 194, 158)]
assert roy.get_palette_hex() == ['#57918a', '#347e8c', '#2c6175', '#9aa891', '#c7c29e']

