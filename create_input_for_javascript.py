
import sys
print("The arguments are: " , str(sys.argv))

# polygon_location = "data/geodatabase/OMS_NHM_20201223.gdb" ##### hier batch input van maken #####
# identifier_column_name = 'KRCode'
# gdb_layer = 'vWaterafvoer'

polygon_location = sys.argv[1]
identifier_column_name = sys.argv[2]
gdb_layer = sys.argv[3]

# Load packages
import os
import pandas as pd
import geopandas as gpd

from osgeo import ogr
import fiona


# # Load functions
from functions import coord_lister

# Create directories
if not os.path.exists('data'): os.makedirs('data')
if not os.path.exists('data/polygon_input'): os.makedirs('data/polygon_input')
if not os.path.exists('data/javascript_input'): os.makedirs('data/javascript_input')
if not os.path.exists('data/javascript_output'): os.makedirs('data/javascript_output')
if not os.path.exists('output'): os.makedirs('output')

# Load polygons
# polygons = gpd.read_file(polygon_location)
# print(type(polygons))
layerlist = fiona.listlayers(polygon_location)
print(layerlist)
polygons = gpd.read_file(polygon_location,layer=gdb_layer)
# print(type(df1))

print(len(polygons.index), " polygons found")
mp=0
p=0
multipolygons = []

# LIMIT = 0
for idx,row in polygons.iterrows():
    # if LIMIT == 100:
    #     break
    # LIMIT+=1
    identifier = row[identifier_column_name] 
    polygon = row['geometry']

    if polygon.geom_type == 'MultiPolygon':
        sep_polygons = list(polygon)    
        if len(sep_polygons) == 1:
            polygon = list(polygon)[0]
        
        
        if len(sep_polygons) > 1:
            multipolygons.append(identifier)
            continue

    # single polygon
    if identifier:
        with open("data/javascript_input/" + identifier + ".txt","w") as file:
            n_coordinates = len(coord_lister(polygon))
            for idx, point in enumerate(coord_lister(polygon)):

                x = str(point[0])
                y = str(point[1])
                file.write(x + "," + y)
                if not idx == n_coordinates -1:
                    file.write("\n")



print("p: ",p)
print("mp: ", mp)