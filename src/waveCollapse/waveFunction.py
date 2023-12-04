# The following link taught us a majority of what we have learned about the wave function collapse algorithm.
# We drew heavy insperation from this article and used the author's Rust code as a basis for our implementation.
# https://www.gridbugs.org/wave-function-collapse/

from waveClasses import Grid
from random import randint


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


def wfc_core(tileSetSize: int, adjacencyRules, frequencyRules, outputSize: tuple[int,int]):
	tileGrid = Grid(outputSize[0], outputSize[1], tileSetSize)

	for item in tileGrid.heap:
		x, y = item.coord
		if(not tileGrid.cells[x][y].collapsed):
			_collapseCell(tileGrid, item.coord, frequencyRules)
	
	tileList = tileGrid.getFinalTileList()
	output = ""
	for y in range(tileGrid.size[1]):
		for x in range(tileGrid.size[0]):
			output += str(tileList[x][y]) + " "
		output += '\n'
	print(output)


def _collapseCell(tileGrid: Grid, coord: tuple[int,int], frequencyHints: list[int]) -> bool:
	x, y = coord
	cell = tileGrid.cells[x][y]
	
	weightedList = []
	for i, possible in enumerate(cell.possible):
		if(not possible):
			continue
		
		for _ in range(frequencyHints[i]):
			weightedList.append(i)
	
	if(len(weightedList) == 0):
		return False

	cell.chosenTile = weightedList[randint(0, len(weightedList)-1)]
	cell.possible = [cell.chosenTile]

def _updatePossible(tileGrid: Grid, coord: tuple[int,int], adjacencyRules):
	...


if __name__ == "__main__":
	#tileGrid = Grid(200, 200, 5)

	#for item in tileGrid.heap:
	#	print(item)

	#print('done')
	wfc_core(5, None, [1,2,3,4,5], (10,10))
	#print(_getNeighborSet((1,1), (3,3)))