import numpy as np
from datetime import datetime
from datetime import timedelta
import csv


# This file takes a dataset with (nearly) daily samples and adds missing records


# import the data
def getdata(filename):

    locations = np.genfromtxt(filename+'.csv', delimiter=',', dtype=[('latitude', np.float32), ('longitude', np.float32), ('time',datetime)], usecols=(1, 2, 0), skip_header=1)

    # get the timestamps for the records
    times = np.asarray([bytes.decode(i[2]) for i in locations])
    # get latitude and longitude data
    locations = np.asarray([(i[1],i[0]) for i in locations])
    
    return locations, times
    
    
# write output to a csv file
def write_file(output_filename, times, locations):

	with open(output_filename, 'w', newline='') as csvfile:
		wr = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
		wr.writerow(['timestamp', 'latitude','longitude'])
		for i in range(0, len(times)):
			wr.writerow([times[i], locations[i][0], locations[i][1]])


# add the days that are missing by doing linear interpolation
def add_missing(new_times,new_locations):
    m = new_locations.shape[0]
    
    # for each record
    for ii in range(m-1):
        
        # find difference in day between two records
        date_object = datetime.strptime(new_times[ii],'%Y-%m-%d')
        day = date_object.day
        
        date_object_next = datetime.strptime(new_times[ii+1],'%Y-%m-%d')
        day_next = date_object_next.day
        
        diff_day = day_next-day

        # if there is at least one day missing        
        if diff_day != 1:
            
            # check if there is a difference in months as well
            month = date_object.month
            month_next = date_object_next.month
            diff_month = month_next-month
            # adjust day difference
            if diff_month > 0:
                year = date_object.year
                if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
                    mult = 31
                elif month == 4 or month == 6 or month == 9 or month == 11:
                    mult = 30
                elif month == 2 and (year == 2016 or year == 2012 or year == 2008):
                    mult = 29
                else:
                    mult = 28
                diff_day = mult*diff_month+diff_day

            # add additional records with linear interpolation
            for n in range(diff_day-1):
                # if difference is diff_day, want to add diff_day-1 in between
            
                # add a timestamp
                new_time = date_object + (n+1)*timedelta(days=1)
                new_times = np.insert(new_times,ii+1+n,new_time,axis=0)
                
                # add a location
                if n == 0:
                    f_a = new_locations[ii]
                    f_b = new_locations[ii+1]   
                a = 0
                b = diff_day
                loc_new = f_a + (f_b-f_a)/(b-a)*(n+1-a)
                loc_new = np.array([loc_new])
                new_locations = np.insert(new_locations,ii+1+n,loc_new,axis=0)
                    
        # skip added records in loop
        m = new_times.shape[0]
        
    return new_times, new_locations


filename = 'latplotallbirds'

locations,times = getdata(filename)
write_file(filename+'getdata.csv', times, locations)

times, locations = add_missing(times, locations)
write_file(filename+'addeddays.csv', times, locations)

