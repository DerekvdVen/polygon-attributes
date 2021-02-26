The purpose of this collection of scripts is to collect length and width information on a ESRI shapefile collection of polygons. To run the workflow.bat, you will need to install a conda environment manager (miniconda for example) and node.js + nms(automatically included in node.js install). You may start the workflow by running FME_batch.fmw. FOr this you will need to install FME. 

The workflow can also be called from the shell:

.\workflow.bat $(anaconda_loc) $(polygon_file_location) $(identifier_column_name) 
                OPTIONAL: $(lcheck_factor) $(squareness_factor) $(lf_factor) $(cl_distance)
                
                # anaconda3_location=C:\Users\Derek\Anaconda3 , location to check for conda environment
                # polygon_file_location=data/polygon_input/shapefile.sh, shapefile location
                # identifier_column_name=KRcode, object id column name

                OPTIONAL parameters
                # lcheck_factor = 0.3, Een hogere lcheck betekent dat er meer gecheckt moet worden. 
                # squareness_factor = 0.7, Een hogere squareness betekent dat minder langwerpige polygonen eerder als vierkant worden bestempelt. Hierdoor wordt dan de lengte van de polygoon met de oppervlaktemethode berekent.
                #  lf = 2.5, Verhouding waarop polygonen als langwerpig worden beschouwd. Een hogere lf leidt tot minder als langwerpig beschouwde polygonen.
                # distance = 1, Simplificatiefactor voor centerlijn. Hogere waardes leidt tot verwdijnen van dunne polygonen.

This directory contains 6 scripts:

-- workflow.bat
    batch file to call all other scripts in the order as shown below
    also installs all modules in conda environment
    also installs java modules

-- FME_batch.fmw
    simply calls the workflow.bat with a popup for user parameters.
    
-- create_input_for_javascript.py
    input:
        - shapefile (WFS, polygons)
    output:
        - .txt file per polygon in ./data/java_input/*.txt
            Contains coordinate pairs split by single comma with one pair per line
    
-- get_width.js
    input:
        - ./data/java_input/*.txt
    output:
        - ./data/java_output/*.txt
            Contains .txt file per polygon with width value
                   
-- calc_length.py
    input:
        -./data/java_output/*.txt
    output:
        -./output/length_width_table.xlsx
        
 -- functions.py
    Contains functions for other scripts

     
