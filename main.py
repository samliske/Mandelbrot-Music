import numpy as np
from mido import Message, MidiFile, MidiTrack

def mandelbrot(h, w, max_iter):
    x = np.linspace(-2, 1, w).reshape((1, w))
    y = np.linspace(-1.5, 1.5, h).reshape((h, 1))
    c = x + 1j * y
    z = np.zeros((h, w), dtype=np.complex128)
    output = np.zeros((h, w), dtype=int)
    
    for i in range(max_iter):
        z = z ** 2 + c
        mask = (np.abs(z) > 2)
        output[mask & (output == 0)] = i
        z[mask] = 2
    
    return output

def generate_midi(output, filename):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    pentatonic_scale = [0, 2, 4, 7, 9]

    for row in output:
        for val in row:
            if val != 0:
                octave = val // len(pentatonic_scale)
                note_index = val % len(pentatonic_scale)
                note = octave * 12 + pentatonic_scale[note_index] + 60
                
                if 0 <= note <= 127:
                    track.append(Message('note_on', note=note, velocity=64, time=32))
                    track.append(Message('note_off', note=note, velocity=0, time=32))
    
    mid.save(filename)

# Generate Mandelbrot set
width, height = 800, 600
max_iterations = 100
mandelbrot_output = mandelbrot(height, width, max_iterations)

# Generate MIDI file
output_file = 'mandelbrot.mid'
generate_midi(mandelbrot_output, output_file)

print(f"MIDI file '{output_file}' generated successfully.")