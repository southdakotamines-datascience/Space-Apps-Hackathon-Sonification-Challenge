import json
import PySimpleGUI as sg
import os
import threading
from Sam import SamGenerator
from sonifying_module import sonify
from OutputMIDI import OutputMIDI

sg.theme("DarkBrown")

layout = [
    [sg.Text('Enter a Path to Frame Directory')],
    [sg.FileBrowse(key="file_browse", size=(50, 1)), sg.Input(key="directory_path", size=(50, 1))],
    [sg.Text("From:"), sg.InputText(key="from_input", size=(10, 1)), sg.Text("To:"),
     sg.InputText(key="to_input", size=(10, 1))],
    [sg.Button("OK")]
]

loading_layout = [
    [sg.Text('Working... Please wait.', size=(30, 1), key='-LOADING-')]
]

window = sg.Window('Sonification', layout)
loading_window = sg.Window('Loading', loading_layout, finalize=True)
loading_window.hide()


# Function to run the time-consuming task in a separate thread
def run_sam_generator(input_path, from_value, to_value):
    Sam = SamGenerator()
    Sam.generate(input_path)
    sonified_json = sonify("test.txt")
    midi = OutputMIDI(sonified_json, generate_incremented_filename("MIDI") + ".mid")
    midi.Output()

    # Close the loading window
    loading_window.hide()
    window.un_hide()


def generate_incremented_filename(base_filename):
    # Check if the file already exists
    count = 1
    filename = f"{base_filename}"

    while os.path.exists(filename):
        count += 1
        filename = f"{base_filename}_{count}"

    return filename


while True:

    event, values = window.read()

    if event in (None, 'Exit'):
        break

    if event == "OK":
        input_path = values['directory_path']
        from_value = values["from_input"]
        to_value = values["to_input"]

        # Show the loading screen
        window.hide()
        loading_window.un_hide()

        # Start the time-consuming task in a separate thread
        thread = threading.Thread(target=run_sam_generator, args=(input_path, from_value, to_value))
        thread.start()

# Close
window.close()
