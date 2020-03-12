import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pathos.multiprocessing import Pool


""" https://scipython.com/book/chapter-7-matplotlib/problems/p72/the-julia-set/ """
# Image width and height; parameters for the plot
pool_size = 10
im_height = im_width = 10000
print("image height: ", im_height)

indexes = range(im_width)
len_of_chunk = im_width // pool_size
chunks = [indexes[x:x + len_of_chunk] for x in range(0, len(indexes), len_of_chunk)]

c = complex(-0.1, 0.65)
zabs_max = 10
nit_max = 1000
xmin, xmax = -1.5, 1.5
xwidth = xmax - xmin
ymin, ymax = -1.5, 1.5
yheight = ymax - ymin

def julia_row(ixs):
    inside_julia = np.zeros((im_width, im_height))
    for ix in ixs:
        for iy in range(im_height):
            nit = 0
            # Map pixel position to a point in the complex plane
            z = complex(ix / im_width * xwidth + xmin, iy / im_height * yheight + ymin)
            # Do the iterations
            while abs(z) <= zabs_max and nit < nit_max:
                z = z**2 + c
                nit += 1
            shade = 1-np.sqrt(nit / nit_max)
            ratio = nit / nit_max
            inside_julia[ix, iy] = ratio

    return inside_julia

p = Pool(pool_size)
julias = p.map(julia_row, chunks)
julia = np.array(julias).sum(axis=0)

np.save("julia_fractal", julia)


"""
# without multiprocessing
julia = np.zeros((im_width, im_height))
for ix in range(im_width):
    for iy in range(im_height):
        nit = 0
        # Map pixel position to a point in the complex plane
        z = complex(ix / im_width * xwidth + xmin,
                    iy / im_height * yheight + ymin)
        # Do the iterations
        while abs(z) <= zabs_max and nit < nit_max:
            z = z**2 + c
            nit += 1
        shade = 1-np.sqrt(nit / nit_max)
        ratio = nit / nit_max
        julia[ix, iy] = ratio
"""

fig, ax = plt.subplots()
ax.imshow(julia, interpolation='nearest', cmap=cm.hot)
# Set the tick labels to the coordinates of z0 in the complex plane
xtick_labels = np.linspace(xmin, xmax, xwidth / 0.5)
ax.set_xticks([(x-xmin) / xwidth * im_width for x in xtick_labels])
ax.set_xticklabels(['{:.1f}'.format(xtick) for xtick in xtick_labels])
ytick_labels = np.linspace(ymin, ymax, yheight / 0.5)
ax.set_yticks([(y-ymin) / yheight * im_height for y in ytick_labels])
ax.set_yticklabels(['{:.1f}'.format(ytick) for ytick in ytick_labels])
plt.show()
