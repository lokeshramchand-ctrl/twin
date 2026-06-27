import fiona
import json
from pyproj import Transformer
from shapely.geometry import shape, mapping
from shapely.ops import transform

shapefile_path = "Address_Points.shp"
output_ndjson_path = "converted_data.json"

print("Starting streaming conversion...")

with fiona.Env(SHAPE_RESTORE_SHX="YES"):
    with fiona.open(shapefile_path, "r") as src:
        
        # Set up the coordinate transformer
        transformer = Transformer.from_crs(src.crs, "EPSG:4326", always_xy=True)
        
        with open(output_ndjson_path, "w", encoding="utf-8") as dst:
            
            for feature in src:
                # In newer fiona, properties are accessed via attributes or .get()
                if feature.geometry is not None:
                    
                    # 1. Grab the geometry and reproject it
                    geom = shape(feature.geometry)
                    reprojected_geom = transform(transformer.transform, geom)
                    
                    # 2. Build a brand new, clean Python dictionary
                    # We cast properties to dict() so json.dumps doesn't complain
                    new_feature = {
                        "type": "Feature",
                        "geometry": mapping(reprojected_geom),
                        "properties": dict(feature.properties)
                    }
                    
                    # 3. Serialize and write our pure Python dictionary
                    dst.write(json.dumps(new_feature) + "\n")

print("Conversion complete! File is ready for MongoDB.")