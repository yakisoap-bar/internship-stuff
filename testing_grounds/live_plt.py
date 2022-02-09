import matplotlib.pyplot as plt
# import matplotlib.animation as ani
# from matplotlib import style

# stuff to generate fake data
import numpy as np

# enable interactive mode
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

with plt.ion():
    data = np.random.rand(7)
    rects = plt.barh(labels, data, align='center')
    while True:
        data = np.random.rand(7)

        for rect, d in zip(rects, data):
            rect.set_width(d)

        plt.draw()
        
        plt.pause(0.5)