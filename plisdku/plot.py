import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

def imshow(img, *args, **kwargs):
    """
    Call matplotlib.pyplot.imshow() with adjusted extent.

    Image extent will be changed so pixels 0, 1, 2, ... will be centered at 0, 1, 2, ...
    
    Standard imshow extent puts the left edge of the leftmost pixels at extents[0].  This
    will put the center of the leftmost pixel at extent[0] instead.
    
    New named arguments x and y are provided a la Matlab.  These are the center positions
    of the pixels in "real" coordinates.  x and y should be arrays and only the first and
    last elements of x and y are actually used.

    X INCREASES AS COLUMN NUMBER INCREASES
    Y INCREASES AS ROW NUMBER INCREASES

    Therefore, unless origin="lower" is provided, the y axis will have y[-1] at
    the bottom and y[0] at the top.
    """
    
    if "extent" not in kwargs:
        extent = [-0.5, img.shape[1]-0.5, img.shape[0]-0.5, -0.5]
        
        def extent_1d(x):
            nx = len(x)
            x0 = x[0]
            x1 = x[nx-1]
            
            if nx == 2:
                dx = x1-x0
            else:
                dx = (x1-x0)/(nx-1)

            return [x0-dx/2, x1+dx/2]
        
        if "x" in kwargs:
            extent[0:2] = extent_1d(kwargs["x"])
            del kwargs["x"]
        if "y" in kwargs:
            extent[2:4] = extent_1d(kwargs["y"])
            del kwargs["y"]

        if "origin" not in kwargs or kwargs["origin"] != "lower":
            extent[2:4] = extent[3], extent[2]
        # if "origin" in kwargs and kwargs["origin"] == "lower":

        kwargs["extent"] = extent
    
    return plt.imshow(img, *args, **kwargs)


def pltbox(bounds, *args, **kwargs):
    """
    Plot a box from bounds.  Bounds is [[x0,y0],[x1,y1]].
    """
    b = np.array(bounds)
    x = b[[0, 1, 1, 0, 0], 0]
    y = b[[0, 0, 1, 1, 0], 1]
    return plt.plot(x, y, *args, **kwargs)


def patches(faces, vertices, **kwargs):
    v = [[vertices[f,:] for f in face] for face in faces]
    p3d = art3d.Poly3DCollection(v)
    
    # ALPHA MUST BE SET BEFORE COLOR!!!  or it will be ignored.  (Nice one guys.)
    if 'alpha' in kwargs:
        p3d.set_alpha(kwargs['alpha'])
    if 'edgecolor' in kwargs:
        p3d.set_edgecolor(kwargs['edgecolor'])
    if 'facecolor' in kwargs:
        p3d.set_facecolor(kwargs['facecolor'])
    else:
        p3d.set_facecolor('C0') # this is to make sure that the alpha is changed.
    
    plt.gca().add_collection(p3d)

def colorbar(mappable):
    """
    by Joseph Long
    https://joseph-long.com/writing/colorbars/
    """
    ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    return fig.colorbar(mappable, cax=cax)
