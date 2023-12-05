from dataclasses import dataclass
from heapq import heappush, heappop
from random import random, randint
from waveExceptions import *
from math import log2


class TileCell:
	"""Class for keeping track of the state of individual cells in the grid."""
	collapsed: bool
	chosenTile: int
	possible: list[bool]
	_sum_of_possible_weights: int
	_sum_of_possilbe_weight_log_weight: float
	_entropy_noise: float

	def __init__(self, frequencyHints: list[int]):
		self.collapsed = False
		self.possible = [True]*len(frequencyHints)
		self._sum_of_possible_weights = sum(frequencyHints)
		self._sum_of_possilbe_weight_log_weight = sum([freq*log2(freq) for freq in frequencyHints])
		self._entropy_noise = random() / 10_000

	def collapse(self, frequencyHints: list[int]) -> bool:
		weightedList = []
		for i, possible in enumerate(self.possible):
			if(not possible):
				continue
			
			for _ in range(frequencyHints[i]):
				weightedList.append(i)
		
		if(len(weightedList) == 0):
			return False

		self.chosenTile = weightedList[randint(0, len(weightedList)-1)]
		self.collapsed = True
		for index, possible in enumerate(self.possible):
			if(possible):
				self._removeTile(index, frequencyHints)
		
		return True

	def entropy(self) -> float:
		"""Returns the current entropy of this cell."""
		# The \ allows the code to carry onto the next line. It has no effect on the computation.
		return log2(self._sum_of_possible_weights) \
			- (self._sum_of_possilbe_weight_log_weight / self._sum_of_possible_weights) \
			+ self._entropy_noise

	def updateEntropy(self) -> bool:
		"""Checks how tiles are possible for this cell and updates 'possible' list accordingly.
		Returns True if the posibilities have changed, False otherwise."""
		# TODO: Implement possibility update
		return False

	def _removeTile(self, tile_index: int, freq_hints: list[int]):
		"""Removes a tile from the 'possible' list and updates the cached entropy values accordingly."""
		self.possible[tile_index] = False

		freq = freq_hints[tile_index]
		self._sum_of_possible_weights -= freq
		self._sum_of_possilbe_weight_log_weight -= freq * log2(freq)


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


class Grid:
	"""The entire grid of cells. Contains redundant information to make access easier (ex. size)"""
	cells: list[list[TileCell]]
	size: tuple[int,int]
	heap: EntropyHeap

	def __init__(self, width: int, height: int, frequencyHints: list[int]):
		self.size = (width, height)
		self.cells = [[None for i in range(height)] for j in range(width)]
		self.heap = EntropyHeap()

		for x in range(width):
			for y in range(height):
				cell = TileCell(frequencyHints)
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
