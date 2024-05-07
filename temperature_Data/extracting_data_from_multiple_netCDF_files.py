import glob
from netCDF4 import Dataset
import pandas as pd
import numpy as np

#record all the years of the netCDF4 files into a python list
all_years = []

for file in glob.glob('*.nc'):
    #will prevent to pick other kinds of files
    #*.nc means detect all files with .nc extension
    print(file)
    data = Dataset(file, 'r') #'r' means reading mod form dataset
    time = data.variables['time']
    #time = data.variables['time'].units variable further specification
    year = time.units[14:18]
    #index of data 
    all_years.append(year)

#Creating an empty Pandas DataFrame covering the whole range of data
    year_start = min(all_years)
    year_end = max(all_years) 

    date_range = pd.date_range (start = str(year_start) + '-01-01',    
                                end = str(year_end) + '-12-31',
                                freq = 'D')#daily M monthly etc.
    df = pd.DataFrame(0.0, columns = ['Temperature'], index = date_range)
    
    #Defining the coordinates by lat, lon for the location of your interest

    lat_katmandu = 27.697817
    lon_katmandu = 85.329806

    #sorting the all_years by order python list
    all_years.sort() 

for yr in all_years:
    #reading in data
    data = Dataset(str(yr)+'.nc', 'r')

    #storing the lat and lon data of the netCDF file into variables
    lat = data.variables['lat'][:]
    lon = data.variables['lon'][:]

    #squared fifference between the specified lat, lon and the of the netCDF
    sq_diff_lat = (lat - lat_katmandu)**2
    sq_diff_lon = (lon - lon_katmandu)**2
    #identify the index of the min value for lat and lon 
    min_index_lat = sq_diff_lat.argmin()
    min_index_lon = sq_diff_lon.argmin()

    #Accessing the average temperature data
    temp = data.variables['tave']
    #Creating the date range for each year during each iteration
    start = str(yr) + '-01-01'  
    end = str(yr) + '-12-31'  
    d_range = pd.date_range(start = start,
                            end = end,
                            freq ='D')
    for t_index in np.arange(0, len(d_range)):
        print('Recording the value for: ' + str(d_range[t_index]))
        df.loc[d_range[t_index]]['Temperature'] = temp[t_index, min_index_lat, min_index_lon]

    df.to_csv('temperature_Katmandu_1961_1966.csv')