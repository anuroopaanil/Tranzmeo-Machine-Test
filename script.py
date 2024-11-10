import pandas as pd
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Load the CSV files
lat_lon_df = pd.read_csv("latitude_longitude_details (1).csv")
terrain_df = pd.read_csv("terrain_classification (1).csv")


# You can view the loaded data to understand its structure
print(lat_lon_df.head())
print(terrain_df.head())

# Function to calculate the distance between two points
def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).km

# Fix discontinuous coordinates by comparing distances between points
def fix_discontinuities(df):
    corrected_coords = [df.iloc[0]] 
    for i in range(1, len(df)):
        # Calculate distance between the current point and the previous point
        prev_point = (df.iloc[i-1]['latitude'], df.iloc[i-1]['longitude'])
        curr_point = (df.iloc[i]['latitude'], df.iloc[i]['longitude'])
        distance = calculate_distance(prev_point, curr_point)

        # If distance is too large, replace with interpolated point
        if distance > 0.1:  
            
            corrected_coords.append(df.iloc[i-1])
        else:
            corrected_coords.append(df.iloc[i])
    
    return pd.DataFrame(corrected_coords)

# Fix discontinuities in the latitude-longitude data
fixed_lat_lon_df = fix_discontinuities(lat_lon_df)

# Plotting the before and after data
plt.figure(figsize=(10,6))

# Before Fixing
plt.subplot(1, 2, 1)
plt.scatter(lat_lon_df['longitude'], lat_lon_df['latitude'], color='red', label='Before Fix')
plt.title('Before Fixing Discontinuities')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# After Fixing
plt.subplot(1, 2, 2)
plt.scatter(fixed_lat_lon_df['longitude'], fixed_lat_lon_df['latitude'], color='green', label='After Fix')
plt.title('After Fixing Discontinuities')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Show the plot
plt.tight_layout()
plt.show()

# Save the fixed data to a new CSV file
fixed_lat_lon_df.to_csv("fixed_latitude_longitude.csv", index=False)
lat_lon_df = pd.read_csv("latitude_longitude_details (1).csv")



import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="tranzmeo_test",  # Replace with your database name
    user="postgres",         # Replace with your username
    password="your_password", # Replace with your password
    host="localhost",        # Replace with your host (localhost or IP)
    port="5432"              # Default PostgreSQL port
)

# Create a cursor object to interact with the database
cur = conn.cursor()

# Write the query to fetch points with terrain "road" but without "civil station"
query = """
SELECT * 
FROM terrain_classification
WHERE terrain_type = 'road' 
AND classification != 'civil station';
"""

# Execute the query
cur.execute(query)

# Fetch all the results
results = cur.fetchall()

# Print the results
if results:
    print("Points with terrain 'road' and without 'civil station':")
    for row in results:
        print(row)
else:
    print("No results found.")

# Close the cursor and connection
cur.close()
conn.close()
