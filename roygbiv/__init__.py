import PIL
import PIL.JpegImagePlugin
from PIL import Image
from PIL import ImageChops
from collections import namedtuple
from Counter import Counter
from operator import itemgetter, mul, attrgetter
from colormath.color_objects import RGBColor
import colorsys

Color = namedtuple('Color', ['value', 'prominence'])
Palette = namedtuple('Palette', 'colors bgcolor')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# algorithm tuning
N_QUANTIZED = 100       # start with an adaptive palette of this size
MIN_DISTANCE = 10.0     # min distance to consider two colors different
MIN_PROMINENCE = 0.01   # ignore if less than this proportion of image
MIN_SATURATION = 0.05   # ignore if not saturated enough
MAX_COLORS = 5          # keep only this many colors
BACKGROUND_PROMINENCE = 0.5     # level of prominence indicating a bg color

# multiprocessing parameters
BLOCK_SIZE = 10
N_PROCESSES = 1
SENTINEL = 'no more to process'

class Roygbiv(object):

    __img = None

    def __init__(self, img_or_filename):
        if not img_or_filename:
            raise Exception('Must provide filename in constructor')

        if isinstance(img_or_filename, PIL.JpegImagePlugin.JpegImageFile):
            self.__img = img_or_filename
        else:
            self.__img = Image.open(img_or_filename)

        # make sure image is RGB
        if self.__img.mode != 'RGB':
            self.__img = self.__img.convert('RGB')

        # remove borders
        self.__img = self.__autocrop()

    def __extract_colors(self, min_saturation=MIN_SATURATION,
        min_distance=MIN_DISTANCE, max_colors=MAX_COLORS,
        min_prominence=MIN_PROMINENCE, n_quantized=N_QUANTIZED):
        """
        Determine what the major colors are in the given image.
        """

        # get point color count
        im = self.__img
        im = im.convert('P', palette=Image.ADAPTIVE, colors=n_quantized).convert('RGB')
        data = im.getdata()
        dist = Counter(data)
        n_pixels = mul(*im.size)

        # aggregate colors
        to_canonical = {WHITE: WHITE, BLACK: BLACK}
        aggregated = Counter({WHITE: 0, BLACK: 0})
        sorted_cols = sorted(dist.iteritems(), key=itemgetter(1), reverse=True)
        for c, n in sorted_cols:
            if c in aggregated:
                # exact match!
                aggregated[c] += n
            else:
                d, nearest = min((self.__distance(c, alt), alt) for alt in aggregated)
                if d < min_distance:
                    # nearby match
                    aggregated[nearest] += n
                    to_canonical[c] = nearest
                else:
                    # no nearby match
                    aggregated[c] = n
                    to_canonical[c] = c

        # order by prominence
        colors = sorted((Color(c, n / float(n_pixels)) \
                    for (c, n) in aggregated.iteritems()),
                key=attrgetter('prominence'),
                reverse=True)

        colors, bg_color = self.__detect_background(im, colors, to_canonical)

        # keep any color which meets the minimum saturation
        sat_colors = [c for c in colors if self.__meets_min_saturation(c, min_saturation)]
        if bg_color and not self.__meets_min_saturation(bg_color, min_saturation):
            bg_color = None
        if sat_colors:
            colors = sat_colors
        else:
            # keep at least one color
            colors = colors[:1]

        # keep any color within 10% of the majority color
        colors = [c for c in colors if c.prominence >= colors[0].prominence
                * min_prominence][:max_colors]

        return Palette(colors, bg_color)

    def __autocrop(self):
        "Crop away a border of the given background color."
        bg = Image.new("RGB", self.__img.size, WHITE)
        diff = ImageChops.difference(self.__img, bg)
        bbox = diff.getbbox()
        if bbox:
            return self.__img.crop(bbox)

        return self.__img # no contents, don't crop to nothing

    def __distance(self, c1, c2):
        "Calculate the visual distance between the two colors."
        return RGBColor(*c1).delta_e(RGBColor(*c2), method='cmc')

    def __meets_min_saturation(self, c, threshold):
        return colorsys.rgb_to_hsv(*self.__norm_color(c.value))[1] > threshold

    def __norm_color(self, c):
        r, g, b = c
        return (r/255.0, g/255.0, b/255.0)

    def __detect_background(self, im, colors, to_canonical):
        # more then half the image means background
        if colors[0].prominence >= BACKGROUND_PROMINENCE:
            return colors[1:], colors[0]

        # work out the background color
        w, h = im.size
        points = [(0, 0), (0, h/2), (0, h-1), (w/2, h-1), (w-1, h-1),
                (w-1, h/2), (w-1, 0), (w/2, 0)]
        edge_dist = Counter(im.getpixel(p) for p in points)

        (majority_col, majority_count), = edge_dist.most_common(1)
        if majority_count >= 3:
            # we have a background color
            canonical_bg = to_canonical[majority_col]
            bg_color, = [c for c in colors if c.value == canonical_bg]
            colors = [c for c in colors if c.value != canonical_bg]
        else:
            # no background color
            bg_color = None

        return colors, bg_color


    def __average_color(self):
        """ determine the average RGB color in image """
        h = self.__img.histogram()

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
        hexcolor = '#%02x%02x%02x' % rgb
        return hexcolor

    def get_palette(self):
        palette = self.__extract_colors()

        return palette

        '''
        print '%s\t%s\t%s' % (
            ','.join(rgb_to_hex(c.value) for c in palette.colors),
            palette.bgcolor and rgb_to_hex(palette.bgcolor.value) or '',
        )
        '''

    def get_palette_rgb(self):
        palette = self.get_palette()

        out = []
        for p in palette.colors:
            out.append(p.value)

        return out

    def get_palette_hex(self):
        palette = self.get_palette_rgb()

        out = []
        for p in palette:
            out.append(self.__rgb_to_hex(p))

        return out

    def get_average_hex(self):
        """ return average hex color in image """
        rgb = self.__average_color()
        return self.__rgb_to_hex(rgb)

    def get_average_rgb(self):
        """ return average RGB color in image """
        return self.__average_color()

