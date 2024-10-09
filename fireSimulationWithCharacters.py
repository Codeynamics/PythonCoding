# Run in an IDE. 
# VS Code is perfect
# Isn't working in colab for me. 
# Nor in Jupyter Notebook

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip

fireChars = " ,;+ltgti!lI?/\\|)(1}{][rcvzjftJUOQocxfXhqwWB8&%$#@"
maxCharIndex = len(fireChars)
width, height = 145, 28
firePixelsArray = np.zeros((height, width), dtype=int)

font = ImageFont.load_default()

# Colors
colors = [
    (255, 165, 000),    # orange
    (255, 223, 000),    # yellow
    (  4, 217, 255),    # light blue
    (144, 238, 144),    # Green
    (255, 255, 255)     # white
]

# Color assigning fn
def get_color(index):
    # assign based on intensity
    if index < maxCharIndex * 0.20:
        return colors[0]  # orange
    elif index < maxCharIndex * 0.30:
        return colors[1]  # yellow
    elif index < maxCharIndex * 0.40:
        return colors[2]  # light blue
    elif index < maxCharIndex * 0.60:
        return colors[3]  # Light Green
    else:
        return colors[4]  # white

def generate_fire_frame():
    # Bottom row random values. Will be unchanged
    for i in range(width):
        firePixelsArray[-1, np.random.randint(0, width)] = np.random.randint(0, maxCharIndex)

    # Assign random values in the 5th row from last to space. or 0 in value (simulate cooling down)
    for i in range(width):
        firePixelsArray[-5, np.random.randint(0, width)] = 0

    # propagate the fire upwards
    for y in range(height - 1):
        for x in range(width - 1):
            average_value = (
                firePixelsArray[y, x]
                + firePixelsArray[y + 1, x]
                + firePixelsArray[y, x + 1]
                + firePixelsArray[y + 1, x + 1]
            ) / 4
            firePixelsArray[y, x] = int(average_value)

    # Take photo of the image and draw it in the frame
    img = Image.new('RGB', (width * 10, height * 18), 'black')  # Scale up for better visibility
    draw = ImageDraw.Draw(img)

    # Draw the char based on the pixed value
    for y in range(height):
        for x in range(width):
            char = fireChars[firePixelsArray[y, x]]
            color = get_color(firePixelsArray[y, x])  # Get color based on pixel value
            draw.text((x * 10, y * 18), char, fill=color, font=font)
    return img

# Generate frames for 20 seconds of video at 15 fps
frames = []
fps = 15
num_frames = fps * 20

for _ in range(num_frames):
    frame = generate_fire_frame()
    frames.append(frame)

# Save the frames
clip = ImageSequenceClip([np.array(f) for f in frames], fps=fps)
clip.write_videofile("fire_chars.mp4", codec="libx264", fps=fps)
