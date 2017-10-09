#This code is divided into 3 parts
#You need the csv named finalosprey.csv to run it. It is the original dataset after pre-processing.The SQL queries to generate it are mentioned in another instruction file
#The first part runs the k-means clustering on all birds to give 3 cluster points
#The second part runs k-means to see migration patterns for a single bird(birdId: 120)
#The third part calculates the performance metrics as mentioned in the result section of the report
#Uncomment the appropriate code to execute that part

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.patches as mpatches
from datetime import date
import datetime as dt
from sklearn.metrics import classification_report

locations = np.genfromtxt("finalosprey.csv",
                         delimiter=',',
                         dtype=[('latitude', np.float32), ('longitude', np.float32),('ID',int),('Time',dt.datetime)],
                         usecols=(2,3,7,1), skip_header=1)
#==================================Part 1 k-means clustering on all birds====================================
'''
locations = np.asarray([(i[1],i[0]) for i in locations])
kmeans = KMeans(n_clusters=3, random_state=0).fit(locations)
x,y = zip(*locations)
x1,y1 = zip(*kmeans.cluster_centers_)
h = .02
x_min, x_max = min(x) - 1, max(x) + 1
y_min, y_max = min(y) - 1, max(y) + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.figure(1)
plt.clf()
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plt.cm.Paired,
           aspect='auto', origin='lower')
plt.scatter(x1, y1,
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)
plt.plot(x, y, 'k.', markersize=2,color = 'black')
red_patch = mpatches.Patch(color='brown',label = 'South America')
green_patch = mpatches.Patch(color='#33D1FF',label = 'Cuba and Caribbean Sea')
blue_patch = mpatches.Patch(color='#FF5733',label = 'North America')
plt.legend(loc='upper right',handles=[blue_patch,green_patch,red_patch])
matplotlib.rcParams.update({'font.size':20})
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
'''
#==================================Part 2 k-means clustering for one bird====================================
'''
birdId = [120]
loc = np.asarray([(i[0],i[1],i[3]) for i in locations if i[2] in birdId])
locations = np.asarray([(i[1],i[0]) for i in locations if i[2] in birdId])
loc1 = []
loc2 = []
for i in loc:
	if (i[2] > '2013-09-01 00:00:00' and i[2] < '2014-03-01 00:00:00') or (i[2] > '2014-09-01 00:00:00' and i[2] < '2015-03-01 00:00:00') or (i[2] > '2015-09-01 00:00:00' and i[2] < '2016-03-01 00:00:00'):
		loc1.append([i[1],i[0]])
	else:
		loc2.append([i[1],i[0]])
kmeans = KMeans(n_clusters=3, random_state=0).fit(locations)
x,y = zip(*locations)
xa,ya = zip(*loc1)
xb,yb = zip(*loc2)
x1,y1 = zip(*kmeans.cluster_centers_)
h = .02
x_min, x_max = min(x) - 1, max(x) + 1
y_min, y_max = min(y) - 1, max(y) + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

Z = Z.reshape(xx.shape)
plt.figure(1)
plt.clf()
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plt.cm.Paired,
           aspect='auto', origin='lower')

plt.plot(xa, ya, 'k.', markersize=2,color = 'm')
plt.plot(xb, yb, 'k.', markersize=2,color = 'g')
plt.scatter(x1, y1,
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)
red_patch = mpatches.Patch(color='brown',label = 'Cuba and Caribbean Sea')
green_patch = mpatches.Patch(color='#33D1FF',label = 'South America')
blue_patch = mpatches.Patch(color='#FF5733',label = 'North America')
plt.legend(loc='upper right',handles=[blue_patch,red_patch,green_patch])
matplotlib.rcParams.update({'font.size':20})
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
'''
#==================================Part 3 Performance metrics for k-means====================================
#'''
locations = np.asarray([(j,i[1],i[0]) for j,i in enumerate(locations)])
northAmerica = []
southAmerica = []
cuba = []
y=[]
for j,i in enumerate(locations):
  if i[2]>25:
    northAmerica.append([i[1],i[2]])
    y.append(0)
  elif i[2]<25 and i[2]>9:
    cuba.append([i[1],i[2]])
    y.append(1)
  else:
    southAmerica.append([i[1],i[2]])
    y.append(2)
kmeans = KMeans(n_clusters=3, random_state=42).fit(locations[:,1:3])
target_names = ['North America', 'Cuba & Caribbean Sea', 'South America']
print(classification_report(y, kmeans.labels_, target_names=target_names))
locations = locations[:,1:3]
x,y = zip(*locations)
xNA,yNA = zip(*northAmerica)
xCU,yCU = zip(*cuba)
xSA,ySA = zip(*southAmerica)
x1,y1 = zip(*kmeans.cluster_centers_)
h = .02
x_min, x_max = min(x) - 1, max(x) + 1
y_min, y_max = min(y) - 1, max(y) + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.figure(1)
plt.clf()
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plt.cm.Paired,
           aspect='auto', origin='lower')

kab, = plt.plot(xNA, yNA, 'k.', markersize=10,color = 'm',label = 'North America')
kab2, = plt.plot(xSA, ySA, 'k.', markersize=10,color = 'g',label = 'South America')
kab3, = plt.plot(xCU,yCU,'k.',markersize = 10,color = 'b',label = 'Cuba')
plt.scatter(x1, y1,
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)
red_patch = mpatches.Patch(color='brown',label = 'South America')
green_patch = mpatches.Patch(color='#33D1FF',label = 'North America')
blue_patch = mpatches.Patch(color='#FF5733',label = 'Cuba and Caribbean Sea')
plt.legend(handles=[kab2,kab3,kab,red_patch,blue_patch,green_patch],loc='upper right',prop={'size':15})
matplotlib.rcParams.update({'font.size':20})
plt.xlabel("Latitude")
plt.ylabel("Longitude")
plt.show()
#'''
