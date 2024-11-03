import matplotlib.pyplot as plt
import numpy as np

N = 10

xR = np.arange(0,N,1)
lst = np.linspace(1,100,N)
np.random.shuffle(lst)

n = len(lst)
for i in range(n):
    for j in range(0, n-i-1):
        barplot = plt.bar(xR,lst, color='green')
        barplot[j].set_color('blue')
        for k in range(n-i,n):
            barplot[k].set_color('white')
            
        plt.gcf().set_facecolor('black')
        plt.axis('off')
        plt.pause(0.001)
        plt.clf()
        if lst[j] > lst[j+1]:
            lst[j], lst[j+1] = lst[j+1], lst[j]
    
    if i==n-1:
        barplot = plt.bar(xR,lst, color='white')
        plt.gcf().set_facecolor('black')
        plt.axis('off')
        for k in range(n):
            barplot[k].set_color('green')
            plt.pause(0.1)
            plt.gcf().set_facecolor('black')
            plt.axis('off')
        
plt.show()