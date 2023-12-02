# The following link taught us a majority of what we have learned about the wave function collapse algorithm.
# We drew heavy insperation from this article and used the author's Rust code as a basis for our implementation.
# https://www.gridbugs.org/wave-function-collapse/

from dataclasses import dataclass
from heapq import heappush, heappop, heapify
import random

@dataclass
class TileCell:
	"""Class for keeping track of the state of individual cells in the grid."""
	collapsed: bool
	possible: list
	_entropy_noise: float

	def __init__(self, tileSetSize):
		self.collapsed = False
		self.possible = [True]*tileSetSize
		self._entropy_noise = random.random() / 1000

	def entropy(self):
		"""Returns the current entropy of this cell."""
		# TODO: Impelment entropy calculation
		return self._entropy_noise

	def updateEntropy(self):
		"""Checks how tiles are possible for this cell and updates 'possible' list accordingly.
		Returns True if the posibilities have changed, False otherwise."""
		# TODO: Implement possibility update
		return False

@dataclass(frozen = True, order = True)
class EntropyCoord:
	"""Immutable class that stores the entropy for a specific coord"""
	entropy: float
	coord: tuple[int, int]

@dataclass
class Grid:
	"""The entire grid of cells. Contains redundant information to make access easier (ex. size)"""
	cells: list[list[TileCell]]
	size: tuple[int,int]
	heap: list[EntropyCoord]

	def __init__(self, width, height, tileSetSize):
		self.size = (width, height)
		self.cells = [[None]*height]*width
		self.heap = []

		for x in range(width):
			for y in range(height):
				cell = TileCell(tileSetSize)
				self.cells[x][y] = cell
				heappush(self.heap, EntropyCoord(cell.entropy(), (x,y)))


tileGrid: Grid = None

def Main():
	#global entropyHeap
	#heapq.heapify(entropyHeap) #sorts the current list into a heap structure
	#heapq.heappush(entropyHeap, EntropyCoord(10.0, (0,0))) #inserts the given element into entropyHeap, assuming heap structure
	#heapq.heappop(entropyHeap) #pops the smallest element off the heap and maintains heap structure

	global tileGrid
	tileGrid = Grid(200, 200, 5)

	for i in range(len(tileGrid.heap)):
		print(heappop(tileGrid.heap))

	print('done')

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

	return neighbors

if __name__ == "__main__":
	Main()
	getNeighborSet((0,1))