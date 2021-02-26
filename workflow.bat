@echo off

rem Workflow.bat - Derek van de Ven - 26-2-2021

rem This workflow.bat runs a set of scripts to collect width and height of polygons in a shapefile. 
rem Inputs are the anaconda3 directory location, the polygon shapefile location, and the identifier column name in the shapefile:

rem FME parameters
rem # anaconda3_location=C:\Users\Derek\Anaconda3 , location to check for conda environment
rem # polygon_file_location=data/polygon_input/shapefile.sh, shapefile location
rem # identifier_column_name=KRcode, object id column name

rem OPTIONAL parameters
rem # lcheck_factor = 0.3, Een hogere lcheck betekent dat er meer gecheckt moet worden. 
rem # squareness_factor = 0.7, Een hogere squareness betekent dat minder langwerpige polygonen eerder als vierkant worden bestempelt. Hierdoor wordt dan de lengte van de polygoon met de oppervlaktemethode berekent.
rem #  lf = 2.5, Verhouding waarop polygonen als langwerpig worden beschouwd. Een hogere lf leidt tot minder als langwerpig beschouwde polygonen.
rem # distance = 1, Simplificatiefactor voor centerlijn. Hogere waardes leidt tot verwdijnen van dunne polygonen.

set anaconda3_location=%1
set polygon_file_location=%2
set identifier_column_name=%3

set lcheck_factor=%4
set squareness_factor=%5
set lf_factor=%6
set cl_distance=%7   

rem fixed parameter
set CONDA_ENV=\envs\conda_polygons

rem install node.js modules
call npm install d3plus
call npm install fs

rem create conda env
set conda_polygons_location=%anaconda3_location%%CONDA_ENV%

if exist %conda_polygons_location% (
    echo "Conda environment already exists"
    
    rem update packages
    call conda activate conda_polygons
    call conda update --all
    call conda deactivate

) else (
    echo "Conda environment does not yet exist"
    call conda create --name conda_polygons pandas geopandas matplotlib descartes shapely openpyxl -y
)



rem install centerline using pip
call conda install -n conda_polygons pip -y
call conda activate conda_polygons
pip install centerline



rem CODE
python create_input_for_javascript.py %polygon_file_location% %identifier_column_name%
node get_width.js
python calc_length_store_table.py %polygon_file_location% %identifier_column_name% %lcheck_factor% %squareness_factor% %lf_factor% %cl_distance%
call conda deactivate
