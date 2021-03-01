# import packages

import os
import sys
import pandas as pd
import fiona
import geopandas as gpd
import matplotlib.pyplot as plt 
from descartes import PolygonPatch
from shapely.geometry import Polygon, Point
from centerline.geometry import Centerline

# import functions
from functions import calc_squareness, calc_l_w_minimum_rectangle

polygon_location = sys.argv[1]
identifier_column_name = sys.argv[2]
layer = sys.argv[3]

lcheck_factor = float(sys.argv[4]) # Een hogere lcheck betekent dat er meer gecheckt moet worden. 
squareness_factor = float(sys.argv[5]) # Een hogere squareness betekent dat minder langwerpige polygonen eerder als vierkant worden bestempelt. Hierdoor wordt dan de lengte van de polygoon met de oppervlaktemethode berekent.
lf_factor = float(sys.argv[6]) # Verhouding waarop polygonen als langwerpig worden beschouwd. Een hogere lf leidt tot minder als langwerpig beschouwde polygonen.
cl_distance = float(sys.argv[7]) # Simplificatiefactor voor centerlijn. Hogere waardes leidt tot verwdijnen van dunne polygonen. 


# CONSTANTE VARIABELEN
INPUT_LOCATION = 'data/javascript_output/'
OUTPUT_LOCATION = 'output/'

# Dictionaries containing widths and areas of polygons
width_dict = {}
area_dict={}

# Read widths from javascript_output
for file in os.listdir(INPUT_LOCATION):
    
    with open(INPUT_LOCATION + file,"r") as f:
        width = f.readline()
    
    # Use output_name[without .txt] to read found width
    width_dict[file[:-4]] = width

# Load in polygons again and add empty width and length column
# polygons = gpd.read_file(polygon_location)
polygons = gpd.read_file(polygon_location,layer=layer)
# print(type(df1))
polygons['js_width'] = 0
polygons['length'] = 0
polygons['check'] = False
polygons['l_methode'] = ''

# Loop over polygons
multipolygons = []
stats = {}
stats['multipolygons'] = 0
stats['geen_breedte_gevonden'] = 0


