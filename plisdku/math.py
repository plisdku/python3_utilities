import numpy as np

def quick_lstsq(a,b):
    return np.linalg.solve(a.T@a, a.T@b)


def bin_average(x, new_shape):
    """
    Average and downsample array x to a new shape.
    """
    shape = np.shape(x)

    factors = np.floor_divide(shape, new_shape)
    tmp_shape = np.column_stack((new_shape, factors)).ravel()
    x_reshaped = x.reshape(tmp_shape)

    x_mean = x_reshaped
    for axis in range(len(tmp_shape)-1, 0, -2):
        x_mean = x_mean.mean(axis)

    return x_mean

