def save_ellipse_as_geotiff(ellipse_utm, filename="IRT_footprint.tif", pixel_size=0.01, value=1):
    """
    Save ellipse as a GeoTIFF image from UTM coordinates.

    Parameters:
    - ellipse_utm: Nx2 numpy array of (x, y) coordinates in UTM.
    - filename: output GeoTIFF file name.
    - pixel_size: resolution in meters.
    - value: value to fill the ellipse area (deafult=1).
    """
    
    import numpy as np
    import rasterio
    from rasterio.features import rasterize
    from shapely.geometry import Polygon
    from rasterio.transform import from_origin

    # Ensure the polygon is closed
    if not np.allclose(ellipse_utm[0], ellipse_utm[-1]):
        ellipse_utm = np.vstack([ellipse_utm, ellipse_utm[0]])  # Close the loop

    # Create polygon from boundary
    polygon = Polygon(ellipse_utm)
    if not polygon.is_valid:
        polygon = polygon.buffer(0)  # Fix self-intersection or degenerate cases

    # Get bounding box
    minx, miny, maxx, maxy = polygon.bounds
    width = int(np.ceil((maxx - minx) / pixel_size))
    height = int(np.ceil((maxy - miny) / pixel_size))

    if width == 0 or height == 0:
        raise ValueError("Invalid dimensions; ellipse might be too small for given pixel size.")

    # Affine transform (top-left corner)
    transform = from_origin(minx, maxy, pixel_size, pixel_size)

    # Rasterize polygon into a binary mask
    mask = rasterize(
        [(polygon, value)],
        out_shape=(height, width),
        transform=transform,
        fill=0,
        dtype='uint8',
        all_touched=True
    )

    # Save GeoTIFF
    with rasterio.open(
        filename,
        'w',
        driver='GTiff',
        height=mask.shape[0],
        width=mask.shape[1],
        count=1,
        dtype=mask.dtype,
        crs="EPSG:32610",  # UTM Zone 10N
        transform=transform,
    ) as dst:
        dst.write(mask, 1)

    print(f"IRT footprint is saved as {filename}")
