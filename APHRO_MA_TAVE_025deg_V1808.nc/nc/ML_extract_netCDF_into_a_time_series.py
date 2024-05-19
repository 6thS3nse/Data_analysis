import glob
from netCDF4 import Dataset
import pandas as pd
import numpy as np

# Define the range of years you want to process
start_year_str = 'APHRO_MA_TAVE_025deg_V1808.1961'
end_year_str = 'APHRO_MA_TAVE_025deg_V1808.2015'

# Extracting years from the file names
start_year = int(start_year_str.split('.')[-1])
end_year = int(end_year_str.split('.')[-1])

# Record all the years of the netCDF4 files into a python list
all_years = []
#During the generation of the all_years list, the code does not access the netCDF files or their names
for year in range(start_year, end_year + 1):
    all_years.append(year)

# Creating an empty list to store data
data_rows = []

# Defining the coordinates by lat, lon for the location of your interest
lat_katmandu = 27.697817
lon_katmandu = 85.329806

# Sorting the all_years by order python list
all_years.sort()

for yr in all_years:
    # reading in data
    data = Dataset(f"APHRO_MA_TAVE_025deg_V1808.{yr}.nc", 'r')

    # storing the lat and lon data of the netCDF file into variables
    lat = data.variables['lat'][:]
    lon = data.variables['lon'][:]

    # squared difference between the specified lat, lon and the of the netCDF
    sq_diff_lat = (lat - lat_katmandu) ** 2
    sq_diff_lon = (lon - lon_katmandu) ** 2
    # identify the index of the min value for lat and lon
    min_index_lat = sq_diff_lat.argmin()
    min_index_lon = sq_diff_lon.argmin()

    # Accessing the average temperature data
    temp = data.variables['tave']
    # Accessing the 'rstn' data
    rstn = data.variables['rstn']

    # Creating the date range for each year during each iteration
    start = f"{yr}-01-01"
    end = f"{yr}-12-31"
    d_range = pd.date_range(start=start, end=end, freq='D')
    
    for t_index, date in enumerate(d_range):
        temp_val = temp[t_index, min_index_lat, min_index_lon]
        rstn_val = rstn[t_index, min_index_lat, min_index_lon]
        data_rows.append([f"{date.strftime('%Y-%m-%d')}", temp_val, rstn_val])
        # Print index and date
        print('Recording the value for date {} and index {}'.format(date, t_index))

# Creating DataFrame
df = pd.DataFrame(data_rows, columns=['Date', 'Temperature', 'RSTN'])

# Writing DataFrame to CSV
df.to_csv('temperature_rstn_Katmandu.csv', index=False)