from PIL import Image
import PySimpleGUI as sg
import os
import io
import numpy as np
from preProcessor.preProcessor import createTileSet, createAdjacency
from waveCollapse.waveFunction import wfc_core
import threading
from queue import Queue

file_types = [('PNG (*.png)', '*.png')]

def Main ():
	sg.theme('Dark Blue 3')  # please make your windows colorful
	
	layout = [[sg.Text('')],
			[sg.Input(key='-IN-', change_submits=True), sg.FileBrowse(key='-FILEPATH-', file_types=file_types),  sg.Button('Exit')],
			[sg.Button('Generate'), sg.Input(key='-SAVEAS-FILENAME-', visible=False, enable_events=True), sg.FileSaveAs(key='-SAVEAS-', file_types=file_types, visible=False)],
			[sg.Text(key='-OUTPUT-')],
			[sg.Image(key='-IMAGE-'), sg.Image(key='-GENERATED-', visible=False)],
			[sg.Text(key='-PROGRESS-')]]

	window = sg.Window('Window Title', layout, size=(700,500))
	t1 = None
	queue = Queue(maxsize=3)

	while True:  # Event Loop		
		event, values = window.read()
		print(event, values)
		if event == sg.WIN_CLOSED or event == 'Exit':
			if t1 != None and t1.is_alive:
				t1.join()
			break
		if event == '-IN-':
			window['Generate'].update(visible=True)
			window['-SAVEAS-'].update(visible=False)
		if event == 'Generate':
			window['-SAVEAS-'].update(visible=False)
			# change the "output" element to be the value of "input" element
			if window['-GENERATED-'].visible:
				window['-GENERATED-'].update(visible=False)
			window['-OUTPUT-'].update(values['-IN-'])
			window['Generate'].update(visible=False)
			if os.path.exists(values['-IN-']):
				image = Image.open(values["-IN-"])
				imNew = image.resize((300, 300), Image.NEAREST)
				bio = io.BytesIO()
				imNew.save(bio, format="PNG")
				window["-IMAGE-"].update(data=bio.getvalue())
				print('Opened original', flush=True)
				if t1 == None:
					while(queue.qsize() >= 1):
						queue.get()
					t1 = threading.Thread(target=_threadGenerate, args=(image, window,queue,))
					t1.start()
		if t1 != None and not t1.is_alive():
			window['Generate'].update(visible=True)
			t1.join()
			t1 = None
		if event == '-SAVEAS-FILENAME-':
			window['Generate'].update(visible=True)
			window['-SAVEAS-'].update(visible=False)
			print(window['-GENERATED-'])
			if queue.qsize() >= 1:
				generatedImage = queue.get()
				generatedImage.save(values['-SAVEAS-FILENAME-'], "PNG")
		
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

def _threadGenerate(image : Image, window : sg.Window, queue : Queue) :
	window['-PROGRESS-'].update('Generating Tileset')
	# Set to run
	tileSet , frequencyTable = createTileSet(image)
	print('Created tileset', flush=True)
	window['-PROGRESS-'].update('Generating Adjancency Rules')
	adjacencyTable = createAdjacency(tileSet)
	print('Created adjacency table', flush=True)
	window['-PROGRESS-'].update('Generating Grid')
	grid = wfc_core(adjacencyTable, frequencyTable, (50,50), printOutput=True)
	print('Created grid', flush=True)
	window['-PROGRESS-'].update('Generating Image')
	generatedBio = io.BytesIO()
	generatedImage = _draw(tileSet, grid, (50,50))
	generatedImage = generatedImage.resize((300, 300), Image.NEAREST)
	generatedImage.save(generatedBio, format="PNG")
	window['-GENERATED-'].update(data=generatedBio.getvalue())
	window['-GENERATED-'].update(visible = True)
	window['-PROGRESS-'].update('Image Generated')
	window['Generate'].update(visible=True)
	window['-SAVEAS-'].update(visible=True)
	queue.put(generatedImage)


if __name__ == "__main__":
	Main()