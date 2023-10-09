import json
import math
import numpy as np
import re


def get_segments(filename: str) -> list:
    """
        Author: Sherwyn Braganza

        Open the JSON file that contains the segmented frames of the
        video.

        :param filename: str
            Name of the JSON file to open
        :return: list
            List of a list of image segments from different frames
    """
    with open(filename, "r") as file:
        segments = json.load(file)
    return segments


def strip_newlines(input_string):
    return re.sub(r'\r?\n', '', input_string)


def get_size_stats(segments: list) -> (float, float, float):
    """
        Author: Sherwyn Braganza

        Get statistical measures of the segments pertaining to
        a frame.

        :param segments: list
            A list of segments in JSON format
        :return: (float, float, float)
            Floats corresponding to the mean, standard deviation
            and median of the sements pertaining to a frame
    """
    sizes = np.zeros((len(segments)))
    for idx in range(len(segments)):
        sizes[idx] = (segments[idx]['segment']['pixel_area'])
    mean = np.mean(sizes)
    std = np.std(sizes)
    median = np.median(sizes)
    return mean, std, median


def generate_key_freq_diffs():
    """
        Author: Sherwyn Braganza

        Generate the differences between frequencies of notes next to each other
        and return the resulting list.

        :return: list
            List of frequency differences between correspodning keys
    """
    # Frequencies entered here are the frequencies from C4 to B4
    frequencies_diffs = [261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99,
                         392.00, 415.30, 440.00, 466.15, 493.88]
    for idx in range(len(frequencies_diffs) - 1, 0, -1):
        frequencies_diffs[idx] = frequencies_diffs[idx] - frequencies_diffs[idx - 1]
    frequencies_diffs[0] = 0
    return frequencies_diffs


def regularize(pixel: np.ndarray):
    """
        Author: Sherwyn Braganza

        Convert 3D pixel data to 1D.
        TODO: Use PCA to find best weights to condense dimensions

        :param pixel: np.ndarray
            The RGB values corresponding to a pixel
        :return: int
            The Grayscale Pixel value
    """
    assert pixel.shape == (3,)  # assert a single pixel conversion
    # implement color to grayscale pixel conversion
    return int(0.2989 * pixel[0] + 0.5870 * pixel[1] + 0.1140 * pixel[2])


def shifted_sigmoid(x, median):
    """
        Author: Sherwyn Braganza

        Return the value of x after passing through a sigmoid shifted towards
        the median of the data.

        :param x: float
            The value to be sigmoided
        :param median: float
            The shift amount
        :return: float
            The shifted sigmoided value
    """
    return 1 / (1 + np.exp(-x + median))


def freq_to_midi(freq: float) -> int:
    """
        Author: Sherwyn Braganza

        Convert frequency to MIDI numbers given by
        the formula on https://newt.phys.unsw.edu.au/jw/notes.html

        :param freq: float
            The frequency to be converted
        :return: int
            An integer between 0 and 127 that corresponds to a
            MIDI note
    """
    return int(69 + 12 * math.log(freq / 440, 2))


def amp_to_midiAmp(amp: float) -> int:
    """
        Author: Sherwyn Braganza

        Convert the Amplitude scaling factor to a MIDI output between
        0 and 127. Starts with an initial threshold amplitude of 30
        and scales with a scaling factor of 80 times the amplitude
        assigned to the object

        Parameters
        ----------
        amp : float
          The frequency to be converted

        Returns
        -------
        int

        An integer between 0 and 127 that corresponds to a
        MIDI amplitude value
    """
    assert 0 <= amp <= 1
    base_amplitude = 30  # base amplitude
    amplitude_scaling_fact = 80  # midi amplitude scaling fact
    return int(base_amplitude + amplitude_scaling_fact * amp)


def get_frequency(features: dict, median):
    """
        Author: Sherwyn Braganza

        Converts the segment data into its corresponding frequencies and
        amplitude.

        :param features: dict
            The segment data
        :param median: float
            The median size of the segments from a frame
        :return: tuple(float, float, int, int)
            The amplitude, frequency, midi mapped freq and midi mapped amp of
            the object
    """
    image_shape = (1920, 1080)
    feature_size = features['pixel_area']
    avg_pix = np.array(features['avg_color']).reshape((3,))

    bins = np.linspace(0, 255, 12)
    base_freq = 261.63
    frequencies_diffs = generate_key_freq_diffs()

    amp = shifted_sigmoid(np.log(feature_size), np.log(median))
    octave_scaled = base_freq * (16 ** (0.6 - amp))
    freq = octave_scaled * (1 + frequencies_diffs[regularize(avg_pix) // 255 * 12])
    midi = freq_to_midi(freq)
    midi_amp = amp_to_midiAmp(amp)

    return amp, freq, midi, midi_amp


def sonify(filename: str):
    """
        Author: Sherwyn Braganza

        Wrapper function for all the above functions.
        Unpacks the JSON list and gets frequencies of
        each of the segments in it. Rewrites the
        JSON file with addition params.

        :param filename: str
            the .json file to pull segment data from

        :return: None
    """
    flythrough = get_segments(filename)
    mean, std, median = get_size_stats(flythrough)
    for frame in (flythrough):
        amp, freq, midi, midi_amp = get_frequency(frame['segment'],                                                  median)
        frame['segment'].update({'amplitude': amp, 'frequency': freq,
                                                'midi': midi, 'midi_amp': midi_amp})

    with open('sonified_' + filename, 'w') as ofile:
        json.dump(flythrough, ofile)

    return 'sonified_' + filename + ".json"


if __name__ == '__main__':
    filename = input('Enter the name of the .json file you want to sonify: ')
    sonify(filename)
