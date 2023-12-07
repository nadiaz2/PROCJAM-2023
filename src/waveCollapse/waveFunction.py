# The following link taught us a majority of what we have learned about the wave function collapse algorithm.
# We drew heavy insperation from this article and used the author's Rust code as a basis for our implementation.
# https://www.gridbugs.org/wave-function-collapse/

from waveClasses import *


def wfc_core(adjacencyRules: list[tuple[list[int]]], frequencyRules: list[int], outputSize: tuple[int,int]):
	tileGrid = Grid(outputSize[0], outputSize[1], adjacencyRules, frequencyRules, given_seed=1701893307)
	removalStack: list[RemovalUpdate] = []

	for item in tileGrid.heap:
		x, y = item.coord
		cell = tileGrid.cells[x][y]
		if(cell.collapsed):
			continue
		
		# Collapse chosen cell
		oldPossible = cell.possible
		success = cell.collapse(frequencyRules)
		_printTileList(tileGrid.getFinalTileList())
		if(not success):
			# TODO: restart
			raise NotImplementedError("Yet to implement redo or abort on contradiction.")

		# Begin propogation
		oldPossible[cell.chosenTile] = False  # the chosen tile is still a valid enabler

		# The stack should be empty at the moment. This just adds all needed RemovalUpdates
		removalStack = [RemovalUpdate(index, item.coord) for index,pastPossible in enumerate(oldPossible) if pastPossible]

		_updatePossible(tileGrid, removalStack, adjacencyRules, frequencyRules)
	
	return tileGrid.getFinalTileList()


def _getNeighborSet(coord: tuple[int,int], gridSize: tuple[int,int]) -> list[tuple[Direction, tuple[int,int]]]:
	"""Returns a list of coordinate pairs that are directly adjacent to the given coord.
	Coordinates that lie outside the given gridSize are not returned in the list."""
	def inBounds(variable):
		x, y = variable[1]

		if(x >= gridSize[0] or x < 0):
			return False
		if(y >= gridSize[1] or y < 0):
			return False
		
		return True

	offsets = [(Direction.LEFT, (-1,0)), (Direction.RIGHT, (1,0)), (Direction.UP, (0,-1)), (Direction.DOWN, (0,1))]
	neighbors = [(dir, (coord[0]+x, coord[1]+y)) for dir,(x,y) in offsets]
	neighbors = list(filter(inBounds, neighbors))

	return neighbors


def _updatePossible(tileGrid: Grid, removalStack: list[RemovalUpdate], adjacencyRules: list[tuple[list[int]]], frequencyHints: list[int]):
	while(len(removalStack) > 0):
		removal = removalStack.pop()
		tileIndex = removal.tileIndex
		coord = removal.coord
		for dir,cellCoord in _getNeighborSet(coord, tileGrid.size):
			x,y = cellCoord
			cell = tileGrid.cells[x][y]

			if(cell.collapsed):
				continue

			# for all tiles that tileIndex enables via adjacencyRules
			for enabledTile in adjacencyRules[tileIndex][dir.value]:
				if(not cell.possible[enabledTile]):
					continue

				cell.tile_enabler_counts[enabledTile][(dir.value+2) % 4] -= 1

				if(cell.tile_enabler_counts[enabledTile][(dir.value+2) % 4] == 0):
					cell.removeTile(enabledTile, frequencyHints)
					removalStack.append(RemovalUpdate(enabledTile, cellCoord))
					tileGrid.heap.push(EntropyCoord(cell.entropy(), cellCoord))


def _printTileList(tileList):
	output = ""
	for y in range(len(tileList[0])):
		for x in range(len(tileList)):
			output += str(tileList[x][y]) + " "
		output += '\n'
	print(output)

if __name__ == "__main__":
	tileList = wfc_core([([0,1],[0,1],[0,1],[0]),([0,1],[0,1],[0,1],[0,1])], [1,1], (3,3))
	_printTileList(tileList)

	print(_getNeighborSet((1,1), (3,3)))