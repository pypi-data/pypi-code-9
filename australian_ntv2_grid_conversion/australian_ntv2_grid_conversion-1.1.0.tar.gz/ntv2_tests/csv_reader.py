import csv

gdait_agd66_input_file = 'GDAit_and_GDAy_conversions/random_AGD66_gdait_input.csv'
gdait_agd84_input_file = 'GDAit_and_GDAy_conversions/random_AGD84_gdait_input.csv'
gdait_agd66_output_file = 'GDAit_and_GDAy_conversions/random_AGD66_gdait_output.csv'
gdait_agd84_output_file = 'GDAit_and_GDAy_conversions/random_AGD84_gdait_output.csv'

gdait_input_data_header_rows = 2
gdait_output_data_header_rows = 12

gdait_agd66_input_data = {}
gdait_agd84_input_data = {}
gdait_agd66_output_data = {}
gdait_agd84_output_data = {}

gday_agd66_input_file = 'GDAit_and_GDAy_conversions/random_AGD66_gday_input.csv'
gday_agd84_input_file = 'GDAit_and_GDAy_conversions/random_AGD84_gday_input.csv'
gday_agd66_output_file = 'GDAit_and_GDAy_conversions/random_AGD66_gday_output.csv'
gday_agd84_output_file = 'GDAit_and_GDAy_conversions/random_AGD84_gday_output.csv'

gday_input_data_header_rows = 0
gday_output_data_header_rows = 0

gday_agd66_input_data = {}
gday_agd84_input_data = {}
gday_agd66_output_data = {}
gday_agd84_output_data = {}

known_values_file = 'known_values.py'

