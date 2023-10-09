# Space-Apps-Hackathon-Sonification-Challenge

[Link to Project Presentation](https://docs.google.com/presentation/d/1N4Q_3RL41o3zjiXu680vd1VnKz-Jf7EaLle2ejpjzJc/edit?usp=sharing)

## Overview
This project was conceived to devise a methodology to sonify 3D NASA space datasets, aiming to provide a unique auditory and visual experience. The primary objective is to make space data more accessible to the general public, especially to the visually impaired, artists, and creators. The process of sonification is broken down into six main steps, from reading the data to saving the sonification to a MIDI file. Through this method, a 3D immersive sound experience is created, where the size and color of space objects are translated into musical notes and their amplitudes. This initiative aligns with NASA's goal of enhancing public engagement with space data, offering a fresh tool for crafting multimodal sensory experiences.

## Features

- Frame-by-frame processing of NASA's image data and fly-through videos into MIDI audio files.
- A user-friendly interface for selecting any image for processing.
- Utilizes the Segment Anything Model (SAM) by Meta AI for image segmentation.
- Generation of frequency and amplitude for each segment based on size and color.
- MIDI file generation for each processed image or video frame.
- Modular design for easy expansion and customization.

## Implementation

1. **Data Reading**:
   - Locate and read in the 3D space datasets from NASA.
   
2. **Segmentation**:
   - Segment the data to identify objects and collect essential attributes like size, color, and position.
   
3. **Musical Note Assignment**:
   - Assign a musical note (frequency) and octave (amplitude) based on the size and color of each object.
   
4. **Sonification Creation**:
   - Create a sonification based on the assigned note and octave for each object.
   
5. **MIDI File Saving**:
   - Save the sonification to a MIDI file for each image or video frame.
   
6. **3D Sound Experience**:
   - Experience a 3D immersive sound that corresponds to the visual dimensionality of the space datasets.

## Usage

1. **User Interface**:
   - Select any image or video frame, which will then be passed to our segmenting model for processing.
   
2. **JSON Communication**:
   - Our modules communicate using JSON blobs, making it easy to replace or expand functionalities without substantial refactoring.
   
3. **MIDI File Output**:
   - The generated MIDI files can be further modified or enhanced using open-source MIDI applications like GarageBand or MuseScore.

4. **Customization**:
   - Our modular approach allows for the replacement of the final module with one that outputs to physical sensory devices, broadening the scope of sensory experiences.

## Technology Stack

- **Language**: Python 3.10
- **Libraries**: Segment Anything Model (SAM) by Meta AI, MIDIUtil by Mark Conway Wirt

## Installation



## Contribution

We have laid down a foundation for anyone to experience space in a new, immersive way. We encourage further development to cater to both scientific and creative needs, leveraging the modularity of our solution for continuous innovation.


---

The project is aimed at delivering a blend of science, creativity, and inclusivity, opening up new avenues for individuals to interact with and perceive space data. By following the instructions provided in the README, you can easily replicate the project and possibly extend it to meet specific requirements or explore new dimensions of sonifications.
