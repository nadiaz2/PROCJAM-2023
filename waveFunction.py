from dataclasses import dataclass
import heapq
import random

@dataclass
class TileCell:
	"""Class for keeping track of the state of individual cells in the grid."""
	collapsed: bool
	possible: list
	entropy_noise: float

	def __init__(self, tileSetSize):
		self.collapsed = False
		self.possible = [True]*tileSetSize
		self.entropy_noise = random.random() / 1000

@dataclass
class Grid:
	"""The entire grid of cells. Contains redundant information to make access easier (ex. size)"""
	cells: list[list[TileCell]]
	size: tuple[int,int]

	def __init__(self, width, height, tileSetSize):
		self.size = (width, height)
		self.cells = [[TileCell(tileSetSize)]*height]*width

@dataclass(frozen = True, order = True)
class EntropyCoord:
	"""Immutable class that stores the entropy for a specific coord"""
	entropy: float
	coord: tuple[int, int]


tileGrid: Grid = None
entropyHeap = list()

def Main():
	#global entropyHeap
	#heapq.heapify(entropyHeap) #sorts the current list into a heap structure
	#heapq.heappush(entropyHeap, EntropyCoord(10.0, (0,0))) #inserts the given element into entropyHeap, assuming heap structure
	#heapq.heappop(entropyHeap) #pops the smallest element off the heap and maintains heap structure

	#for x in range(size[0]):
	#	for y in range(size[1]):
	#		heapq.heappush(entropyHeap, EntropyCoord(random.random()*100, (x,y)))

	#heapq.heappush(entropyHeap, EntropyCoord(10.0, (0,0)))
	#print(heapq.heappop(entropyHeap))
	global tileGrid
	tileGrid = Grid(200, 200, 5)
	print("done")
	#for i in range(len(entropyHeap)):
	#	print(heapq.heappop(entropyHeap))

def getNeighborSet(coord: tuple[int,int]):
	def inBounds(variable):
		x, y = variable

		global tileGrid
		if(x >= tileGrid.size[0] or x < 0):
			return False
		if(y >= tileGrid.size[1] or y < 0):
			return False
		
		return True

	offsets = [(-1,0), (1,0), (0,-1), (0,1)]
	neighbors = [(coord[0]+x, coord[1]+y) for x,y in offsets]
	neighbors = list(filter(inBounds, neighbors))

	print(neighbors)
	return neighbors

if __name__ == "__main__":
	Main()
	getNeighborSet((0,1))