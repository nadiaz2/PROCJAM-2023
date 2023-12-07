from PIL import Image
import os
import io
import math
import numpy

def Main ():
	...

class Tile:
	"""Tile Class for holding tile index and 3x3 image"""
	index : int
	pixels : list[list[tuple[int, int, int, int]]]
	
	def __eq__(self, other):
		return self.pixels == other.pixels
	
	def __init__(self, index = None, pixels = None):
		self.index = index
		if pixels == None:
			self.pixels = [[None, None, None],[None, None, None],[None, None, None]]
		else:
			self.pixels = [[None, None, None],[None, None, None],[None, None, None]]
			for i in range(len(pixels)):
				x = i % 3
				y = math.floor(i/3)
				self.pixels[x][y] = pixels[i]
	

def createTileSet (image : Image) -> tuple[list[Tile], list[int]]:
	width = image.width
	height = image.height
	pixel_vals = list(image.getdata())
	all_tiles = []
	frequency_list = []

	OFFSET = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

	for i,pixel in enumerate(pixel_vals):

		tempPixels = list()
		for xOffset, yOffset in OFFSET:
			x = (i + xOffset) % width
			y = (math.floor(i / width) + yOffset) % height
			tempPixels.append(pixel_vals[y * width + x])
			#tempTile.pixels[xOffset][yOffset] = pixel_vals[y * width + x]
		
		flag = False

		for index,tile in enumerate(all_tiles):
			if tempPixels == tile.pixels:
				frequency_list[index] += 1
				flag = True

		if not flag:
			array = numpy.array([tempPixels])
			matrix = array.reshape(3, 3, 4)
			# 4 rotations
			for _ in range(0,4):
				matrix = numpy.rot90(matrix, 1)
				for _ in range(0,2):
					matrix = numpy.flip(matrix, 0)
					tileConfig = matrix.flatten().tolist()
					it = iter(tileConfig)
					tempTile = Tile(len(all_tiles), list(zip(it, it, it, it)))
					all_tiles.append(tempTile)
					frequency_list.append(1)
			break
		break
	
	return (all_tiles, frequency_list)
	
def _createAdjacency ():
	...

if __name__ == "__main__":
	Main()