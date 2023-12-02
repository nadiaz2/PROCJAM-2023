from dataclasses import dataclass
from heapq import heappush, heappop
import random


class TileCell:
	"""Class for keeping track of the state of individual cells in the grid."""
	collapsed: bool
	possible: list
	_entropy_noise: float

	def __init__(self, tileSetSize):
		self.collapsed = False
		self.possible = [True]*tileSetSize
		self._entropy_noise = random.random() / 1000

	def entropy(self) -> float:
		"""Returns the current entropy of this cell."""
		# TODO: Impelment entropy calculation
		return self._entropy_noise

	def updateEntropy(self) -> bool:
		"""Checks how tiles are possible for this cell and updates 'possible' list accordingly.
		Returns True if the posibilities have changed, False otherwise."""
		# TODO: Implement possibility update
		return False


@dataclass(frozen = True, order = True)
class EntropyCoord:
	"""Immutable class that stores the entropy for a specific coord"""
	entropy: float
	coord: tuple[int, int]


class Heap:
	_heap: list

	def __init__(self):
		self._heap = []

	def push(self, item):
		heappush(self._heap, item)

	def pop(self):
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
	heap: Heap

	def __init__(self, width, height, tileSetSize):
		self.size = (width, height)
		self.cells = [[None]*height]*width
		self.heap = Heap()

		for x in range(width):
			for y in range(height):
				cell = TileCell(tileSetSize)
				self.cells[x][y] = cell
				self.heap.push(EntropyCoord(cell.entropy(), (x,y)))
