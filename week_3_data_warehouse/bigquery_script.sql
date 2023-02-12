-- Created external table
CREATE OR REPLACE EXTERNAL TABLE `dtc-de-27012023.trips_data_all.fhv_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://prefect-de-zoomcamp_2023/data/fhv_tripdata_2019-*.csv']
);


-- Counted table records
SELECT COUNT(*) FROM `dtc-de-27012023.trips_data_all.fhv_tripdata`;


-- Counted records by condition 
SELECT COUNT(1) 
FROM `dtc-de-27012023.trips_data_all.fhv_tripdata` 
WHERE PUlocationID IS NULL 
  AND DOlocationID IS NULL;


-- Non-partitioned table
SELECT DISTINCT Affiliated_base_number
FROM `dtc-de-27012023.trips_data_all.fhv_tripdata_internal`
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31'


-- Partitioned table
SELECT DISTINCT Affiliated_base_number
FROM `dtc-de-27012023.trips_data_all.fhv_tripdata_partitioned`
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31'