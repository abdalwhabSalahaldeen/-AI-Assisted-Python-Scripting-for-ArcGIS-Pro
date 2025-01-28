import arcpy

# Get the current ArcGIS Pro project
project = arcpy.mp.ArcGISProject("CURRENT")

# Get the map and layers from the current project
map_view = project.listMaps()[0]  # Assuming you're working with the first map

# Access the polygon layer named "OutputFeatureClass"
polygon_layer = map_view.listLayers("OutputFeatureClass")[0]  # Assuming your polygon layer is named "OutputFeatureClass"

# Create a feature layer from the polygon layer
arcpy.MakeFeatureLayer_management(polygon_layer, "polygon_layer")

# Select the polygon with ID = 75
arcpy.SelectLayerByAttribute_management("polygon_layer", "NEW_SELECTION", "ID = 75")

# Loop through all layers in the map
for layer in map_view.listLayers():
    if layer.isFeatureLayer:  # Only process feature layers
        # Create a feature layer from the current layer
        arcpy.MakeFeatureLayer_management(layer, "input_layer")
        
        # Apply spatial selection to get features inside the polygon with ID 75
        arcpy.SelectLayerByLocation_management("input_layer", "WITHIN", "polygon_layer")

        # Get the default geodatabase for the current project
        default_gdb = project.defaultGeodatabase

        # Define the output feature class path within the current project's default geodatabase
        output_fc = default_gdb + r"\filtered_" + layer.name

        # Save the selected features to the output feature class
        arcpy.CopyFeatures_management("input_layer", output_fc)

        print(f"Filtered data from {layer.name} has been saved to {output_fc}")
 