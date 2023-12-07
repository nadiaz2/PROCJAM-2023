# The following link taught us a majority of what we have learned about the wave function collapse algorithm.
# We drew heavy insperation from this article and used the author's Rust code as a basis for our implementation.
# https://www.gridbugs.org/wave-function-collapse/

from waveClasses import *


def wfc_core(adjacencyRules: list[tuple[list[int]]], frequencyRules: list[int], outputSize: tuple[int,int], seed: int = None, printOutput: bool = False) -> list[list[int]]:
	MAX_FAILS = 10
	fails = 0
	tileOutput = None
	while((fails < MAX_FAILS) and (tileOutput == None)):
		try:
			gridSeed, tileOutput = _runGeneration(adjacencyRules, frequencyRules, outputSize, seed)
		except ContradictionException:
			fails += 1
			if(printOutput):
				print('Fail!')

	if(printOutput):
		print(f'SEED: {gridSeed}')
		_printTileList(tileOutput)
	
	return tileOutput


def _runGeneration(adjacencyRules: list[tuple[list[int]]], frequencyRules: list[int], outputSize: tuple[int,int], seed: int) -> tuple[int, list[list[int]]]:
	tileGrid = Grid(outputSize[0], outputSize[1], adjacencyRules, frequencyRules, seed)
	removalStack: list[RemovalUpdate] = []

	for item in tileGrid.heap:
		x, y = item.coord
		cell = tileGrid.cells[x][y]
		if(cell.collapsed):
			continue
		
		# Collapse chosen cell
		oldPossible = cell.possible
		success = cell.collapse(frequencyRules)
		if(not success):
			raise ContradictionException("A cell ran out of possibilities during generation.")

		# Begin propogation
		oldPossible[cell.chosenTile] = False  # the chosen tile is still a valid enabler

		# The stack should be empty at the moment. This just adds all needed RemovalUpdates
		removalStack = [RemovalUpdate(index, item.coord) for index,pastPossible in enumerate(oldPossible) if pastPossible]

		_updatePossible(tileGrid, removalStack, adjacencyRules, frequencyRules)

	return (tileGrid.seed, tileGrid.getFinalTileList())


def _getNeighborSet(coord: tuple[int,int], gridSize: tuple[int,int]) -> list[tuple[Direction, tuple[int,int]]]:
	"""Returns a list of coordinate pairs that are directly adjacent to the given coord.
	Coordinates that lie outside the given gridSize are not returned in the list."""
	def inBounds(variable):
		x, y = variable[1]
		x, y = variable[1]

		if(x >= gridSize[0] or x < 0):
		if(x >= gridSize[0] or x < 0):
			return False
		if(y >= gridSize[1] or y < 0):
		if(y >= gridSize[1] or y < 0):
			return False
		
		return True

	offsets = [(Direction.LEFT, (-1,0)), (Direction.RIGHT, (1,0)), (Direction.UP, (0,-1)), (Direction.DOWN, (0,1))]
	neighbors = [(dir, (coord[0]+x, coord[1]+y)) for dir,(x,y) in offsets]
	offsets = [(Direction.LEFT, (-1,0)), (Direction.RIGHT, (1,0)), (Direction.UP, (0,-1)), (Direction.DOWN, (0,1))]
	neighbors = [(dir, (coord[0]+x, coord[1]+y)) for dir,(x,y) in offsets]
	neighbors = list(filter(inBounds, neighbors))

	return neighbors


def _updatePossible(tileGrid: Grid, removalStack: list[RemovalUpdate], adjacencyRules: list[tuple[list[int]]], frequencyHints: list[int]):
	while(len(removalStack) > 0):
		removal = removalStack.pop()
		tileRemoved = removal.tileIndex
		coord = removal.coord
		for dir,neighborCoord in _getNeighborSet(coord, tileGrid.size):
			x,y = neighborCoord
			neighborCell = tileGrid.cells[x][y]
			oppositeDir = (dir.value+2) % 4

			if(neighborCell.collapsed):
				continue

			# for all tiles that tileRemoved enables via adjacencyRules
			for enabledTile in adjacencyRules[tileRemoved][dir.value]:
				if(not neighborCell.possible[enabledTile]):
					continue

				neighborCell.tile_enabler_counts[enabledTile][oppositeDir] -= 1

				if(neighborCell.tile_enabler_counts[enabledTile][oppositeDir] == 0):
					neighborCell.removeTile(enabledTile, frequencyHints)
					tileGrid.heap.push(EntropyCoord(neighborCell.entropy(), neighborCoord))
					removalStack.append(RemovalUpdate(enabledTile, neighborCoord))


def _printTileList(tileList):
	if(tileList == None):
		print('tileList is None\n')
		return

	output = ""
	for y in range(len(tileList[0])):
		for x in range(len(tileList)):
			output += str(tileList[x][y]) + " "
		output += '\n'
	print(output)

if __name__ == "__main__":
	wfc_core(
		[
			([0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4]),
			([0,3], [0,2], [0,3], [0,2]),
			([0,4], [0,1], [0,4], [0,1]),
			([0,1], [0], [0,1], [0]),
			([0,2], [0], [0,2], [0])
		],
		[1, 5, 5, 5, 5],
		(20, 10),
		seed=None,
		printOutput=True
	)