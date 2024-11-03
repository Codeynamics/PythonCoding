import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from pydub import AudioSegment
from pydub.playback import play
import moviepy.editor as mp

# Data initialization
N = 15
xR = np.arange(0, N, 1)
lst = np.linspace(1, 100, N)
np.random.shuffle(lst)

fig, ax = plt.subplots()
ax.set_axis_off()
plt.gcf().set_facecolor('black')
barplot = ax.bar(xR, lst, color='green')

# Function to generate a tone for each bar
def generate_tone(frequency, duration=100):
    """Generate a tone using a sine wave"""
    sine_wave = AudioSegment.sine(frequency=frequency, duration=duration)
    return sine_wave

# Bubble Sort Logic for Animation
def bubble_sort_animation():
    n = len(lst)
    steps = []  # List to store the sorting steps (each step is a snapshot of lst state)
    
    for i in range(n):
        for j in range(0, n-i-1):
            # Snapshot of current comparison
            current_state = lst.copy()
            bar_colors = ['green'] * N
            bar_colors[j] = 'blue'
            for k in range(n-i, n):
                bar_colors[k] = 'white'
            steps.append((current_state, bar_colors, j))  # Add index j to trigger sound
            
            # Swap if out of order
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
        
        if i == n-1:
            # After sorting, turn all bars green one by one
            for k in range(N):
                steps.append((lst.copy(), ['green' if m <= k else 'white' for m in range(N)], None))

    return steps

# Get sorting steps
sorting_steps = bubble_sort_animation()

# Animation update function
def update(frame):
    current_lst, current_colors, pointer = sorting_steps[frame]
    ax.cla()  # Clear axis to redraw
    ax.set_axis_off()
    barplot = ax.bar(xR, current_lst, color=current_colors)
    plt.gcf().set_facecolor('black')
    
    # Trigger sound if the pointer (blue bar) is present
    if pointer is not None:
        # Frequency of the sound is proportional to the value in the bar
        frequency = 100 + int(lst[pointer]) * 10  # Example: scale bar value to frequency
        tone = generate_tone(frequency)
        play(tone)  # Play the sound

# Create the animation
anim = FuncAnimation(fig, update, frames=len(sorting_steps), interval=100, repeat=False)

# Save animation as MP4 (GIF doesn't support audio)
anim.save("bubble_sort_animation.mp4", writer='ffmpeg', dpi=200)

# Combine video and audio using moviepy
video = mp.VideoFileClip("bubble_sort_animation.mp4")
video = video.set_audio(None)  # Remove any default audio

# Save the final video file
final_clip = video.set_duration(video.duration)  # Sync video and audio duration
final_clip.write_videofile("bubble_sort_animation_with_audio.mp4", codec="libx264")
