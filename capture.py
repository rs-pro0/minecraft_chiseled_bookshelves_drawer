#idea and some code was taken from https://github.com/kasamikona/BadAppleBookshelf/

from PIL import Image
from mcrcon import MCRcon
import numpy as np
import cv2, pyautogui, copy
from mss import mss


capture_resolution = [640,480]
blocks_x = 16*3
blocks_y = 12*3

origin_x = 0
origin_y = 90
origin_z = 0

view_distance = 8.7 

startbits = 0
endbits = 0
startdelay = 20
blockbits_last = [[startbits]*blocks_y for x in range(blocks_x)]
sct = mss()
input("Top left")
tl=pyautogui.position()
input("Bottom right")
br=pyautogui.position()
bounding_box={"top":tl.y,"left":tl.x,"width":br.x-tl.x,"height":br.y-tl.y}
width = bounding_box["width"]
height = bounding_box["height"]
emptybits=[[0]*blocks_y for x in range(blocks_x)]

brightness_add = 60

#exit()
def getblockbits(pix, x, y):
	xx = x*3
	yy = y*2
	bit0 = pix[xx+0][yy+0]>>7
	bit1 = pix[xx+1][yy+0]>>7
	bit2 = pix[xx+2][yy+0]>>7
	bit3 = pix[xx+0][yy+1]>>7
	bit4 = pix[xx+1][yy+1]>>7
	bit5 = pix[xx+2][yy+1]>>7
	return bit0*1 + bit1*2 + bit2*4 + bit3*8 + bit4*16 + bit5*32

def bools(bit):
	return "true" if (bit&1 == 1) else "false"

def bitstostate(bits):
	state = "minecraft:chiseled_bookshelf[facing=south"
	for i in range(6):
		state += ",slot_{}_occupied={}".format(i, bools(bits>>i))
	state += "]"
	return state

def setblock(x, y, z, state):
	return "setblock {} {} {} {}".format(x, y, z, state)
	
def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

with MCRcon("127.0.0.1", "1234") as mcr:
	mcr.command("fill {} {} {} {} {} {} {} replace".format(origin_x, origin_y, origin_z, origin_x+blocks_x-1, origin_y+blocks_y-1, origin_z, bitstostate(endbits)))
	mcr.command("teleport @p {:.2f} {:.2f} {:.2f} 180 0".format(origin_x+(blocks_x/2), origin_y+(blocks_y/2)-1.62, origin_z+view_distance))
	while True:
		shot=np.array(sct.grab(bounding_box))
		shot=increase_brightness(shot,brightness_add)
		#cv2.imshow("a",shot)
		#cv2.waitKey(0)
		shot=cv2.cvtColor(shot, cv2.COLOR_BGR2GRAY)
		shot=cv2.resize(shot,(blocks_x*3,blocks_y*2))
		#cv2.imshow("a",shot)
		#cv2.waitKey(0)
		pix=shot.T
		blockbits = copy.deepcopy(emptybits)
		function = ""
		functions=[]
		for x in range(blocks_x):
			for y in range(blocks_y):
				blockbits[x][y] = getblockbits(pix, x, y)
				changed = (blockbits[x][y] != blockbits_last[x][y])
				if changed:
					mcr.command(setblock(origin_x+x, origin_y+blocks_y-1-y, origin_z, bitstostate(blockbits[x][y])))
		blockbits_last=blockbits
		
		
		
