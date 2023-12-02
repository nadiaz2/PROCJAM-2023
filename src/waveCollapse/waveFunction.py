# The following link taught us a majority of what we have learned about the wave function collapse algorithm.
# We drew heavy insperation from this article and used the author's Rust code as a basis for our implementation.
# https://www.gridbugs.org/wave-function-collapse/

from waveClasses import Grid


def Main():
	tileGrid = Grid(200, 200, 5)

	for item in tileGrid.heap:
		print(item)

	print('done')

def getNeighborSet(coord: tuple[int,int], gridSize: tuple[int,int]) -> list[tuple[int,int]]:
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

if __name__ == "__main__":
	Main()
	#print(getNeighborSet((1,1), (3,3)))