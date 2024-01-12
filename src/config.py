# Coordinates of the all the PATTERNS
#PATTERN 1
VERTICAL_CROSS = [[(40, 27), (40,284)], [(10, 56), (69, 56)], [(40, 164), (76, 164)]]
#PATTERN 2
BIG_RECTANGLE = [[(76, 130), (520, 130)], [(520, 130), (520, 430)], [(520, 430), (76, 430)], [(76, 430), (76, 130)]]
#PATTERN 3
BIG_CROSS = [[(76, 130),(520, 430)],[(520, 130),(76, 430)]]
#PATTERN 4
HORIZONTAL_MIDLINE = [[(76, 280), (520, 280)]]
#PATTERN 5
VERTICAL_MIDELINE = [[(300, 130), (300, 430)]]
#PATTERN 6
SMALL_RECTANGLE_CROSS = [[(76, 210), (190, 210)], [(190, 210), (190, 350)], [(190, 350), (76, 350)], [(76, 350), (76, 210)], [(76, 210), (190, 350)], [(190, 210), (76, 350)]]
#PATTERN 7
HORIZONTAL_SMALL_LINE = [[(76, 200), (176, 200)]]
#PATTERN 8
FOUR_PARALLEL_LINE = [[(125, 160), (300, 160)], [(168, 190), (300, 190)], [(215, 220), (300, 220)], [(260, 250), (300, 250)]]
#PATTERN 9
SMALL_TRIANGLE = [[(300, 22), (300, 130)], [(300, 130), (520, 130)], [(520, 130), (300, 22)]]
#PATTERN 10
VERTICAL_SMALL_LINE = [[(360, 130), (360, 235)]]
#PATTERN 11
CIRCLE = [[(468, 234, 35)],[(453, 223)], [(481, 223)]]
#PATTERN 12
FIVE_PARALLEL_LINE = [[(330, 340), (360, 291)], [(360, 360), (400, 311)], [(400, 380), (430, 331)], [(430, 400), (460, 351)], [(460, 420), (490, 371)]]
#PATTERN 13
RIGHT_JOIN_LINE = [[(520, 130), (666, 280)], [(666, 280), (520, 430)]]
#PATTERN 14
RHOMBUS = [[(666, 280), (688, 337)], [(688, 337), (666, 393)], [(666, 393), (644, 337)], [(644, 337), (666, 280)]]
#PATTERN 15
VERTICAL_RIGHT_LINE = [[(587, 192), (587, 364)]]
#PATTERN 16
HORIZENTAL_RIGHT_LINE = [[(520, 280), (666, 280)]]
#PATTERN 17
HORIZENTAL_CROSS = [[(196, 490), (480, 490)], [(300, 430), (300, 490)], [(450, 465), (450, 515)]]
#PATTERN 18
BOTTOM_RECTANGLE = [[(76, 430), (196, 430)], [(196, 430), (196, 550)], [(196, 550), (76, 550)], [(76, 550), (76, 430)], [(76, 430), (196, 550)]]

#ALL PATTERNS
PATTERNS = [BIG_RECTANGLE, BIG_CROSS, HORIZONTAL_MIDLINE, VERTICAL_MIDELINE,
            SMALL_RECTANGLE_CROSS, HORIZONTAL_SMALL_LINE, FOUR_PARALLEL_LINE, SMALL_TRIANGLE, VERTICAL_SMALL_LINE,
            CIRCLE, FIVE_PARALLEL_LINE, RIGHT_JOIN_LINE,  RHOMBUS,VERTICAL_RIGHT_LINE, HORIZENTAL_RIGHT_LINE,
            HORIZENTAL_CROSS, BOTTOM_RECTANGLE, VERTICAL_CROSS]
ID_PATTERN = {1: "big rectangle", 2: "big cross", 3:'horizontal midline', 4:'vertical midline',
              5:'small rectangle with cross', 6:'horizontal small line', 7:'four parallel lines',
              8:'small triangle', 9:'vertical small line', 10:'circle', 11:'five parallel lines',
              12:'right join lines', 13:'rhombus', 14: 'vertical right line', 15:'horizental right line',
               16:'bottom rectangle', 17:'horizental cross', 18:'vertical cross'}
IMAGE_WIDTH = 708
IMAGE_HEIGHT = 564
IMAGE_CHANNELS = 3
DPI = 72
PIXELS_3 = 3 / 25.4 * DPI #8.5
# PIXELS_3 = 6 / 25.4 * DPI
PIXELS_6 = PIXELS_3 * 2 #17
PIXELS_12 = PIXELS_3 * 4 #34
ROTATION_LIMIT = 5#3
MAX_NOISE_X = int (IMAGE_WIDTH * 0.01)
MAX_NOISE_Y = int (IMAGE_HEIGHT * 0.01)
#paras for big rectangle
BIGREC_WIDTH_HEIGHT_RATIO = [1.2, 1.8]
BIGRECHEIGHT_IMAGEHEIGHT_RATION = 300 / 564
BIG_CORNER_RANGE = {"X": [], "Y": []}
LOG_FILE = ''
POINTS_DIC = {"bigrec_up_left" : (80, 130), "bigrec_up_right": (520, 130), "bigrec_down_left" :(80, 430), "bigrec_down_right":(520, 430),
              "bigcross_up_left": (80, 130), "bigcross_up_right": (520, 130), "bigcross_down_left" :(80, 430), "bigcross_down_right":(520, 430),
              "bigcross_center": (300, 280),
              "hori_midline_left":(80, 280), "hori_midline_right":(520, 280),
              "vert_midline_up":(300, 130), "vert_midline_down":(300, 430),
              "right_triangle_tip": (666, 280),
              'bottom_rec_down_right': (196, 550)}
score_map = {1: "both correct", 2:"correct place", 3: "correct shape", 4:"both wrong"}

class PATTERN:
    VERTICAL_CROSS = 'vertical cross'
    # PATTERN 2
    BIG_RECTANGLE = 'big rectangle'
    # PATTERN 3
    BIG_CROSS = 'big cross'
    # PATTERN 4
    HORIZONTAL_MIDLINE = 'horizontal midline'
    # PATTERN 5
    VERTICAL_MIDELINE = 'vertical midline'
    # PATTERN 6
    SMALL_RECTANGLE_CROSS = 'small rectangle with cross'
    # PATTERN 7
    HORIZONTAL_SMALL_LINE = 'horizontal small line'
    # PATTERN 8
    FOUR_PARALLEL_LINE = 'four parallel lines'
    # PATTERN 9
    SMALL_TRIANGLE = 'small triangle'
    # PATTERN 10
    VERTICAL_SMALL_LINE = 'vertical small line'
    # PATTERN 11
    CIRCLE = 'circle'
    # PATTERN 12
    FIVE_PARALLEL_LINE = 'five parallel lines'
    # PATTERN 13
    RIGHT_JOIN_LINE = 'right join lines'
    # PATTERN 14
    RHOMBUS = 'rhombus'
    # PATTERN 15
    VERTICAL_RIGHT_LINE = 'vertical right line'
    # PATTERN 16
    HORIZENTAL_RIGHT_LINE = 'horizental right line'
    # PATTERN 17
    HORIZENTAL_CROSS =  'horizental cross'
    # PATTERN 18
    BOTTOM_RECTANGLE = 'bottom rectangle'

