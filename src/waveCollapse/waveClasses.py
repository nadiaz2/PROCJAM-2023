from dataclasses import dataclass
from heapq import heappush, heappop
import random
from waveExceptions import *
from math import log2
from copy import deepcopy
import time
import sys
sys.path.append('src/utils')
from direction import Direction



@dataclass
class RemovalUpdate:
	"""Represents that the stored tileIndex was removed from the possibilities
	of the cell at the stored coordinate."""
	tileIndex: int
	coord: tuple[int,int]


@dataclass(frozen = True, order = True)
class EntropyCoord:
	"""Immutable class that stores the entropy for a specific coord"""
	entropy: float
	coord: tuple[int, int]


class EntropyHeap:
	"""Maintains the heap of entropy values for cells"""
	_heap: list[EntropyCoord]

	def __init__(self):
		self._heap = []

	def push(self, item: EntropyCoord):
		heappush(self._heap, item)

	def pop(self) -> EntropyCoord:
		return heappop(self._heap)

	def __iter__(self):
		return self
	
	def __next__(self):
		try:
			return self.pop()
		except(IndexError):
			raise StopIteration


class TileCell:
	"""Class for keeping track of the state of individual cells in the grid."""
	collapsed: bool
	chosenTile: int
	possible: list[bool]  # indexed by tile_index
	_sum_of_possible_weights: int
	_sum_of_possilbe_weight_log_weight: float
	_entropy_noise: float
	tile_enabler_counts: list[list[int]]  # outer list is indexed by tile_index, inner list is indexed by Direction

	def __init__(self, frequencyHints: list[int], enablerList: list[list[int]]):
		self.collapsed = False
		self.chosenTile = -1
		self.possible = [True]*len(frequencyHints)
		self._sum_of_possible_weights = sum(frequencyHints)
		self._sum_of_possilbe_weight_log_weight = sum([freq*log2(freq) for freq in frequencyHints])
		self._entropy_noise = random.random() / 100_000
		self.tile_enabler_counts = deepcopy(enablerList)

	def collapse(self, frequencyHints: list[int]) -> bool:
		weightedList = []
		for i, possible in enumerate(self.possible):
			if(not possible):
				continue
			
			for _ in range(frequencyHints[i]):
				weightedList.append(i)
		
		if(len(weightedList) == 0):
			return False

		self.chosenTile = weightedList[random.randint(0, len(weightedList)-1)]
		self.collapsed = True
		self.possible = [i == self.chosenTile for i in range(len(self.possible))]
		
		return True

	def entropy(self) -> float:
		"""Returns the current entropy of this cell."""
		# The \ allows the code to carry onto the next line. It has no effect on the computation.
		return log2(self._sum_of_possible_weights) \
			- (self._sum_of_possilbe_weight_log_weight / self._sum_of_possible_weights) \
			+ self._entropy_noise

	def removeTile(self, tile_index: int, freq_hints: list[int]):
		"""Removes a tile from the 'possible' list and updates the cached entropy values accordingly."""
		self.possible[tile_index] = False

		freq = freq_hints[tile_index]
		self._sum_of_possible_weights -= freq
		self._sum_of_possilbe_weight_log_weight -= freq * log2(freq)


class Grid:
	"""The entire grid of cells. Contains redundant information to make access easier (ex. size)"""
	cells: list[list[TileCell]]
	size: tuple[int,int]
	cellsCollapsed: int
	heap: EntropyHeap
	seed: int

	def __init__(self, width: int, height: int, adjacencyRules: list[tuple(list[int])], frequencyHints: list[int], given_seed: int = None):
		self.size = (width, height)
		self.cellsCollapsed = 0
		self.cells = [[None for i in range(height)] for j in range(width)]
		self.heap = EntropyHeap()
		
		if(given_seed == None):
			given_seed = int(time.time())
		random.seed(given_seed)
		self.seed = given_seed

		defaultEnablers = Grid._getDefaultEnablers(adjacencyRules)

		for x in range(width):
			for y in range(height):
				cell = TileCell(frequencyHints, defaultEnablers)
				self.cells[x][y] = cell
				self.heap.push(EntropyCoord(cell.entropy(), (x,y)))

	def getFinalTileList(self) -> list[list[int]]:
		width, height = self.size
		
		tiles = [[None for _ in range(height)] for _ in range(width)]

		for x in range(width):
			for y in range(height):
				if(self.cells[x][y].collapsed):
					tiles[x][y] = self.cells[x][y].chosenTile
				else:
					raise NotReadyException("Not all cells have been collapsed.")
		
		return tiles
	
	@staticmethod
	def _getDefaultEnablers(adjacencyRules: list[tuple[list[int]]]) -> list[list[int]]:
		tile_count = len(adjacencyRules)
		defaultEnablers = [[0,0,0,0] for _ in range(tile_count)]

		# This for loop calculates the number of tiles that enable each tile from a specific direction.
		# For example, defaultEnablers[tile_a][Direction.RIGHT.value] would be the number of possibilities
		# from the RIGHT side that allow tile_a to exist in a given cell.
		#
		# This calculation relies on the adjacencyRules being consistent. This means that if tile_a
		# enables tile_b to be placed on its left, then tile_b must also enable tile_a to be placed
		# on its right. Therefore the number of tiles that tile_a enables in a given direction is equal
		# to the number of tiles that enable it from the opposite direction.
		for index in range(tile_count):
			for dir in Direction:
				defaultEnablers[index][dir.value] = len(adjacencyRules[index][dir.value])
		
		return defaultEnablers
