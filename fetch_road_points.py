import psycopg2

# Connect to the database
connection = psycopg2.connect(
    dbname="tranzmeo_test",
    user="postgres",
    password="Annuislove",
    host="localhost",
    port="5432"
)

# Create a cursor
cursor = connection.cursor()

# Define and execute the query
query = """
SELECT * FROM terrain_classification
WHERE terrain_type = 'road' AND classification != 'civil station';
"""
cursor.execute(query)

# Fetch the results and print them
results = cursor.fetchall()
for row in results:
    print(row)

# Close the cursor and connection
cursor.close()
connection.close()

import csv

# Assuming 'results' contains the data fetched from the database
with open("filtered_road_points.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id", "terrain_type", "classification"])  # Adjust headers as per table columns
    writer.writerows(results)

print("Filtered data saved to filtered_road_points.csv")

import matplotlib.pyplot as plt

# Extract latitude and longitude columns from results
latitudes = [row[1] for row in results]  # Adjust indices based on actual table structure
longitudes = [row[2] for row in results]

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(longitudes, latitudes, c='blue', marker='o', label="Road Terrain Points")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Terrain Points with 'Road' Classification (Excluding 'Civil Station')")
plt.legend()
plt.show()
