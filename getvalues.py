import sys, csv
import shapefile
import shapelogic

if len(sys.argv) < 5:
    print "Please call as: python getvalues.py <historical-shapefile> <values-csv> <values-column> <type>"
    print "  The historical shapefile and values csv must represent the same year."
    print "  <type> may be SUM or AVG"
    exit()

historical_filename = sys.argv[1] # "nhgis0005_shapefile_tl2000_us_county_1950/US_county_1950"
values_filename = sys.argv[2] # "nhgis0001_ts_1950_county.csv"
column = sys.argv[3] # "A00AA1950"
column_type = sys.argv[4].lower()

if column_type not in ['sum', 'avg']:
    print "Please specify a valid type."
    exit()

year2000 = shapefile.Reader("year2000/US_county_2000")
year2000_header = map(lambda f: f[0], year2000.fields)[1:]
year2000_records = year2000.records()

historic = shapefile.Reader(historical_filename)
historic_header = map(lambda f: f[0], historic.fields)[1:]
historic_records = historic.records()

index = {} # {FIPS: (year2000, historic)}
for ii in range(len(year2000_records)):
    record = year2000_records[ii]
    statefips = record[year2000_header.index('NHGISST')][0:-1]
    countyfips = record[year2000_header.index('NHGISCTY')][0:-1]
    fips = statefips + countyfips
    index[fips] = (ii, None)

for ii in range(len(historic_records)):
    record = historic_records[ii]
    statefips = record[historic_header.index('NHGISST')][0:-1]
    countyfips = record[historic_header.index('NHGISCTY')][0:-1]
    fips = statefips + countyfips
    if fips in index:
        index[fips] = (index[fips][0], ii)
    else:
        index[fips] = (None, ii)

# Look for exact matches
values = {} # {GISJOIN: value}
with open(values_filename, 'r') as fp:
    reader = csv.reader(fp)
    header = reader.next()
    print ','.join(header)
    for row in reader:
        fips = row[header.index('STATEA')][0:-1] + row[header.index('COUNTYA')][0:-1]
        if fips in index:
            year2000_ii, historic_ii = index[fips]
            if year2000_ii is not None and historic_ii is not None:
                if year2000.shape(year2000_ii).points == historic.shape(historic_ii).points:
                    state = row[header.index('STATE')]
                    county = row[header.index('COUNTY')]
                    value = row[header.index(column)]
                    print ','.join([fips, state, county, value])
                    del index[fips]
                    continue

        # We couldn't find an exact match
        values[row[header.index('GISJOIN')]] = float(row[header.index(column)])

# Iterate through remaining
for fips in index:
    year2000_ii, historic_ii = index[fips]
    if year2000_ii is None:
        continue
    year2000_shape = year2000.shape(year2000_ii)
    year2000_polygon = shapelogic.shape2multi(year2000_shape).buffer(0)
    # Find all counties that could contribute to year2000 county
    total = 0.0
    denom = 0.0
    historic_ii = 0
    for shape in historic.iterShapes():
        gisjoin = historic_records[historic_ii][historic_header.index('GISJOIN')]
        if gisjoin in values and shapelogic.box_intersects(year2000_shape.bbox, shape.bbox):
            historic_polygon = shapelogic.shape2multi(shape).buffer(0)
            intersection = year2000_polygon.intersection(historic_polygon)
            total += values[gisjoin] * intersection.area / historic_polygon.area
            denom += intersection.area / historic_polygon.area
        historic_ii += 1

    state = year2000_records[year2000_ii][year2000_header.index('STATENAM')]
    county = year2000_records[year2000_ii][year2000_header.index('ICPSRNAM')]
    if column_type == 'sum':
        print ','.join([fips, state, county, str(total)])
    elif column_type == 'avg':
        print ','.join([fips, state, county, str(total / denom)])
