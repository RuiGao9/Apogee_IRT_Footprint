def rotate_ellipse_local(ellipse_points, center_point, angle_deg):
    """
    Rotate the ellipse around a center point (the IRT sensor location) in the Cartesian coordinate system.
    Based on the user defined horizontal angle (variable "beta_irt_horizontal" in the main program), rotate all points on the ellipse based on the center point of the Cartesian coordinate system.

    Parameters:
    - ellipse_points: Nx2 array of (x, y) coordinates
    - center_point: (0, 0), center of rotation (the IRT sensor location)
    - angle_deg: rotation angle in degrees (0=north, 90=east, clockwise)

    Returns:
    - rotated_points: Nx2 array of rotated coordinates
    """

    import numpy as np

    angle_deg = 360 - angle_deg # My math needs to be improved!!!
    
    angle_rad = np.radians(angle_deg)
    cos_theta = np.cos(angle_rad)
    sin_theta = np.sin(angle_rad)
    x0, y0 = center_point

    # Shift points to origin
    shifted = ellipse_points - np.array([x0, y0])

    # Apply rotation
    x_rot = shifted[:, 0] * cos_theta - shifted[:, 1] * sin_theta
    y_rot = shifted[:, 0] * sin_theta + shifted[:, 1] * cos_theta

    # Shift back
    rotated = np.stack((x_rot + x0, y_rot + y0), axis=1)
    return rotated
