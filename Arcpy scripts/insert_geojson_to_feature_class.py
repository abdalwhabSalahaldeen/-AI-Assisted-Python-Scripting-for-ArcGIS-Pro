import arcpy
import json

def insert_geojson_to_current_project(json_file_path, output_feature_class):
    # Get the current project and map
    project = arcpy.mp.ArcGISProject("CURRENT")
    active_map = project.activeMap

    if not active_map:
        raise ValueError("No active map found. Please open a map in your project.")

    # Load the JSON data from the file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create a feature class to store the data if it doesn't exist
    spatial_reference = arcpy.SpatialReference(4326)  # WGS 84
    gdb_path = arcpy.env.workspace or project.defaultGeodatabase
    output_fc_path = f"{gdb_path}\\{output_feature_class}"

    # Check if feature class exists and delete if necessary
    if arcpy.Exists(output_fc_path):
        arcpy.Delete_management(output_fc_path)

    arcpy.CreateFeatureclass_management(
        out_path=gdb_path,
        out_name=output_feature_class,
        geometry_type="POLYGON",
        spatial_reference=spatial_reference
    )

    # Add necessary fields
    arcpy.AddField_management(output_fc_path, "id", "LONG")
    arcpy.AddField_management(output_fc_path, "country_id", "LONG")
    arcpy.AddField_management(output_fc_path, "region_id", "LONG")
    arcpy.AddField_management(output_fc_path, "ar_name", "TEXT", field_length=255)
    arcpy.AddField_management(output_fc_path, "en_name", "TEXT", field_length=255)
    arcpy.AddField_management(output_fc_path, "trip_count", "LONG")
    
    # Insert data into the feature class
    with arcpy.da.InsertCursor(output_fc_path, ["SHAPE@", "id", "country_id", "region_id", "ar_name", "en_name", "trip_count"]) as cursor:
        for feature in data:
            geojson = json.loads(feature["area_geojson"])
            coordinates = geojson["coordinates"]

            # Convert the coordinates to an arcpy-compatible polygon
            multipolygon = arcpy.Array()
            for polygon in coordinates:
                outer_ring = arcpy.Array([arcpy.Point(*coords) for coords in polygon[0]])
                multipolygon.add(outer_ring)
            
            # Create an arcpy polygon geometry
            geometry = arcpy.Polygon(multipolygon, spatial_reference)
            
            # Insert the data
            cursor.insertRow([geometry, feature["id"], feature["country_id"], feature["region_id"], feature["ar_name"], feature["en_name"], feature["trip_count"]])

    # Add the feature class to the current map
    active_map.addDataFromPath(output_fc_path)
    print(f"Feature class '{output_feature_class}' has been added to the active map.")

# Parameters
json_file_path = r"C:\Users\abdo\Downloads\cites json.json"  # Replace with the path to your JSON file
output_feature_class = "OutputFeatureClass"  # Name of the output feature class
arcpy.env.workspace = None  # Automatically uses the project's default geodatabase

# Run the function
insert_geojson_to_current_project(json_file_path, output_feature_class)
