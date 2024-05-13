import argparse
import time, os, serial
from PIL import Image, ImageDraw, ImageFont
from rgbmatrix import RGBMatrix, RGBMatrixOptions

parser = argparse.ArgumentParser(description='Something Something')
parser.add_argument('--text', type=str, default='Hello World')
parser.add_argument('--R', type=int, default=63)
parser.add_argument('--G', type=int, default=63)
parser.add_argument('--B', type=int, default=255)
args = parser.parse_args()


color_R = max(0, min(args.R, 255))
color_G = max(0, min(args.G, 255))
color_B = max(0, min(args.B, 255))

Noto_Serif = '/usr/local/src/fonter/Noto_Serif/NotoSerif-Italic-VariableFont_wdth,wght.ttf'#Noto_Sans/static/NotoSans-Black.ttf
Noto_Sans = '/usr/local/src/fonter/Noto_Sans/static/NotoSans-Black.ttf'

if os.path.exists(Noto_Sans) == False:
    print('Could not find path to fonts')
if os.path.exists(Noto_Serif) == False:
    print('Could not find path to fonts')

img_width = 64 * 2 * 2
options = RGBMatrixOptions()
options.cols = 64
options.rows = 32
options.chain_length =  2 # No. of screens
options.parallel = 1
options.gpio_slowdown =  4
options.show_refresh_rate = 1
options.hardware_mapping = 'regular'  #the hat
matrix = RGBMatrix(options = options)
offscreen_canvas = matrix.CreateFrameCanvas()

#Declaration of variables
xpos = 0
score = 0
time_left = 60

highest_score = 0
second_highest_score = 0
third_highest_score = 0
int_highscore = 0

highest_score_str		 = '0'
second_highest_score_str = '0'
third_highest_score_str  = '0'
table_of_highscores = [0,0,0]

#Connect to pico
ser = serial.Serial('/dev/ttyACM0',9600, timeout=30)
ser.flushInput()
time.sleep(0.01)
	
def image_draw (string_to_print):
	global highest_score, second_highest_score,third_highest_score, highest_score_str, second_highest_score_str, third_highest_score_str

	image = Image.new('RGB', (img_width, 64),(0, 0, 0))
	draw = ImageDraw.Draw(image)
	
	if string_to_print[0] == '-': # Check if game is over by checking if pico sent over a minus sign in the begynging, call the highscore function
		string_to_print = string_to_print[1:] # Remove game_over sign (-)
		is_high_score = string_to_print.partition('|')[0]
		int_highscore = int(is_high_score)
		for i in range(3):
			if int_highscore > table_of_highscores[i]:
				table_of_highscores.pop() #remove last
				table_of_highscores.insert(i,int_highscore) # insert at i:th place
				break


	font = ImageFont.truetype(Noto_Sans, 17)

	draw.text((2,10), string_to_print.partition('|')[0].rjust(3, "0"),font=font, fill=(0,0,255,0))
	draw.text((31,9), '|',font=font, fill=(0,0,255,0))
	draw.text((40,10), string_to_print.partition('|')[2].rjust(4, "0"),font=font, fill=(0,0,255,0))

	font = ImageFont.truetype(Noto_Sans, 15)
	draw.text((0,-5), '____________________',font=font, fill=(0,255,0,0))
	
	font = ImageFont.truetype(Noto_Sans, 10)
	draw.text((1,0), 'SCORE|TIME',font=font, fill=(255,0,0,0))

	
	draw.text((65,0), 'HIGHSCORE',font=font, fill=(255,0,0,0))
	draw.text((65,16), str(table_of_highscores[0]).rjust(3,"0") + '|' + str(table_of_highscores[1]).rjust(3,"0") + '|' + str(table_of_highscores[2]).rjust(3,"0"),font=font, fill=(0,0,255,0))

	
	return (image)

def print_text(string_to_print):
	global xpos, offscreen_canvas
	image = image_draw(string_to_print)
	
	if (img_width > 256):
		xpos += 1    
	if (xpos > img_width):
		xpos = 0

	offscreen_canvas.SetImage(image, -xpos)
	offscreen_canvas.SetImage(image, -xpos + img_width)

	offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
	time.sleep(0.01)

def get_text():
	string_to_print = ser.readline().decode('utf-8')
	return(str(string_to_print))
	
while True:
	string_to_print = get_text()
	print_text(string_to_print)
