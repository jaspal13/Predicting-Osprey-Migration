--Movebank data needs to be imported into these tables in an ML database.
--Final script to be executed for generating the data (at the end of the script)

--Pre processing of data. 
USE ML
GO


SELECT [tag-local-identifier],count(*) as c FROM ospreydata
GROUP BY [tag-local-identifier]
order by c desc


GO


SELECT MAX([location-lat]),MIN([location-lat]),
MAX([location-long]),MIN([location-long]) 
FROM ospreydata

UPDATE ospreydata
SET [height-raw] = REPLACE([height-raw],'"','')

SELECT *,
geography::Point([Latitude], [Longitude], 4326) as point
INTO FinalOsprey
FROM (
SELECT CAST([event-id] as INT) as eventid,
CONVERT(SMALLDATETIME,timestamp) as currtime,
[location-lat] as latitude,
[location-long]  as longitude,
CAST([ground-speed] as FLOAT) as groundspeed,
CAST(heading as FLOAT) as heading,
ISNULL(TRY_CAST(REPLACE([height-raw],'"','') as INT),0) as height,
CAST(REPLACE([tag-local-identifier],'"','') as INT) as ID
FROM ospreydata
WHERE [sensor-type] = '"gps"'
)T


WHERE [argos altitude] <>'' and [sensor-type]='gps'

ALTER TABLE ospreydata
ADD CONSTRAINT pk_eventid PRIMARY KEY ([event-id])

SELECT top 10 * FROM ospreydata

DECLARE @lat1 VARCHAR(30) = '38.78033'
DECLARE @long1 VARCHAR(30) = '-75.10517'
DECLARE @lat2 VARCHAR(30) = '37.78433'
DECLARE @long2 VARCHAR(30) = '-72.6875'

DECLARE @source geography = geography::Point(@lat1, @long1, 4326) 
DECLARE @target geography = geography::Point(@lat2, @long2, 4326) 

select @source

SELECT @source.STDistance(@target)
 
 ------------------------------------------------------------------
 SELECT distinct id  FROM ML..FinalOsprey
WHERE [location-lat] = ''

SELECT *,
geography::Point([Latitude], [Longitude], 4326) as point
INTO FinalOsprey49ds
FROM (
SELECT CAST([event-id] as INT) as eventid,
CONVERT(SMALLDATETIME,timestamp) as currtime,
[location-lat] as latitude,
[location-long]  as longitude,
0 as groundspeed,
'' as heading,
ISNULL(TRY_CAST(REPLACE([height-raw],'"','') as INT),0) as height,
CAST(REPLACE([tag-local-identifier],'"','') as INT) as ID
FROM ML..Osprey49ds
WHERE [sensor-type] = '"gps"'
)T

------------------------------------------------------------------

USE ML
GO


SELECT *,
geography::Point([Latitude], [Longitude], 4326) as point
--INTO Finalblackbackedgull
FROM (
SELECT CAST([event-id] as INT) as eventid,
CONVERT(SMALLDATETIME,timestamp) as currtime,
[location-lat] as latitude,
[location-long]  as longitude,
CAST([ground-speed] as FLOAT) as groundspeed,
CAST(heading as FLOAT) as heading,
CAST([height-above-msl] as FLOAT) as height,
--ISNULL(TRY_CAST(REPLACE([height-raw],'"','') as INT),0) as height,
REPLACE([tag-local-identifier],'"','') as ID
FROM blackbackedgull
WHERE [sensor-type] = '"gps"'
)T

SELECT datepart(dayofyear, tme) as D, * FROM
(
SELECT CAST(currtime as DATE) as tme,AVG(CAST(latitude as FLOAT)) as latitude,
AVG(CAST(longitude as FLOAT)) as longitude ,ID
FROM FinalOsprey
GROUP BY CAST(currtime as DATE),ID
)T
ORDER BY ID,tme

SELECT datepart(dayofyear, tme) as D, * FROM
(
SELECT CAST(currtime as DATE) as tme,AVG(CAST(latitude as FLOAT)) as latitude,
AVG(CAST(longitude as FLOAT)) as longitude 
FROM FinalOsprey
GROUP BY CAST(currtime as DATE)
)T
ORDER BY T.tme

-----------------------------------------------------------------

USE ML
GO

--DROP TABLE #temp
SELECT ID,COUNT(*) AS C 
INTO #temp
FROM FinalOsprey
WHERE ID IN (120,121,122,389,19,66699,117,118,820,119)
GROUP BY ID
ORDER BY C DESC


SELECT datepart(dayofyear,Currtime) as D, Currtime,latitude,longitude,F.ID FROM FinalOsprey F
INNER JOIN #temp S
ON F.ID = S.ID
ORDER BY S.C DESC,F.Currtime ASC


SELECT MAX(CAST(latitude AS FLOAT)),MIN(CAST(latitude AS FLOAT)) FROM FinalOsprey

SELECT * FROM FinalOsprey
WHERE latitude = '-17.33268'


66699
19


SELECT DATEPART(DD,currtime) as D,currtime,latitude,longitude,ID FROM FinalOsprey
WHERE ID = 120

select datepart(dayofyear, getdate())


USE ML
GO

SELECT * FROM ML..latplotallbirds_weather


USE ML
GO

SELECT * FROM ML..latplotallbirds_weather

--------------------------------------------------------------------------------------------------------
--Final Script to be run for getting the data
SELECT datepart(dayofyear, tme) as D, * FROM
(
SELECT [Date] as tme,AVG(CAST(latitude as FLOAT)) as latitude,
AVG(CAST(longitude as FLOAT)) as longitude,AVG(cast(temperatureMax as FLOAT) + cast(temperatureMin as FLOAT))/2.0 as Temp 
FROM latplotallbirds_weather
GROUP BY [Date]
)T
ORDER BY T.tme

GO

USE ML
GO

--DROP TABLE #temp
SELECT ID,COUNT(*) AS C 
INTO #temp
FROM FinalOsprey
WHERE ID IN (120,121,122,389,19,66699,117,118,820,119)
GROUP BY ID
ORDER BY C DESC


SELECT datepart(dayofyear,Currtime) as D, Currtime,latitude,longitude,F.ID FROM FinalOsprey F
INNER JOIN #temp S
ON F.ID = S.ID
ORDER BY S.C DESC,F.Currtime ASC

------------------------------------------------------------------------------------------------------------