LIMIT = 0
for idx,row in polygons.iterrows():
    if LIMIT == 100:
        break
    LIMIT+=1
    identifier = row[identifier_column_name]
    polygon = row['geometry']
    
    if polygon.geom_type == 'MultiPolygon':
        sep_polygons = list(polygon) 
        if len(sep_polygons) == 1:
            polygon = list(polygon)[0]

            polygon_area = polygon.area
            area_dict[identifier] = polygon_area

            # Als er een breedte terug is gegeven, lengte hiermee uitrekenen
            if width_dict[identifier] != '0':
                js_width = float(width_dict[identifier])
                polygons.loc[idx,'js_width'] = js_width
                js_length = area_dict[identifier]/ float(width_dict[identifier])
            
            # Als de vierkant methode niet werkt en er voor de identifier geen breedte is gevonden, gebruik gewoon de centerline methode, en check de output
            else:
                stats['geen_breedte_gevonden'] +=1
                polygons.loc[idx,'check'] = True    

                try:
                    centerline = Centerline(polygon,interpolation_distance=cl_distance)
                    polygons.loc[idx,'length'] = centerline.length
                    polygons.loc[idx,'l_methode'] = 'centerline'
                    continue
                except:
                    polygons.loc[idx,'length'] = 0
                    polygons.loc[idx,'l_methode'] = 'none: bad centerline and no width found'
                    continue
        
            # check how much of the polygon fills its bounds
            squareness = calc_squareness(polygon, polygon_area)
            
            # check length and width of minimum surrounding rectangle
            l,w = calc_l_w_minimum_rectangle(polygon)
            
            # check centerline, als deze niet werkt, geen lengte invullen en checken
            try:
                centerline = Centerline(polygon,interpolation_distance=cl_distance)
            except:
                polygons.loc[idx,'check'] = True
                #centerline = Centerline(polygon,interpolation_distance=cl_distance)
                polygons.loc[idx,'length'] = 0
                polygons.loc[idx,'l_methode'] = 'none: bad centerline'
                continue
            
            # Check of polygon langwerpig is
            if l/w > lf_factor or w/l > lf_factor:
                polygons.loc[idx,'length'] = centerline.length
                polygons.loc[idx,'l_methode'] = 'centerline'

            # Niet langwerpig? Check of polygon heel erg vierkant is, zo nee, dan is het waarschijnlijk een sliert
            elif squareness < squareness_factor:
                polygons.loc[idx,'length'] = centerline.length
                polygons.loc[idx,'l_methode'] = 'centerline'

            # Niet een sliert? Het polygon is erg vierkant en er kan geen goede centerline gevonden worden. Oppervlakte wordt berekent via de gevonden breedte. 
            else:
                polygons.loc[idx,'length'] = js_length
                polygons.loc[idx,'l_methode'] = 'oppervlakte'

            # Als oppervlakte methode en centerline methode heel andere lengtes meegeven heeft de polygon waarschijnlijk een gekke vorm. # Deze moeten gecheckt worden.
            verhouding = js_length/centerline.length
            if verhouding < lcheck_factor:
                polygons.loc[idx,'check'] = True
                    
        if len(sep_polygons) > 1:
            polygons.loc[idx,'check'] = True  
            polygons.loc[idx,'length'] = 0
            polygons.loc[idx,'l_methode'] = 'none: multiple polygons'
            polygons.loc[idx,'js_width'] = 0
    else:
        polygon_area = polygon.area
        area_dict[identifier] = polygon_area

        # Als er een breedte terug is gegeven, lengte hiermee uitrekenen
        if width_dict[identifier] != '0':
            js_width = float(width_dict[identifier])
            polygons.loc[idx,'js_width'] = js_width
            js_length = area_dict[identifier]/ float(width_dict[identifier])
        
        # Als de vierkant methode niet werkt en er voor de identifier geen breedte is gevonden, gebruik gewoon de centerline methode, en check de output
        else:
            stats['geen_breedte_gevonden'] +=1
            polygons.loc[idx,'check'] = True    

            try:
                centerline = Centerline(polygon,interpolation_distance=cl_distance)
                polygons.loc[idx,'length'] = centerline.length
                polygons.loc[idx,'l_methode'] = 'centerline'
                continue
            except:
                polygons.loc[idx,'length'] = 0
                polygons.loc[idx,'l_methode'] = 'none'
                continue
    
        # check how much of the polygon fills its bounds
        squareness = calc_squareness(polygon, polygon_area)
        
        # check length and width of minimum surrounding rectangle
        l,w = calc_l_w_minimum_rectangle(polygon)
        
        # check centerline, als deze niet werkt, geen lengte invullen en checken
        try:
            centerline = Centerline(polygon,interpolation_distance=cl_distance)
        except:
            polygons.loc[idx,'check'] = True
            #centerline = Centerline(polygon,interpolation_distance=cl_distance)
            polygons.loc[idx,'length'] = 0
            polygons.loc[idx,'l_methode'] = 'none'
            continue
        
        # Check of polygon langwerpig is
        if l/w > lf_factor or w/l > lf_factor:
            polygons.loc[idx,'length'] = centerline.length
            polygons.loc[idx,'l_methode'] = 'centerline'

        # Niet langwerpig? Check of polygon heel erg vierkant is, zo nee, dan is het waarschijnlijk een sliert
        elif squareness < squareness_factor:
            polygons.loc[idx,'length'] = centerline.length
            polygons.loc[idx,'l_methode'] = 'centerline'

        # Niet een sliert? Het polygon is erg vierkant en er kan geen goede centerline gevonden worden. Oppervlakte wordt berekent via de gevonden breedte. 
        else:
            polygons.loc[idx,'length'] = js_length
            polygons.loc[idx,'l_methode'] = 'oppervlakte'

        # Als oppervlakte methode en centerline methode heel andere lengtes meegeven heeft de polygon waarschijnlijk een gekke vorm. # Deze moeten gecheckt worden.
        verhouding = js_length/centerline.length
        if verhouding < lcheck_factor:
            polygons.loc[idx,'check'] = True


polygons.to_excel("output/output.xlsx")
print("output stored")
print(stats)