import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Data initialization
N = 25
xR = np.arange(0, N, 1)
lst = np.linspace(1, 100, N)
np.random.shuffle(lst)

fig, ax = plt.subplots()
ax.set_axis_off()
plt.gcf().set_facecolor('black')
barplot = ax.bar(xR, lst, color='green')

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
            steps.append((current_state, bar_colors))
            
            # Swap if out of order
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
        
        if i == n-1:
            
            # After sorting, turn all bars green one by one
            for k in range(N):
                steps.append((lst.copy(), ['green' if m <= k else 'white' for m in range(N)]))

            '''
            for k in range(N):
                colors = []
                for m in range(N):
                    if m <= k:
                        colors.append('green')
                    else:
                        colors.append('white')
                steps.append((lst.copy(), colors))
            '''
    
    return steps

# Get sorting steps
sorting_steps = bubble_sort_animation()

# Animation update function
def update(frame):
    current_lst, current_colors = sorting_steps[frame]
    ax.cla()  # Clear axis to redraw
    ax.set_axis_off()
    barplot = ax.bar(xR, current_lst, color=current_colors)
    plt.gcf().set_facecolor('black')

# Create the animation
anim = FuncAnimation(fig, update, frames=len(sorting_steps), interval=50, repeat=False)

# Save animation as GIF
anim.save("bubble_sort_animation.mp4", writer='ffmpeg', dpi=200)

# To display the animation, you can use:
# plt.show()
