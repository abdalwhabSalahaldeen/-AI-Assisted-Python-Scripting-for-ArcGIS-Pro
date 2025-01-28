import arcpy
import requests
import time

# Define constants
API_URL = "https://api.openweathermap.org/data/2.5/weather"  # Example API (OpenWeatherMap)
API_KEY = "37e48f751d0527652386ce911c32e216"  # Replace with your actual API key

# Define the layer and field names
layer_name = "Weather_info"
temperature_field = "Temperature"
location_field = "Humidity"  # Assumes there's a field for city names in your layer

# Function to get the temperature from the weather API
def get_temperature(city_name):
    try:
        # Make an HTTP GET request to the weather API
        response = requests.get(API_URL, params={
            "q": city_name,
            "appid": API_KEY,
            "units": "metric"  # Use "metric" for Celsius or "imperial" for Fahrenheit
        })
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        # Extract the temperature
        return data["main"]["temp"]
    except Exception as e:
        print(f"Error fetching temperature for {city_name}: {e}")
        return None

# Function to update temperatures in the layer
def update_temperatures():
    # Access the layer
    layer = arcpy.mp.ArcGISProject("CURRENT").activeMap.listLayers(layer_name)[0]
    print(layer)

    # Start an edit session
    with arcpy.da.UpdateCursor(layer, [location_field, temperature_field]) as cursor:
        for row in cursor:
            print(row)
            city_name = row[0]
            if city_name:  # Ensure the city name is not null
                temperature = get_temperature(city_name)
                print(temperature)
                if temperature is not None:
                    row[1] = temperature
                    cursor.updateRow(row)
                    print(f"Updated {city_name} with temperature: {temperature}°C")
                else:
                    print(f"Skipping update for {city_name} due to error.")
    print("Temperature updates completed!")

# Run the script every hour
if __name__ == "__main__":
    while True:
        print("Starting temperature update...")
        update_temperatures()
        print("Waiting for 1 hour...")
        time.sleep(3600)  # Wait for 1 hour (3600 seconds)
