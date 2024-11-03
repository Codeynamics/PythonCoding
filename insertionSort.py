import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Data initialization
N = 50
xR = np.arange(0, N, 1)
lst = np.linspace(1, 100, N)
np.random.shuffle(lst)

fig, ax = plt.subplots()
ax.set_axis_off()
plt.gcf().set_facecolor('black')
barplot = ax.bar(xR, lst, color='green')

# Bubble Sort Logic for Animation
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
        steps.append((current_state, bar_colors))
        
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
            steps.append((current_state, bar_colors))
            
            j -= 1
        
        lst[j+1] = key
        
        # Capture state after insertion
        current_state = lst.copy()
        bar_colors = ['green'] * N
        bar_colors[j+1] = 'red'  # The inserted bar turns red
        for k in range(i+1):
            if k != j+1:
                bar_colors[k] = 'white'  # Already sorted bars turn white
        steps.append((current_state, bar_colors))

        # Optionally turn the red bar back to white in the next step
        bar_colors[j+1] = 'white'
        steps.append((lst.copy(), bar_colors))
    
    return steps


# Get sorting steps
sorting_steps = insertion_sort_animation()

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
anim.save("insertion_sort.mp4", writer='ffmpeg', dpi=200)

# To display the animation, you can use:
# plt.show()
