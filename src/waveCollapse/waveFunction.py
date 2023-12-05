# The following link taught us a majority of what we have learned about the wave function collapse algorithm.
# We drew heavy insperation from this article and used the author's Rust code as a basis for our implementation.
# https://www.gridbugs.org/wave-function-collapse/

from waveClasses import Grid


def _getNeighborSet(coord: tuple[int,int], gridSize: tuple[int,int]) -> list[tuple[int,int]]:
	"""Returns a list of coordinate pairs that are directly adjacent to the given coord.
	Coordinates that lie outside the given gridSize are not returned in the list."""
	def inBounds(variable):
		x, y = variable

		if(x >= gridSize[0] or x < 0):
			return False
		if(y >= gridSize[1] or y < 0):
			return False
		
		return True

	offsets = [(-1,0), (1,0), (0,-1), (0,1)]
	neighbors = [(coord[0]+x, coord[1]+y) for x,y in offsets]
	neighbors = list(filter(inBounds, neighbors))

	return neighbors


def wfc_core(adjacencyRules, frequencyRules: list[int], outputSize: tuple[int,int]):
	tileGrid = Grid(outputSize[0], outputSize[1], frequencyRules)

	for item in tileGrid.heap:
		x, y = item.coord
		if(tileGrid.cells[x][y].collapsed):
			continue
		
		success = tileGrid.cells[x][y].collapse(frequencyRules)
		if(not success):
			#restart
			...
	
	return tileGrid.getFinalTileList()


def _updatePossible(tileGrid: Grid, coord: tuple[int,int], adjacencyRules):
	...
	for cell in _getNeighborSet(coord, tileGrid.size):
		cell.updateEntropy()


if __name__ == "__main__":
	tileList = wfc_core(None, [1,2,3,4,5], (10,10))

	output = ""
	for y in range(len(tileList[0])):
		for x in range(len(tileList)):
			output += str(tileList[x][y]) + " "
		output += '\n'
	print(output)

	print(_getNeighborSet((1,1), (3,3)))