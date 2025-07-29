def compute_footprint_ellipse(h, alpha_deg, fov_half_deg=14):
    """
    Returns:
    - OC: The length from the ellipse/cycle to the projected IRT sensor position
    - BE: The length from the beam center to the ellipse on the y-axis
    - OB: The length form the beam center to the projected IRT sensor position
    - CA, CD, AD/2: The semi-major-axis of the ellipse/cycle
    - CF: The semi-minor-axis of the ellipse/cycle
    - np.stack((x_ellipse, y_ellipse), axis=1): get the coordinates of the points on the ellipse boundary
    """
    import numpy as np

    # Convert angles
    alpha = np.radians(alpha_deg)
    fov_half = np.radians(fov_half_deg)

    ###=== Information about the where the IRT sensor point out to (beam center OB) ===###
    ###=== It is a calculation about triangle ===###
    print("Information about the beam center:")
    # Beam center from where the IRT sensor located, not the center of the ellipse
    OB = h * np.tan(alpha)
    # The distance from the ellipse to the beam center on the y-axis direction, BE (not the center of the ellipse)
    BE = h * np.tan(fov_half) / np.cos(alpha)
    print(f"The distance from the beam center to the IRT sensor location is (OB): {OB:.3f}")
    print(f"The distance from the beam center to the ellipse boundary is (BE): {BE:.3f}")

    ###=== Information about the ellipse center and boundary ===###
    ###=== It is a calculation about Focus-Eccentricity Relationship (ellipse) ===###
    print("\nInformation about the ellipse:")
    # The longest distance between the projected IRT location and the point on the ellipse, OD
    OD = h * np.tan(alpha+fov_half)
    print(f"The distance from the IRT projected location to the farthest point on the ellipse (OD): {OD:.3f}")
    # The shortest distance between the projected IRT location and the point on the ellipse, OA
    OA = h * np.tan(alpha-fov_half)
    print(f"The distance from the IRT projected location to the nearest point on the ellipse (OA): {OA:.3f}")
    # The distance between ellipse center to the beam center, BC
    CA = (OD-OA) / 2
    CD = CA
    print(f"The length of the semi-major-axis is (CD or CA): {CD:.3f}")
    OC = CA+OA
    print(f"The distance of the center of the ellipse to the projected IRT sensor is (OC): {OC:.3f}")
    BC = OD - OB - CD
    print(f"The length between beam center and ellipse center (BC): {BC:.3f}")
    # The distance from sensor to the beam center, BH
    BH = np.sqrt(h*h + OB*OB)
    print(f"The length from the sensor to the beam center (BH): {BH:.3f}")
    # The semi-minor axis, CF, 
    # The distance from focus to edge along minor-axis direction
    # (d/b)^2 = 1 - (c/a)^2 which is:
    # b = sqrt(a^2*d^2/(a^2-c^2))
    # a: the semi-major axis
    # b: the semi-minor axis
    # c: the distance between B and C
    # d: the distance between B and E
    # In this case: (BE/CF)^2 = 1 - (BC/CD)^2, which is:
    # CF = sqrt(CD^2*BE^2/(CD^2-BC^2))
    CF = np.sqrt(CD**2 * BE**2 / (CD**2 - BC**2))
    print(f"The length of the semi-minor-axis is (CF): {CF:.3f}")

    # Points on the ellipse for showing the ellipse
    # Let's make a horizontal ellipse first
    theta = np.linspace(0, 2 * np.pi, 1200)
    x_c = OC
    y_c = 0
    x_ellipse = x_c + CD * np.cos(theta)
    y_ellipse = y_c + CF * np.sin(theta)

    return OC, BE, OB, CA, CF, np.stack((x_ellipse, y_ellipse), axis=1)