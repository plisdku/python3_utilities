import matplotlib.pyplot as plt

def imshow(img, *args, **kwargs):
    """
    Call matplotlib.pyplot.imshow() with adjusted extent.

    Image extent will be changed so pixels 0, 1, 2, ... will be centered at 0, 1, 2, ...
    
    Standard imshow extent puts the left edge of the leftmost pixels at extents[0].  This
    will put the center of the leftmost pixel at extent[0] instead.
    
    New named arguments x and y are provided a la Matlab.  These are the center positions
    of the pixels in "real" coordinates.  x and y should be arrays and only the first and
    last elements of x and y are actually used.
    """
    
    if "extent" not in kwargs:
        extent = [-0.5, img.shape[1]-0.5, -0.5, img.shape[0]-0.5]
        
        def extent_1d(x):
            nx = len(x)
            x0 = x[0]
            x1 = x[nx-1]
            
            if nx == 2:
                dx = x1-x0
            else:
                dx = (x1-x0)/nx
            
            return [x0-dx/2, x1+dx/2]
        
        if "x" in kwargs:
            extent[0:2] = extent_1d(kwargs["x"])
            del kwargs["x"]
        if "y" in kwargs:
            extent[2:4] = extent_1d(kwargs["y"])
            del kwargs["y"]
        
        kwargs["extent"] = extent
    
    return plt.imshow(img, *args, **kwargs)
