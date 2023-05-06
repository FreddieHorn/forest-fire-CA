import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import animation
import numpy as np

iterations = 50
neighbourhood = ((-1,0), (0,-1), (0, 1), (1,0))
colors_list = [(0.2,0,0), (0,0.5,0), (1,0,0), 'orange']
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3]
norm = colors.BoundaryNorm(bounds, cmap.N)
forest_fraction = 0.0
q = 0.5 #1 - induced growth. 
f = 0.0001
p = 0.0001

def iterate(X):
    """Iterate the forest according to the forest-fire rules."""

    # The boundary of the forest is always empty, so only consider cells
    # indexed from 1 to nx-2, 1 to ny-2
    ashes_count = np.count_nonzero(X == 0)
    tree_count = np.count_nonzero(X == 1)
    fire_count = np.count_nonzero(X == 2)
    out_file.write(f"{ashes_count} {tree_count} {fire_count}\n")
    print(f"{ashes_count} {tree_count} {fire_count}\n")
    X1 = np.zeros((nx, ny))
    for ix in range(0,nx):
        for iy in range(0,ny):

            if X[iy,ix] == 0 and np.random.random() <= p: #growth of a random forest
                X1[iy,ix] = 1
            elif X[iy,ix] == 0:
                for dx,dy in neighbourhood:
                    if X[(iy+dy)%ny,(ix+dx)%nx] == 1 and np.random.random() < q: #induced growth rate
                        X1[iy,ix] = 1
                        break

            if X[iy,ix] == 1:
                X1[iy,ix] = 1
                for dx,dy in neighbourhood:
                    if X[(iy+dy)%ny,(ix+dx)%nx] == 2:
                        X1[iy,ix] = 2
                        break
                else:
                    if np.random.random() <= f:
                        X1[iy,ix] = 2
    return X1

nx, ny = (100, 100)
X  = np.zeros((ny, nx))
#X[0:ny, 0:nx] = np.random.randint(0, 2, size=(ny, nx))
#X[0:ny, 0:nx] = np.random.random(size=(ny, nx)) < forest_fraction

fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(X, cmap=cmap, norm=norm)#, interpolation='nearest')

# The animation function: called to produce a frame for each generation.
def animate(i):
    im.set_data(animate.X)
    animate.X = iterate(animate.X)
# Bind our grid to the identifier X in the animate function's namespace.
animate.X = X

out_file = open("forest_fire_output.txt", "w")
# Interval between frames (ms).
interval = 100
anim = animation.FuncAnimation(fig, animate, interval=interval, frames=iterations, repeat = False)
plt.show()
out_file.close()

