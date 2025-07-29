def plot_rotated_ellipse(ellipse_points, center_beam, center_x):
    '''
    Display the rotated ellipse/cycle on the Cartesian coordinate system.
    '''
    
    import matplotlib.pyplot as plt
    
    print("Dimension of the ellipse is:",ellipse_points.ndim)
    print("Dimension of the center beam point is:",center_beam.ndim)
    print("Dimension of the ellipse center point is:",center_x.ndim)
    plt.figure(figsize=(8, 6))
    plt.plot(ellipse_points[:, 0], ellipse_points[:, 1], label="Projected Footprint", color='blue')
    plt.plot(center_x[:, 0], center_x[:, 1], 'ro', label='Ellipse Center')
    plt.plot(center_beam[:, 0], center_beam[:, 1], 'bo', label='Beam Center')
    plt.axhline(0, color='gray', linestyle='--')
    plt.axvline(0, color='gray', linestyle='--')
    plt.gca().set_aspect('equal')
    plt.xlabel("X (meters)")
    plt.ylabel("Y (meters)")
    plt.title("Infrared Sensor Ground Footprint (Projected Ellipse)")
    plt.grid(True)
    plt.legend()
    plt.show()