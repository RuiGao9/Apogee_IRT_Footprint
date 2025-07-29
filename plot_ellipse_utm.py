def plot_ellipse_utm(ellipse_points, title="Final IRT Footprint (UTM)"):
    '''
    Display the final footprint.
    '''
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 6))
    plt.plot(ellipse_points[:, 0], ellipse_points[:, 1], 'b-', label='Ellipse')
    plt.scatter(ellipse_points[:, 0].mean(), ellipse_points[:, 1].mean(), color='red', label='Ellipse Center')
    plt.xlabel("Easting (m)")
    plt.ylabel("Northing (m)")
    plt.title(title)
    plt.gca().set_aspect('equal')
    plt.legend()
    plt.grid(True)
    plt.show()