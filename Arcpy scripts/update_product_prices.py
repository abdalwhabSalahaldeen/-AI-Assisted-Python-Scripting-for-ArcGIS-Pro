import arcpy

# Get the current ArcGIS Pro project
project = arcpy.mp.ArcGISProject("CURRENT")

# Get the map and layers from the current project
map_view = project.listMaps()[0]  # Assuming you're working with the first map

# Define the feature class and table
products_fc = "products"  # Replace with your actual feature class name
updated_prices_table = "updated_prices"  # Replace with your actual table name

# Create an update cursor for the updated_prices table
with arcpy.da.SearchCursor(updated_prices_table, ['Product_ID', 'Price']) as cursor:
    for row in cursor:
        product_id = row[0]
        new_price = row[1]
        
        # Skip invalid prices (null, whitespace, zero, or negative)
        if new_price is None or str(new_price).strip() == "" or new_price <= 0:
            continue  # Skip this row if the price is invalid
        
        # Create an update cursor for the products feature class
        with arcpy.da.UpdateCursor(products_fc, ['Product_ID', 'Price']) as update_cursor:
            for update_row in update_cursor:
                # Check if the product_id matches
                if update_row[0] == product_id:
                    # Update the price field with the new valid price
                    update_row[1] = new_price
                    update_cursor.updateRow(update_row)  # Commit the changes
                    print(f"Updated product_id {product_id} with price {new_price}")
                    
print("Price update process completed.")
