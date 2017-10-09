import datetime
import pandas as pd
import forecastio
import matplotlib.pyplot as plt
import numpy as np

# This file extracts weather data from each day of the study at the average location of all birds

# upload latitude and longitude
locations = np.genfromtxt("latplotallbirds.csv",
                             delimiter=',', 
                             dtype=[('time', np.float32), ('latitude', np.float32), ('longitude', np.float32)], 
                             usecols=(1, 2), skip_header=1)

# api key from darksky
api_key = "0342692bd64fcf2f4d158352432e5309"

# in total we have 3384 days

# first day
y = 2010
m = 1
d = 19
start = datetime.datetime(y,m,d)

# number of days
num_days = 50
latitude = np.zeros((num_days,1))
longitude = np.zeros((num_days,1))

# weather acquired so far
so_far = pd.DataFrame(columns=['pressure','temperature'])

# loop through days
for day in range(num_days):
    # get date
    date = start + datetime.timedelta(day)
    
    # get location
    lat = locations[day][0]
    lng = locations[day][1]
    
    # get the forecast
    forecast = forecastio.load_forecast(api_key, lat, lng, time=date, units='si')

    # get daily data
    daily = forecast.daily()
    
    daily_data = pd.DataFrame(columns=['pressure','humidity','precipProbability','windBearing','windSpeed','temperatureMax','temperatureMin'])

    for dailyData in daily.data:
        daily_data = daily_data.append({'date':dailyData.time, 'windBearing':dailyData.windBearing, 'windSpeed':dailyData.windSpeed, 'temperatureMax': dailyData.temperatureMax, 'temperatureMin':dailyData.temperatureMin},ignore_index = True)

    # add to mother panda    
    so_far = so_far.append(daily_data)

# put in csv file
so_far.to_csv('weather'+str(y) + str(m) + str(d)+'.csv',date_format='%Y-%m-%d')


# get an ugly plot
#plt.style.use('ggplot')
#so_far.plot(subplots=True)

