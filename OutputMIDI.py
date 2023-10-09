import json
import math
import random
from midiutil import MIDIFile

class OutputMIDI:
    def __init__(self, json_file, output_file) -> None:
        self.json_file = json_file
        self.output_file = output_file


    def freq_to_midi(self, frequency:float) -> int:
        '''

            Convert frequency to MIDI numbers given by 
            the formula on https://newt.phys.unsw.edu.au/jw/notes.html

            Parameters
            ----------
            frequency : float
            The frequency to be converted

            Returns
            -------
            int
            
            An integer between 0 and 127 that corresponds to a 
            MIDI note
        '''
        return int(69 + 12 * math.log(frequency/440, 2))

    def amp_to_midiAmp(self, amplitude:float) -> int:
        '''
        
        Convert the Amplitude scaling factor to a MIDI output between
        0 and 127. Starts with an initial threshold amplitude of 30
        and scales with a scaling factor of 80 times the amplitude
        assigned to the object

        Parameters
        ----------
        amplitude : float
        The frequency to be converted

        Returns
        -------
        int
        
        An integer between 0 and 127 that corresponds to a 
        MIDI amplitude value
        '''

        assert amplitude >=0 and amplitude <= 1
        base_amplitude = 30 # base amplitude
        amplitude_scaling_factor = 80 # midi amplitude scaling factor
        return int(base_amplitude + amplitude_scaling_factor * amplitude)
    
    def Output(self, track_num=0, track_name="Default Track", channel=0, tempo=120, instrument=1, separate=True, randomize=False):
        '''
        
        Output the music for the provided segment data to a MIDI output file.
        Starts by opening the JSON file, reading in the amplitude and frequency
        for each segment and saving the corresponding note to a MIDI file.

        Parameters
        ----------
        track_num : int
        The track desired for notes to be added to

        track_name : string
        The name of the track desired for notes to be added to

        channel : int
        The channel desired for notes to be added to

        tempo : int 
        The desired tempo (Beats Per Minute or BPM) for music.

        separate : bool
        Whether you want the notes for each segment to be played separately
        or as a chord.

        randomize : bool
        Whether you want the segments to be randomized before adding their
        respective notes to the MIDI file. Otherwise, the notes will play in
        order of size (large to small) so the music will always be ascending
        (low notes to high notes).

        '''

        # Read in JSON file
        with open(self.json_file, 'r') as file:
            self.data = json.load(file)

        # Create a MIDIFile object
        midi = MIDIFile()
    
        # Add a track to the MIDI file
        midi.addTrackName(track_num, 0, track_name)

        # Set the tempo (in BPM)
        midi.addTempo(track_num, 0, tempo)

        instrument = 1 
        midi.addProgramChange(track_num, channel, 0, instrument)

        separate_count = 0
        chord_count = 0
        print(len(self.data))
        for frame in self.data:
            if randomize:
                random.shuffle(frame)
            for segment in range(len(frame)):
                amplitude = frame[segment]['segment']['midi_amp']
                frequency = frame[segment]['segment']['frequency']
                # print(amplitude, frequency)
                note = self.freq_to_midi(frequency)
                num_chords = len(frame)
                print(num_chords)

                if separate:
                    # Add a note-on event
                    midi.addNote(track_num, channel, note, separate_count, 1, amplitude)

                    # Add a note-off event
                    midi.addNote(track_num, channel, note, separate_count + 1, 1, 0)

                    separate_count = separate_count + 1

                if not separate:
                    # Add a note-on event
                    midi.addNote(track_num, channel, note, chord_count, 1, amplitude)

                    # Add a note-off event
                    midi.addNote(track_num, channel, note, chord_count + 1, 1, 0)

            if not separate:
                chord_count = chord_count + 2 

        # Save the MIDI file
        with open(self.output_file, "wb") as midi_file:
            midi.writeFile(midi_file)
