def georeference_ellipse(ellipse_points, sensor_lat, sensor_lon, epsg_utm="EPSG:32610"):
    """
    Convert local ellipse points to geospatial coordinates in UTM and optionally WGS84.
    For other locations, you may want to do some modifications here.

    Parameters:
    - ellipse_points: numpy array of shape (N, 2), (x, y) in meters relative to sensor
    - sensor_lat, sensor_lon: Latitude and longitude of IRT sensor
    - epsg_utm: UTM projection string (default is EPSG:32610 for California)

    Returns:
    - xy_utm: Projected UTM coordinates
    - lonlat: (optional) Latitude/Longitude coordinates
    """
    
    from pyproj import Transformer
    import numpy as np

    # Transformer for WGS84 → UTM
    transformer_fwd = Transformer.from_crs("EPSG:4326", epsg_utm, always_xy=True)
    # Transformer for UTM → WGS84
    transformer_inv = Transformer.from_crs(epsg_utm, "EPSG:4326", always_xy=True)
    # Convert sensor lat/lon to UTM
    sensor_x, sensor_y = transformer_fwd.transform(sensor_lon, sensor_lat)
    # Add local ellipse offsets
    abs_x = sensor_x + ellipse_points[:, 0]
    abs_y = sensor_y + ellipse_points[:, 1]
    # Convert back to lat/lon
    lon, lat = transformer_inv.transform(abs_x, abs_y)
    xy_utm = np.stack((abs_x, abs_y), axis=1)
    lonlat = np.stack((lon, lat), axis=1)

    return xy_utm, lonlat