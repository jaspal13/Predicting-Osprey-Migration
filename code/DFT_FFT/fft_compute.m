
% script to compute the fft
close all
clc
clear all

%% load the data for bird 120
locations = importdata('TotalBirdValuesbird120.csv');
data = locations.data;

long = data(:,1);
lat = data(:,2);

T_lat = bird_fft(lat,'minutes','latitude','Bird 120');
T_long = bird_fft(long,'minutes','longitude','Bird 120');


%% load the data for the average location of all birds per day
locations = importdata('latplotallbirdsaddeddays.csv');
data = locations.data;

lat = data(:,2);
long = data(:,1);

T_latall = bird_fft(lat,'days','latitude','Average of all birds per day');
T_longall = bird_fft(long,'days','longitude','Average of all birds per day');
