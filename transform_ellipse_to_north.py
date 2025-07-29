def transform_ellipse_to_north(ellipse_points):
    """
    Apply transformation to each point in the ellipse:
    - If y < 0: (|y|, x)
    - If y == 0: (x, 0)
    - If y > 0: (-x, y)
    """
    
    import numpy as np

    x = ellipse_points[:, 0]
    y = ellipse_points[:, 1]

    # Initialize empty arrays
    x_new = np.zeros_like(x)
    y_new = np.zeros_like(y)

    # Case 1: y < 0
    mask_neg = y < 0
    x_new[mask_neg] = np.abs(y[mask_neg])
    y_new[mask_neg] = x[mask_neg]

    # Case 2: y == 0
    mask_zero = y == 0
    x_new[mask_zero] = 0
    y_new[mask_zero] = x[mask_zero]

    # Case 3: y > 0
    mask_pos = y > 0
    x_new[mask_pos] = -y[mask_pos]
    y_new[mask_pos] = x[mask_pos]

    return np.stack((x_new, y_new), axis=1)
