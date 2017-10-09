import numpy as np
from datetime import datetime
from datetime import timedelta
import csv


# This file takes a dataset with frequent samples and turns it into an hourly dataset by removing records and adding missing records


# import the data
def getdata(filename,birdId):

    locations = np.genfromtxt(filename+'.csv', delimiter=',', dtype=[('latitude', np.float32), ('longitude', np.float32), ('ID',int), ('time',datetime)], usecols=(1, 2, 3, 0), skip_header=1)
    # sepcify the desired bird
#    birdId = 120
    ids = np.asarray([i[2] for i in locations])
    # get the timestamps for the records
    times = np.asarray([bytes.decode(i[3]) for i in locations if i[2] == birdId])
    # get latitude and longitude data
    locations = np.asarray([(i[1],i[0]) for i in locations if i[2]==birdId])
    
    return locations, times, ids
    
    
# write output to a csv file
def write_file(output_filename, times, locations):

	with open(output_filename, 'w', newline='') as csvfile:
		wr = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
		wr.writerow(['timestamp', 'latitude','longitude'])
		for i in range(0, len(times)):
			wr.writerow([times[i], locations[i][0], locations[i][1]])


# if there is more than one record per hour, the first record during that hour is kept
def remove_repetitions(times,locations):
    n = times.shape[0]
    new_times = np.copy(times)
    new_locations = np.copy(0*locations)
    
    i=0
    ii=0
    
    # loop through original times and locations
    while i < n:
        # find the hour of record i
        date_object = datetime.strptime(times[i],'%Y-%m-%d %H:%M:%S')
        hour = date_object.hour
        
        # add the record
        new_times[ii] = times[i]
        new_locations[ii] = locations[i]
        
        ii = ii+1
    
        if i == n-1:
            k=1
            break
        
        k=0
        # count the number of times the hour is repeated
        for j in range(i+1,n):
            date_object_next = datetime.strptime(times[j],'%Y-%m-%d %H:%M:%S')
            hour_next = date_object_next.hour
            k=k+1
            if hour_next != hour:
                break
        # skip k records
        i=i+k
    
    # trim the new times and locations arrays
    new_lat = new_locations[:,0]
    new_long = new_locations[:,1]
    
    new_lat = np.trim_zeros(new_lat)
    new_long = np.trim_zeros(new_long)
    m = new_lat.shape[0]
    
    new_lat = np.transpose(np.array([new_lat]))
    new_long = np.transpose(np.array([new_long]))
    
    new_locations = np.concatenate((new_lat,new_long), axis=1)
    m = new_locations.shape[0]
    
    new_times = new_times[0:m]
    
    return new_times, new_locations
    
# add the hours that are missing by doing linear interpolation
def add_missing(new_times,new_locations):
    m = new_locations.shape[0]
    
    # for each record
    for ii in range(m-1):
        
        # find difference in hour between two records
        date_object = datetime.strptime(new_times[ii],'%Y-%m-%d %H:%M:%S')
        hour = date_object.hour
        
        date_object_next = datetime.strptime(new_times[ii+1],'%Y-%m-%d %H:%M:%S')
        hour_next = date_object_next.hour
        
#        if hour_next == 0:
#            hour_next = 24
        diff_hour = hour_next-hour

        # if there is at least one hour missing        
        if diff_hour != 1:
            
            # check if there is a difference in days as well
            day = date_object.day
            day_next = date_object_next.day
            diff_day = day_next-day
            # adjust hour difference
            if diff_day > 0:
                diff_hour = 24*diff_day+diff_hour

            # add additional records with linear interpolation
            for n in range(diff_hour-1):
                # if difference is diff_hour, want to add diff_hour-1 in between
            
                # add a timestamp
                new_time = date_object + (n+1)*timedelta(hours=1)
                new_times = np.insert(new_times,ii+1+n,new_time,axis=0)
                
                # add a location
                if n == 0:
                    f_a = new_locations[ii]
                    f_b = new_locations[ii+1]   
                a = 0
                b = diff_hour
                loc_new = f_a + (f_b-f_a)/(b-a)*(n+1-a)
                loc_new = np.array([loc_new])
                new_locations = np.insert(new_locations,ii+1+n,loc_new,axis=0)
                    
        # skip added records in loop
        m = new_times.shape[0]
        
    return new_times, new_locations


filename = 'TotalBirdValues'
birdId = 388

locations,times,ids = getdata(filename, birdId)
write_file(filename+'getdata.csv', times, locations)

times, locations = remove_repetitions(times,locations)
write_file(filename+'remove_rep.csv', times, locations)

times, locations = add_missing(times, locations)

write_file(filename+'bird'+str(birdId)+'.csv', times, locations)