# read gdait files
row_number = 0
with open(gdait_agd66_input_file, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        row_number += 1
        if row_number <= gdait_input_data_header_rows:
            continue
        gdait_agd66_input_data[int(row[0].replace('p', ''))] = {'lat': float(row[1]), 'lon': float(row[2])}

row_number = 0
with open(gdait_agd84_input_file, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        row_number += 1
        if row_number <= gdait_input_data_header_rows:
            continue
        gdait_agd84_input_data[int(row[0].replace('p', ''))] = {'lat': float(row[1]), 'lon': float(row[2])}

row_number = 0
with open(gdait_agd66_output_file, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        row_number += 1
        if row_number <= gdait_output_data_header_rows:
            continue
        try:
            gdait_agd66_output_data[int(row[0].replace('p', ''))] = {'lat': float(row[1]), 'lon': float(row[2]), 'lat_acc': float(row[7]), 'lon_acc': float(row[8])}
        except ValueError:
            gdait_agd66_output_data[int(row[0].replace('p', ''))] = {'lat': float(row[1]), 'lon': float(row[2]), 'lat_acc': row[7].strip(), 'lon_acc': row[8].strip()}

row_number = 0
with open(gdait_agd84_output_file, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        row_number += 1
        if row_number <= gdait_output_data_header_rows:
            continue
        try:
            gdait_agd84_output_data[int(row[0].replace('p', ''))] = {'lat': float(row[1]), 'lon': float(row[2]), 'lat_acc': float(row[7]), 'lon_acc': float(row[8])}
        except ValueError:
            gdait_agd84_output_data[int(row[0].replace('p', ''))] = {'lat': float(row[1]), 'lon': float(row[2]), 'lat_acc': row[7].strip(), 'lon_acc': row[8].strip()}

# read gday files
row_number = 0
with open(gday_agd66_input_file, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        row_number += 1
        if row_number <= gday_input_data_header_rows:
            continue
        gday_agd66_input_data[int(row[0].replace('p', ''))] = {'lat': float(row[1]), 'lon': float(row[2])}

row_number = 0
with open(gday_agd84_input_file, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        row_number += 1
        if row_number <= gday_input_data_header_rows:
            continue
        gday_agd84_input_data[int(row[0].replace('p', ''))] = {'lat': float(row[1]), 'lon': float(row[2])}

row_number = 0
with open(gday_agd66_output_file, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        row_number += 1
        if row_number <= gday_output_data_header_rows:
            continue
        try:
            gday_agd66_output_data[int(row[0].replace('p', ''))] = {'lat': float(row[1]), 'lon': float(row[2]), 'lat_acc': float(row[7]), 'lon_acc': float(row[8])}
        except ValueError:
            gday_agd66_output_data[int(row[0].replace('p', ''))] = {'lat': float(row[1]), 'lon': float(row[2]), 'lat_acc': row[7].strip(), 'lon_acc': row[8].strip()}

row_number = 0
with open(gday_agd84_output_file, newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        row_number += 1
        if row_number <= gday_output_data_header_rows:
            continue
        try:
            gday_agd84_output_data[int(row[0].replace('p', ''))] = {'lat': float(row[1]), 'lon': float(row[2]), 'lat_acc': float(row[7]), 'lon_acc': float(row[8])}
        except ValueError:
            gday_agd84_output_data[int(row[0].replace('p', ''))] = {'lat': float(row[1]), 'lon': float(row[2]), 'lat_acc': row[7].strip(), 'lon_acc': row[8].strip()}


# write values to python value for easier importing later
with open(known_values_file, 'w') as output_file:
    output_file.write('class KnownValues:\n')
    data_count = 0
    output_file.write('    gdait_agd66_to_gda94 = [\n')
    for i in gdait_agd66_input_data:
        data_count += 1
        if type(gdait_agd66_output_data[i]['lat_acc']) is float and type(gdait_agd66_output_data[i]['lon_acc']) is float:
            output_file.write("                      {{'agd66': [{}, {}], 'gda94': [{}, {}], 'acc': [{}, {}]}}".format(gdait_agd66_input_data[i]['lat'], gdait_agd66_input_data[i]['lon'],
                                                                                                                      gdait_agd66_output_data[i]['lat'], gdait_agd66_output_data[i]['lon'],
                                                                                                                      gdait_agd66_output_data[i]['lat_acc'], gdait_agd66_output_data[i]['lon_acc']))
        else:
            output_file.write("                      {{'agd66': [{}, {}], 'gda94': [{}, {}], 'acc': ['{}', '{}']}}".format(gdait_agd66_input_data[i]['lat'], gdait_agd66_input_data[i]['lon'],
                                                                                                                          gdait_agd66_output_data[i]['lat'], gdait_agd66_output_data[i]['lon'],
                                                                                                                          gdait_agd66_output_data[i]['lat_acc'], gdait_agd66_output_data[i]['lon_acc']))
        if data_count < len(gdait_agd66_input_data):
            output_file.write(",\n")
        else:
            output_file.write("\n")
    output_file.write('    ]\n')
    output_file.write('\n')
    data_count = 0
    output_file.write('    gdait_agd84_to_gda94 = [\n')
    for i in gdait_agd84_input_data:
        data_count += 1
        if type(gdait_agd84_output_data[i]['lat_acc']) is float and type(gdait_agd84_output_data[i]['lon_acc']) is float:
            output_file.write("                      {{'agd84': [{}, {}], 'gda94': [{}, {}], 'acc': [{}, {}]}}".format(gdait_agd84_input_data[i]['lat'], gdait_agd84_input_data[i]['lon'],
                                                                                                                   gdait_agd84_output_data[i]['lat'], gdait_agd84_output_data[i]['lon'],
                                                                                                                   gdait_agd84_output_data[i]['lat_acc'], gdait_agd84_output_data[i]['lon_acc']))
        else:
            output_file.write("                      {{'agd84': [{}, {}], 'gda94': [{}, {}], 'acc': ['{}', '{}']}}".format(gdait_agd84_input_data[i]['lat'], gdait_agd84_input_data[i]['lon'],
                                                                                                                       gdait_agd84_output_data[i]['lat'], gdait_agd84_output_data[i]['lon'],
                                                                                                                       gdait_agd84_output_data[i]['lat_acc'], gdait_agd84_output_data[i]['lon_acc']))
        if data_count < len(gdait_agd84_input_data):
            output_file.write(",\n")
        else:
            output_file.write("\n")

    output_file.write('    ]\n')

    data_count = 0
    output_file.write('    gday_agd66_to_gda94 = [\n')
    for i in gday_agd66_input_data:
        data_count += 1
        if type(gday_agd66_output_data[i]['lat_acc']) is float and type(gday_agd66_output_data[i]['lon_acc']) is float:
            output_file.write("                      {{'agd66': [{}, {}], 'gda94': [{}, {}], 'acc': [{}, {}]}}".format(gday_agd66_input_data[i]['lat'], gday_agd66_input_data[i]['lon'],
                                                                                                                      gday_agd66_output_data[i]['lat'], gday_agd66_output_data[i]['lon'],
                                                                                                                      gday_agd66_output_data[i]['lat_acc'], gday_agd66_output_data[i]['lon_acc']))
        else:
            output_file.write("                      {{'agd66': [{}, {}], 'gda94': [{}, {}], 'acc': ['{}', '{}']}}".format(gday_agd66_input_data[i]['lat'], gday_agd66_input_data[i]['lon'],
                                                                                                                          gday_agd66_output_data[i]['lat'], gday_agd66_output_data[i]['lon'],
                                                                                                                          gday_agd66_output_data[i]['lat_acc'], gday_agd66_output_data[i]['lon_acc']))
        if data_count < len(gday_agd66_input_data):
            output_file.write(",\n")
        else:
            output_file.write("\n")
    output_file.write('    ]\n')
    output_file.write('\n')
    data_count = 0
    output_file.write('    gday_agd84_to_gda94 = [\n')
    for i in gday_agd84_input_data:
        data_count += 1
        if type(gday_agd84_output_data[i]['lat_acc']) is float and type(gday_agd84_output_data[i]['lon_acc']) is float:
            output_file.write("                      {{'agd84': [{}, {}], 'gda94': [{}, {}], 'acc': [{}, {}]}}".format(gday_agd84_input_data[i]['lat'], gday_agd84_input_data[i]['lon'],
                                                                                                                   gday_agd84_output_data[i]['lat'], gday_agd84_output_data[i]['lon'],
                                                                                                                   gday_agd84_output_data[i]['lat_acc'], gday_agd84_output_data[i]['lon_acc']))
        else:
            output_file.write("                      {{'agd84': [{}, {}], 'gda94': [{}, {}], 'acc': ['{}', '{}']}}".format(gday_agd84_input_data[i]['lat'], gday_agd84_input_data[i]['lon'],
                                                                                                                       gday_agd84_output_data[i]['lat'], gday_agd84_output_data[i]['lon'],
                                                                                                                       gday_agd84_output_data[i]['lat_acc'], gday_agd84_output_data[i]['lon_acc']))
        if data_count < len(gday_agd84_input_data):
            output_file.write(",\n")
        else:
            output_file.write("\n")

    output_file.write('    ]\n')
