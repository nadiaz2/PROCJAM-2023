from PIL import Image
from math import floor
from copy import deepcopy
import sys
sys.path.append('src/utils')
from direction import Direction

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
			self.pixels = pixels
	

def createTileSet (image : Image) -> tuple[list[Tile], list[int]]:
	width = image.width
	height = image.height
	pixel_vals = list(image.getdata())
	all_tiles = []
	frequency_list = []

	OFFSET = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

	for i,pixel in enumerate(pixel_vals):

		tempPixels = [[None, None, None],[None, None, None],[None, None, None]]
		for xOffset, yOffset in OFFSET:
			x = (i + xOffset) % width
			y = (floor(i / width) + yOffset) % height
			tempPixels[xOffset][yOffset] = pixel_vals[y * width + x]
		
		flag = False

		for index,tile in enumerate(all_tiles):
			if tempPixels == tile.pixels:
				frequency_list[index] += 1
				flag = True

		if not flag:
			matrix = tempPixels
			# 4 rotations
			for _ in range(0,4):
				matrix = _rotateMatrix(matrix)
				for _ in range(0,2):
					matrix = _reflectMirror(matrix)
					tempTile = Tile(len(all_tiles), matrix)
					all_tiles.append(tempTile)
					frequency_list.append(1)
		
	return (all_tiles, frequency_list)


def createAdjacency (tileSet : list):
	adjacencyTable = [([],[],[],[]) for _ in range(len(tileSet))]
	for tile in tileSet:
		tempTile = tile.pixels

		for adjacentTile in tileSet[tile.index:]:
			tempAdjacentTile = adjacentTile.pixels

			for dir in Direction:
				tempTile = _rotateMatrix(tempTile)
				tempAdjacentTile = _rotateMatrix(tempAdjacentTile)

				if _checkValid(tempTile, tempAdjacentTile):
					adjacencyTable[tile.index][dir.value].append(adjacentTile.index)
					adjacencyTable[adjacentTile.index][(dir.value+2) % 4].append(tile.index)

	return adjacencyTable


def _checkValid(tile, adjacent):
	return (tile[1] == adjacent[0]) and (tile[2] == adjacent[1])


def _rotateMatrix(matrix):
	copy = deepcopy(matrix)

	# rotate corners
	copy[0][0] = matrix[0][2]
	copy[0][2] = matrix[2][2]
	copy[2][2] = matrix[2][0]
	copy[2][0] = matrix[0][0]
	
	# rotate sides
	copy[1][0] = matrix[0][1]
	copy[0][1] = matrix[1][2]
	copy[1][2] = matrix[2][1]
	copy[2][1] = matrix[1][0]

	return copy


def _reflectMirror(matrix):
	"""Returns a copy of the given matrix that is reflected over the vertical axis."""
	copy = deepcopy(matrix)
	copy[0], copy[2] = copy[2], copy[0]
	return copy


if __name__ == "__main__":
	Main()
