
import sys
print("The arguments are: " , str(sys.argv))

# polygon_location = "data/polygon_input/groenvlakken2.shp" ##### hier batch input van maken #####
# identifier_column_name = 'KRCode'

polygon_location = sys.argv[1]
identifier_column_name = sys.argv[2]



# Load packages
import os
import pandas as pd
import geopandas as gpd

# Load functions
from functions import coord_lister

# Create directories
if not os.path.exists('data'): os.makedirs('data')
if not os.path.exists('data/polygon_input'): os.makedirs('data/polygon_input')
if not os.path.exists('data/javascript_input'): os.makedirs('data/javascript_input')
if not os.path.exists('data/javascript_output'): os.makedirs('data/javascript_output')
if not os.path.exists('output'): os.makedirs('output')

# Load polygons
polygons = gpd.read_file(polygon_location)
print(len(polygons.index), " polygons found")

for idx,row in polygons.iterrows():
    identifier = row[identifier_column_name] 
    polygon = row['geometry']

    if identifier:
        with open("data/javascript_input/" + identifier + ".txt","w") as file:
            n_coordinates = len(coord_lister(polygon))
            for idx, point in enumerate(coord_lister(polygon)):

                x = str(point[0])
                y = str(point[1])
                file.write(x + "," + y)
                if not idx == n_coordinates -1:
                    file.write("\n")