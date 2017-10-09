Steps to be followed for data preprocessing.

1. The movebank Data is imported into SQL server. 

2. Pre processing of data is done, removing certain improper data, taking only the necessary features.

3. The weather data is taken from Darksky.net and then combined with the existing database. Again imported into SQL server.

4. Final data extraction is done for all the types of data.
Note: SQL Server was chosen for this because of its capability to handle millions of data.

5. The csvs are generated . FinalOsprey.csv, AvgbirdDataWithWeather.csv, latplotallbirds.csv, TotalBirdValues.csv etc.

6. Importing of data into SQL has to be done manually.

7. All the necessary commands are mentioned in the file comp551_4.sql

Once this is done, each of these dataset is being referenced in the programs for K means clustering, LSTM and DFT.


Each algorithm contains its individual read me files in its folder