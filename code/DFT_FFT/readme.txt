Weather extraction

get_weather.py
Run this with an API Key from Dark Sky API and latplotallbirds.csv to get average weather data for each day of the study at the average location of all birds


Extra pre-processing for FFT

uniform_hours.py
Run this file with a specific bird ID to get uniform hourly sampling
This needs TotalBirdValues.csv and outputs TotalBirdValuesbird120.csv

uniform_days.py
Run this file to get uniform daily sampling
This needs laplotallbirds.csv and outputs latplotallbirdsaddeddays.csv


FFT computation

fft_compute.m
Run this script to set up the data and run the FFT
This needs the following data:
TotalBirdValuesbird120.csv
latplotallbirdsaddeddays.csv

bird_fft.m
The FFT algorithm called by fft_compute.m

smooth.m and mov_avg.m
Used in bird_fft to remove noise in the data.