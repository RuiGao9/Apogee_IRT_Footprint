def tiff_to_shapefile(tiff_path, shapefile_path=None, target_value=1):
    """
    Converts a GeoTIFF raster to a shapefile by extracting pixels equal to target_value.
    Easy for some feature extraction work via ArcGIS Pro (or QGIS).
    
    Parameters:
        tiff_path (str): Input TIFF file path.
        shapefile_path (str, optional): Output .shp path. Defaults to same name as TIFF.
        target_value (int): The pixel value to keep (default = 1).
    
    Returns:
        shapefile_path (str): Output shapefile path.
    """
    import rasterio
    from rasterio import features
    from shapely.geometry import shape, mapping
    import fiona
    import os

    if shapefile_path is None:
        shapefile_path = os.path.splitext(tiff_path)[0] + ".shp"

    with rasterio.open(tiff_path) as src:
        image = src.read(1)
        mask = image == target_value
        transform = src.transform
        crs = src.crs

        # Generate polygons
        shape_generator = features.shapes(image, mask=mask, transform=transform)
        polygons = list(shape_generator)

    # Define shapefile schema
    schema = {
        'geometry': 'Polygon',
        'properties': {'value': 'int'}
    }
    with fiona.open(shapefile_path, 'w', driver='ESRI Shapefile',
                    crs=crs.to_dict(), schema=schema) as shp:
        for geom, val in polygons:
            shp.write({
                'geometry': mapping(shape(geom)),
                'properties': {'value': int(val)}
            })
    print(f"Shapefile saved to: {shapefile_path}")
    
    return shapefile_path
