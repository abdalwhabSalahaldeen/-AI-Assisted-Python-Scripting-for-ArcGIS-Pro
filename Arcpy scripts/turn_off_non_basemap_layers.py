import arcpy

def turn_off_non_basemap_layers():
    # Get the current project
    project = arcpy.mp.ArcGISProject("CURRENT")
    
    # Loop through all maps in the project
    for map_obj in project.listMaps():
        print(f"Processing map: {map_obj.name}")
        
        # Loop through all layers in the map
        for layer in map_obj.listLayers():
            # Check if the layer is not a basemap layer
            if not layer.isBasemapLayer:
                # Turn off the layer visibility
                layer.visible = False
                print(f"Turned off layer: {layer.name}")
            else:
                print(f"Skipped basemap layer: {layer.name}")

if __name__ == "__main__":
    turn_off_non_basemap_layers()