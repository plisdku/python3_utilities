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



# def interp_weights_1d(x, x_query):

#     idx_right = np.searchsorted(x, x_query)
#     idx_left = idx_right-1
#     weight_left = np.zeros_like(x_query)
#     b_valid = np.logical_and(idx_right > 0, idx_left < len(x)-1)
#     weight_left[b_valid] = (x[idx_right[b_valid]] - x_query[b_valid]) / (x[idx_right[b_valid]] - x[idx_left[b_valid]])
    
#     idx_out = np.arange(len(x_query))[b_valid]
    
#     return weight_left[b_valid], idx_out, idx_left[b_valid]

# def interp_matrix_elements_1d(x, x_query):
#     w_left, row, col = interp_weights_1d(x, x_query)
#     w_right = 1.0 - w_left

#     vals = np.concatenate((w_left, w_right))
#     rows = np.concatenate((row,row))
#     cols = np.concatenate((col, col+1))
    
#     return vals, rows, cols

def interp_weights_nd(x_query, *xy_grid):
    """
    Return linear interpolation weights for N-d points x_query in grid given by *xy_grid.
    
    Example:
    weight_left, idx_out, idx_left = interp_weights_nd(xy_query, xs, ys, zs, ws, ...)
    """
    x_query = np.asarray(x_query)

    ndim = len(xy_grid)

    if x_query.ndim < 2:
        if ndim > 1:
            x_query = x_query[None,...]
        else:
            x_query = x_query[...,None]


    npts = x_query.shape[0]
    ndim = x_query.shape[1]
    
    b_valid = np.ones(npts, dtype=bool)
    
    idx_right = np.zeros_like(x_query, dtype=int)
    
    for dd in range(ndim):
        idx_r = np.searchsorted(xy_grid[dd], x_query[:,dd])
        b_valid = b_valid * (idx_r > 0) * (idx_r < len(xy_grid[dd]))
        idx_right[:,dd] = idx_r
    
    idx_left = idx_right - 1
    
    weight_left = np.zeros((npts, ndim))
    
    for dd in range(ndim):
        idx = idx_right[b_valid, dd]
        x_right = xy_grid[dd][idx]
        x_left = xy_grid[dd][idx-1]
        x_q = x_query[b_valid,dd]
        weight_left[b_valid,dd] = (x_right - x_q) / (x_right - x_left)
    
    idx_out = np.arange(npts)[b_valid]
    return weight_left[b_valid,:], idx_out, idx_left[b_valid,:]

def interp1(x_query, z, x_grid):

    w_left, idx_out, idx_left = interp_weights_nd(x_query, (x_grid))
    w_right = 1.0 - w_left

    v_out = np.zeros_like(x_query)
    v_out[idx_out] = w_left*z[idx_left] + w_right*z[idx_left+1]
    return v_out


def bilinear_weights(xy_query, *xy_grid):
    w_left, idx_out, idx_left = interp_weights_nd(xy_query, *xy_grid)
    w_right = 1.0 - w_left
    
    w00 = w_left[:,0]*w_left[:,1]
    w10 = w_right[:,0]*w_left[:,1]
    w01 = w_left[:,0]*w_right[:,1]
    w11 = w_right[:,0]*w_right[:,1]

    return w00, w10, w01, w11, idx_out, idx_left


def interp2(xy_query, grid_values, *xy_grid):

    w00, w10, w01, w11, idx_out, idx_left = bilinear_weights(xy_query, *xy_grid)

    v_out = np.zeros(xy_query.shape[0])
    v_out[idx_out] = w00*grid_values[idx_left[:,0], idx_left[:,1]] + \
        w10*grid_values[idx_left[:,0]+1, idx_left[:,1]] + \
        w11*grid_values[idx_left[:,0]+1, idx_left[:,1]+1] + \
        w01*grid_values[idx_left[:,0], idx_left[:,1]+1]
    return v_out

def adjoint_interp2(xy_query, values, *xy_grid, **kwargs):
    
    w00, w10, w01, w11, idx_out, idx_left = bilinear_weights(xy_query, *xy_grid)
    
    if "out" in kwargs:
        out = kwargs["out"]
    else:
        out = np.zeros([len(g) for g in xy_grid])
    
    if np.isscalar(values):
        # To correctly handle repeated indices, use np.add.at.
        np.add.at(out, [idx_left[:,0], idx_left[:,1]], w00*values)
        np.add.at(out, [idx_left[:,0]+1, idx_left[:,1]], w10*values)
        np.add.at(out, [idx_left[:,0], idx_left[:,1]+1], w01*values)
        np.add.at(out, [idx_left[:,0]+1, idx_left[:,1]+1], w11*values)

        # out[idx_left[:,0], idx_left[:,1]] += w00*values
        # out[idx_left[:,0]+1, idx_left[:,1]] += w10*values
        # out[idx_left[:,0]+1, idx_left[:,1]+1] += w11*values
        # out[idx_left[:,0], idx_left[:,1]+1] += w01*values
    else:
        # To correctly handle repeated indices, use np.add.at.
        np.add.at(out, [idx_left[:,0], idx_left[:,1]], w00*values[idx_out])
        np.add.at(out, [idx_left[:,0]+1, idx_left[:,1]], w10*values[idx_out])
        np.add.at(out, [idx_left[:,0], idx_left[:,1]+1], w01*values[idx_out])
        np.add.at(out, [idx_left[:,0]+1, idx_left[:,1]+1], w11*values[idx_out])

        # out[idx_left[:,0], idx_left[:,1]] += w00*values[idx_out]
        # out[idx_left[:,0]+1, idx_left[:,1]] += w10*values[idx_out]
        # out[idx_left[:,0]+1, idx_left[:,1]+1] += w11*values[idx_out]
        # out[idx_left[:,0], idx_left[:,1]+1] += w01*values[idx_out]
    
    return out

