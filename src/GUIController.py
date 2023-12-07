from PIL import Image
import PySimpleGUI as sg
import os
import io
import numpy as np
from preProcessor.preProcessor import createTileSet, createAdjacency
from waveCollapse.waveFunction import wfc_core

file_types = [('PNG (*.png)', '*.png')]

def Main ():
	sg.theme('Dark Blue 3')  # please make your windows colorful
	
	layout = [[sg.Text('')],
			[sg.Input(key='-IN-', change_submits=True), sg.FileBrowse(key='-FILEPATH-', file_types=file_types)],
			[sg.Button('Generate'), sg.Button('Exit')],
			[sg.Text(key='-OUTPUT-')],
			[sg.Image(key='-IMAGE-'), sg.Image(key='-GENERATED-')]]

	window = sg.Window('Window Title', layout, size=(1200,500))

	while True:  # Event Loop
		event, values = window.read()
		print(event, values)
		if event == sg.WIN_CLOSED or event == 'Exit':
			break
		if event == 'Generate':
			# change the "output" element to be the value of "input" element
			window['-OUTPUT-'].update(values['-FILEPATH-'])
			if os.path.exists(values['-FILEPATH-']):
				image = Image.open(values["-FILEPATH-"])
				imNew = image.resize((300, 300), Image.NEAREST)
				bio = io.BytesIO()
				imNew.save(bio, format="PNG")
				window["-IMAGE-"].update(data=bio.getvalue())
				print('Opened original', flush=True)

				tileSet , frequencyTable = createTileSet(image)
				print('Created tileset', flush=True)
				adjacencyTable = createAdjacency(tileSet)
				print('Created adjacency table', flush=True)
				grid = wfc_core(adjacencyTable, frequencyTable, (50,50), printOutput=True)
				print('Created grid', flush=True)
				generatedBio = io.BytesIO()
				generatedImage = _draw(tileSet, grid, (50,50))
				generatedImage = generatedImage.resize((300, 300), Image.NEAREST)
				#print(list(generatedImage.getdata()))
				generatedImage.save(generatedBio, format="PNG")
				window['-GENERATED-'].update(data=generatedBio.getvalue())
				print('Finished', flush=True)
	
	window.close()

def _draw(tileSet : list, grid : list[list[int]], size : tuple):
	tempArray = []
	for y in range(size[1]):
		for x in range(size[0]):
			tempArray.append(tileSet[grid[x][y]].pixels[0][0])
	#print(f'Array: {tempArray}\n')
	#print('-------------')
	npArray = np.array(tempArray).reshape(size[0], size[1], 4).astype('uint8')
	#print(npArray)
	return Image.fromarray(npArray, mode="RGBA")


if __name__ == "__main__":
	Main()