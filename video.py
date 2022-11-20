#idea and some code was taken from https://github.com/kasamikona/BadAppleBookshelf/

from PIL import Image
from mcrcon import MCRcon
numframes=4382
blocks_x = 16
blocks_y = 12

origin_x = 0
origin_y = 90
origin_z = 0

view_distance = 8.7 

startbits = 0
endbits = 0
startdelay = 20
blockbits_last = [[startbits]*blocks_y for x in range(blocks_x)]
pixes=[0]
for fn in range(1, numframes+1):
		im = Image.open("frames/frame_{:04d}.png".format(fn))
		pixes.append(im.convert('L').load())


def getblockbits(pix, x, y):
	xx = x*3
	yy = y*2
	bit0 = pix[xx+0,yy+0]>>7
	bit1 = pix[xx+1,yy+0]>>7
	bit2 = pix[xx+2,yy+0]>>7
	bit3 = pix[xx+0,yy+1]>>7
	bit4 = pix[xx+1,yy+1]>>7
	bit5 = pix[xx+2,yy+1]>>7
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
	

with MCRcon("127.0.0.1", "1234") as mcr:
	mcr.command("fill {} {} {} {} {} {} {} replace".format(origin_x, origin_y, origin_z, origin_x+blocks_x-1, origin_y+blocks_y-1, origin_z, bitstostate(endbits)))
	mcr.command("teleport @p {:.2f} {:.2f} {:.2f} 180 0".format(origin_x+(blocks_x/2), origin_y+(blocks_y/2)-1.62, origin_z+view_distance))
	for fn in range(1, numframes+1):
		pix=pixes[fn]
		blockbits = [[0]*blocks_y for x in range(blocks_x)]
		function = ""
		functions=[]
		for x in range(blocks_x):
			for y in range(blocks_y):
				blockbits[x][y] = getblockbits(pix, x, y)
				changed = (blockbits[x][y] != blockbits_last[x][y])
				if changed:
					mcr.command(setblock(origin_x+x, origin_y+blocks_y-1-y, origin_z, bitstostate(blockbits[x][y])))
		blockbits_last=blockbits
		
		
		
