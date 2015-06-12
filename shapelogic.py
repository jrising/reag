################################################################################
# shapelogic - Helper functions for using shapefiles with shapely
################################################################################

import shapefile
from shapely.geometry import Polygon, MultiPolygon, geo

def shape2parts(shape):
    """Divide a shape's points based on the indexes in <parts>."""
    parts = []
    start_indexes = shape.parts
    prev_start_index = 0
    for start_index in start_indexes[1:]:
        parts.append(shape.points[prev_start_index:start_index])
        prev_start_index = start_index
    parts.append(shape.points[prev_start_index:])

    return parts

def shape2multi(shape):
    """Construct a Polygon for each of a shape's parts, and a MultiPolygon to wrap it all."""
    parts = shape2parts(shape)
    polygons = []
    for part in parts:
        polygons.append(Polygon(part))

    return MultiPolygon(polygons)

def intersection(one, two):
    """Construct an intersection polygon for two shapefile shapes."""
    onepoly = shape2multi(one)
    twopoly = shape2multi(two)

    return onepoly.intersection(twopoly)

def box_intersects(one, two):
    """Return true if two boxes (as vectors of xmin, ymin, xmax, ymax) intersect."""
    return geo.box(*one).intersects(geo.box(*two))
    
