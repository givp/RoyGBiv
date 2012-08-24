from PIL import Image

class Roygbiv(object):

	__filename = None
	
	def __init__(self, filename=None):
		self.__filename = filename


	def __average_color(self):
		i = Image.open(self.__filename)
		h = i.histogram()

		# split into red, green, blue
		r = h[0:256]
		g = h[256:256*2]
		b = h[256*2: 256*3]

		# perform the weighted average of each channel:
		# the *index* is the channel value, and the *value* is its weight
		return (
			sum( i*w for i, w in enumerate(r) ) / sum(r),
			sum( i*w for i, w in enumerate(g) ) / sum(g),
			sum( i*w for i, w in enumerate(b) ) / sum(b)
		)

	def __rgb_to_hex(self, rgb):
	    """ convert an (R, G, B) tuple to #RRGGBB """
	    hexcolor = '#%02x%02x%02x' % rgb_tuple
	    return hexcolor

	def get_average(self, mode='hex'):
		if mode == 'hex':
			rgb = self.__average_color()
			return self.__rgb_to_hex(rgb)
		else:
			return self.__average_color()

