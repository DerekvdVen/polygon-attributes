from shapely.geometry import Polygon, Point

def coord_lister(geom):
    
    coords = list(geom.exterior.coords)
    return (coords)

def bb_area(bounds):
    area = abs(bounds[0]-bounds[2]) * abs(bounds[1]-bounds[3])
    return(area)

def calc_squareness(polygon, area):
        minimum_square_area = polygon.minimum_rotated_rectangle.area
        squareness = area/minimum_square_area
        return(squareness)
    
def calc_l_w_minimum_rectangle(polygon):
    minimum_rectangle = polygon.minimum_rotated_rectangle
    x, y = minimum_rectangle.exterior.coords.xy
    edge_length = (Point(x[0], y[0]).distance(Point(x[1], y[1])), Point(x[1], y[1]).distance(Point(x[2], y[2])))
    l = max(edge_length)# get length of polygon as the longest edge of the bounding box
    w = min(edge_length)# get width of polygon as the shortest edge of the bounding box
    return(l,w)

