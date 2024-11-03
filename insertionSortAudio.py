import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import simpleaudio as sa
import wave
import struct

# Data initialization
N = 25
xR = np.arange(0, N, 1)
lst = np.linspace(1, 100, N)
np.random.shuffle(lst)

fig, ax = plt.subplots()
ax.set_axis_off()
plt.gcf().set_facecolor('black')
barplot = ax.bar(xR, lst, color='green')

# Parameters for audio
min_freq = 220  # Minimum frequency for the leftmost bar
max_freq = 880  # Maximum frequency for the rightmost bar
frame_rate = 44100  # Standard frame rate for audio

# Insertion Sort Logic for Animation
def insertion_sort_animation():
    n = len(lst)
    steps = []  # List to store the sorting steps (each step is a snapshot of lst state)

    for i in range(1, n):
        key = lst[i]
        j = i - 1
        
        # Capture initial state before moving
        current_state = lst.copy()
        bar_colors = ['green'] * N
        bar_colors[i] = 'blue'  # The bar being inserted is blue
        for k in range(i):
            bar_colors[k] = 'white'  # Already sorted bars turn white
        steps.append((current_state, bar_colors, i))
        
        # Insertion sort logic with visible bar movement
        while j >= 0 and key < lst[j]:
            lst[j+1] = lst[j]  # Shift the bar to the right
            
            # Capture state after each shift
            current_state = lst.copy()
            bar_colors = ['green'] * N
            bar_colors[j] = 'blue'  # Bar being compared is blue
            bar_colors[j+1] = 'red'  # The moved bar turns red
            for k in range(i):
                if k != j+1:
                    bar_colors[k] = 'white'  # Already sorted bars turn white
            steps.append((current_state, bar_colors, j))
            
            j -= 1
        
        lst[j+1] = key
        
        # Capture state after insertion
        current_state = lst.copy()
        bar_colors = ['green'] * N
        bar_colors[j+1] = 'red'  # The inserted bar turns red
        for k in range(i+1):
            if k != j+1:
                bar_colors[k] = 'white'  # Already sorted bars turn white
        steps.append((current_state, bar_colors, j+1))

        if i == n-1:
            # After sorting, turn all bars green one by one
            for k in range(N):
                steps.append((lst.copy(), ['green' if m <= k else 'white' for m in range(N)], k))  # Use `k` for sound

    return steps

# Generate sound for each frame based on bar position
def generate_sound(frequency, duration=0.05):
    t = np.linspace(0, duration, int(frame_rate * duration), False)
    audio_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    audio_wave *= 32767 / np.max(np.abs(audio_wave))  # Normalize to 16-bit range
    audio_wave = audio_wave.astype(np.int16)
    return audio_wave

# Combine all sounds into a single audio file
def combine_sounds(sounds):
    all_audio = np.concatenate(sounds)
    return all_audio

# Save the audio to a WAV file
def save_wavefile(filename, data):
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # Two bytes per sample
        wf.setframerate(frame_rate)
        wf.writeframes(data.tobytes())

# Get sorting steps
sorting_steps = insertion_sort_animation()

# Prepare audio
audio_frames = []

# Animation update function
def update(frame):
    current_lst, current_colors, current_j = sorting_steps[frame]
    ax.cla()  # Clear axis to redraw
    ax.set_axis_off()
    barplot = ax.bar(xR, current_lst, color=current_colors)
    plt.gcf().set_facecolor('black')

    # Generate sound based on the current bar position
    if current_j >= 0:
        # Calculate frequency based on the current bar's position (mapping position to frequency range)
        freq = min_freq + (max_freq - min_freq) * (current_j / (N - 1))
        sound_wave = generate_sound(freq)
        audio_frames.append(sound_wave)

# Create the animation
anim = FuncAnimation(fig, update, frames=len(sorting_steps), interval=50, repeat=False)

# Save animation as video
anim.save("insertion_sort_animation.mp4", writer='ffmpeg', dpi=200)

# Combine and save the audio frames
combined_audio = combine_sounds(audio_frames)
save_wavefile('insertion_sort_audio.wav', combined_audio)

# Merge audio and video using ffmpeg (run this command in the terminal after)
# ffmpeg -i insertion_sort_animation.mp4 -i insertion_sort_audio.wav -c:v copy -c:a aac output_with_audio.mp4
