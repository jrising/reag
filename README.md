# reag
Reaggregation tool for translating historical data to current boundaries.

Reag will use data for counties whose boundaries have not changed
directly.  For all other counties, it will determine the geometric
intersection between year 2000 county boundaries and historical
boundaries, and compute estimated values from each historical county
contribution.

## Installation

Reag uses Python 2.6+, pyshp, and shapely.

Follow the instructions on https://github.com/GeospatialPython/pyshp and http://toblerity.org/shapely/project.html#installation to install these dependencies.

## Use

```
python getvalues.py <historical-shapefile> <values-csv> <values-column> <type>
```

The historical shapefile and values csv must represent the same year.
type may be SUM or AVG.

For example,
```
python getvalues.py nhgis0005_shapefile_tl2000_us_county_1950/US_county_1950 nhgis0001_ts_1950_county.csv A00AA1950 sum
```
