import shapefile
from shapely.geometry import Polygon, MultiPolygon, geo

def shape2parts(shape):
    parts = []
    start_indexes = shape.parts
    prev_start_index = 0
    for start_index in start_indexes[1:]:
        parts.append(shape.points[prev_start_index:start_index])
        prev_start_index = start_index
    parts.append(shape.points[prev_start_index:])

    return parts

def shape2multi(shape):
    parts = shape2parts(shape)
    polygons = []
    for part in parts:
        polygons.append(Polygon(part))

    return MultiPolygon(polygons)

def intersection(one, two):
    onepoly = shape2multi(one)
    twopoly = shape2multi(two)

    return onepoly.intersection(twopoly)

def box_intersects(one, two):
    return geo.box(*one).intersects(geo.box(*two))
    
