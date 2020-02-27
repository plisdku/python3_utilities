import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

def _pixel_edges(x):
    if len(x) > 1:
        dx = np.diff(x)
        x = np.concatenate(( [x[0]-dx[0]/2], x[:-1] + dx/2, [x[-1]+dx[-1]/2] ))
    else:
        if x[0] == 0:
            x = np.array([-0.5, 0.5])
        else:
            x = np.array([x - 0.5*np.abs(x[0]), x + 0.5*np.abs(x[0])])
    return x

def pcolor(*args, **kwargs):
    """Call matplotlib.pyplot.pcolormesh() so pixels are centered at desired coordinates.
    
    This function is called pcolor for brevity but is indeed pcolormesh inside.

    Matplotlib's pcolormesh extent puts the left edge of the leftmost pixels at x[0].  This
    will put the center of the leftmost pixel at extent[0] instead.
    
    New named arguments x and y are provided a la Matlab.  These are the center positions
    of the pixels in "real" coordinates.  x and y should be arrays and only the first and
    last elements of x and y are actually used.

    X INCREASES AS COLUMN NUMBER INCREASES
    Y INCREASES AS ROW NUMBER INCREASES

    Therefore, unless origin="lower" is provided, the y axis will have y[-1] at
    the bottom and y[0] at the top.
    """
    
    if len(args) == 3:
        x = args[0]
        y = args[1]
        img = args[2]
    elif len(args) == 1:
        img = args[0]
        x = np.arange(img.shape[1])
        y = np.arange(img.shape[0])

    # Get pixel edges.

    x = _pixel_edges(x)
    y = _pixel_edges(y)

    # dx = np.diff(x)
    # dy = np.diff(y)
    # x = np.concatenate(( [x[0]-dx[0]/2], dx + x[0] ))
    # y = np.concatenate(( [y[0]-dy[0]/2], dy + y[0] ))

    # x = np.interp(np.arange(len(x)+1), np.linspace(0, len(x))

    # dx = x[1]-x[0]
    # dy = y[1]-y[0]
    
    # x = np.linspace(x[0]-dx/2, x[-1]+dx/2, len(x)+1)
    # y = np.linspace(y[0]-dy/2, y[-1]+dy/2, len(y)+1)

    if "centered" in kwargs:
        if "vmin" in kwargs:
            vmin = kwargs["vmin"]
        else:
            vmin = img.min()

        if "vmax" in kwargs:
            vmax = kwargs["vmax"]
        else:
            vmax = img.max()

        if "vmax" and "vmin" in kwargs:
            v = max(np.abs(kwargs["vmin"]), np.abs(kwargs["vmax"]))
        elif "vmax" in kwargs:
            v = np.abs(kwargs["vmax"])
        elif "vmin" in kwargs:
            v = np.abs(kwargs["vmin"])
        else:
            v = np.max(np.abs(img))

        vmin = -v
        vmax = v

        del kwargs["centered"]

        kwargs["vmin"] = vmin
        kwargs["vmax"] = vmax

    return plt.pcolormesh(x,y,img, **kwargs)




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

        kwargs["extent"] = extent
    
    if "centered" in kwargs:
        if "vmin" in kwargs:
            vmin = kwargs["vmin"]
        else:
            vmin = img.min()

        if "vmax" in kwargs:
            vmax = kwargs["vmax"]
        else:
            vmax = img.max()

        if "vmax" and "vmin" in kwargs:
            v = max(np.abs(kwargs["vmin"]), np.abs(kwargs["vmax"]))
        elif "vmax" in kwargs:
            v = np.abs(kwargs["vmax"])
        elif "vmin" in kwargs:
            v = np.abs(kwargs["vmin"])
        else:
            v = np.max(np.abs(img))

        vmin = -v
        vmax = v

        del kwargs["centered"]

        kwargs["vmin"] = vmin
        kwargs["vmax"] = vmax

    return plt.imshow(img, *args, **kwargs)
    

def plot_loop(x, y, *args, **kwargs):
    n = len(x)
    ii = np.arange(n+1)%n
    return plt.plot(x[ii], y[ii], *args, **kwargs)


def plot_box(bounds, *args, **kwargs):
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

def colorbar(mappable, size_str=None):
    """
    by Joseph Long
    https://joseph-long.com/writing/colorbars/
    """
    ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)

    if size_str is None:
        size_str = "5%"
    cax = divider.append_axes("right", size=size_str, pad=0.05)
    return fig.colorbar(mappable, cax=cax)


def set_very_nice_rcparams(latex=True):
    # inspired by http://nipunbatra.github.io/2014/08/latexify/

    params = {
        'text.usetex': latex,
        'image.origin': 'lower',
        'image.interpolation': 'nearest',
        # 'image.cmap': 'gray',
        'axes.grid': False,
        'savefig.dpi': 150,  # to adjust notebook inline plot size
        # 'axes.labelsize': 8, # fontsize for x and y labels (was 10)
        # 'axes.titlesize': 8,
        # 'font.size': 8, # was 10
        # 'legend.fontsize': 6, # was 10
        # 'xtick.labelsize': 8,
        # 'ytick.labelsize': 8,
        'figure.figsize': [6,4], #[3.39, 2.10],
        'figure.dpi': 100,
    }
    if latex:
        params.update({
            'text.latex.preamble': ['\\usepackage{gensymb}'],
            'font.family': 'serif'
        })
    else:
        params.update({
            'text.latex.preamble': ['\\usepackage{gensymb}'],
            'font.family': 'sans-serif'
        })

    matplotlib.rcParams.update(params)
