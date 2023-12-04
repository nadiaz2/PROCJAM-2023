from PIL import Image
import PySimpleGUI as sg
import os
import io

file_types = [("PNG (*.png)", "*.png")]

def Main ():
	sg.theme('Dark Blue 3')  # please make your windows colorful
	
	layout = [[sg.Text('')],
			[sg.Input(key='-IN-', change_submits=True), sg.FileBrowse(key='-FILEPATH-', file_types=file_types)],
			[sg.Button('Generate'), sg.Button('Exit')],
			[sg.Text(key='-OUTPUT-')],
			[sg.Image(key='-IMAGE-')]]

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
				image.thumbnail((200, 200))
				bio = io.BytesIO()
				image.save(bio, format="PNG")
				window["-IMAGE-"].update(data=bio.getvalue())
	
	window.close()


if __name__ == "__main__":
	Main()