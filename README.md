# COMS6111 Project 3
COMS6111 Project 3

Group Name
--------
Project 3 Group 27

Group Member
--------
   Qianwen Zheng (qz2271)

   Jiajun Zhang (jz2793)
   
Files
--------
	file-tree

Run
--------

1. Clone project
	Install git if you haven't

		sudo apt-get install git

	then, clone project
	
		git clone https://github.com/petercanmakit/group27-proj3.git

2. Navigate to folder

		cd ./group27-proj3

3. Install dependencies

		sudo apt install python-pip
		sudo pip install -r requirements.txt
		
4. Run program
		
		python app.py INTEGRATED-DATASET.csv [min_supp] [min_conf]
		
Description
---------
1. The data set

	We use the [311 Service Requests From 2015](https://data.cityofnewyork.us/dataset/311-Service-Requests-From-2015/57g5-etyj) dataset.

2. Map the original NYC Open Data data set into our INTEGRATED-DATASET file
	
	* We use progreSQL to store all data in a SQL table (i.e. talbe 'table311'). The table contains all attributes of the dataset.
	
	  ```sql
		create table table311 (
			Unique_Key int ,
			Created_Date date ,
			Closed_Date date ,
			Agency text ,
			Agency_Name text ,
			Complaint_Type text ,
			Descriptor text ,
			Location_Type text ,
			Incident_Zip text ,
			Incident_Address text ,
			Street_Name text ,
			Cross_Street_1 text ,
			Cross_Street_2 text ,
			Intersection_Street_1 text ,
			Intersection_Street_2 text ,
			Address_Type text ,
			City text ,
			Landmark text ,
			Facility_Type text ,
			Status text ,
			Due_Date date ,
			Resolution_Description text ,
			Resolution_Action_Updated_Date date ,
			Community_Board text ,
			Borough text ,
			X_Coordinate_State_Plane real ,
			Y_Coordinate_State_Plane real ,
			Park_Facility_Name text ,
			Park_Borough text ,
			School_Name text ,
			School_Number text ,
			School_Region text ,
			School_Code text ,
			School_PhoneP_Number text ,
			School_Address text ,
			School_City text ,
			School_State text ,
			School_Zip text ,
			School_Not_Found text ,
			School_or_Citywide_Complaint text ,
			Vehicle_Type text ,
			Taxi_Company_Borough text ,
			Taxi_Pick_Up_Location text ,
			Bridge_Highway_Name text ,
			Bridge_Highway_Direction text ,
			Road_Ramp text ,
			Bridge_Highway_Segment text ,
			Garage_Lot_Name text ,
			Ferry_Direction text ,
			Ferry_Terminal_Name text ,
			Latitude real ,
			Longitude real ,
			Location text  
		);
	  ```
	
	  Command Line
	
	  ```
	  \copy table311 FROM '/Users/peter/Study/17Fall/6111/project3/311_Service_Requests_from_2015.csv'  DELIMITER ',' CSV HEADER
	  ```
	
	* We create a new table (i.e. table 'table311small') where we select several attributes(i.e. 'Created_Date', 'Complaint_Type', 'Descriptor', 'Community_Board') that we need. 
	
	  SQL

	  ```sql
	  create table table311small (
	  	Unique_Key int ,
	  	Created_Date date ,
	  	Complaint_Type text ,
	  	Descriptor text ,
	  	Community_Board text  
	  );
	  ```
		
	  Command Line
	
	  ```
	  \copy (Select Unique_Key, Created_Date, Complaint_Type, Descriptor, Community_Board From table311) To '/Users/peter/Study/17Fall/6111/project3/311_2015_tmp.csv' With CSV HEADER;
	  \copy table311small FROM '/Users/peter/Study/17Fall/6111/project3/311_2015_tmp.csv'  DELIMITER ',' CSV HEADER
	  ```

	  And then, we eliminate records whose 'Community Board' is '0 Unspecified' or 'Complaint_Type' is 'Missed Collection (All Materials)'.

	  ```
	  DELETE FROM table311small where Community_Board = '0 Unspecified';
	  DELETE FROM table311small where Complaint_Type = 'Missed Collection (All Materials)';
	  ```
	  Do deduplication and sort the record. Output the talbe into a new csv file in order to generate 'item' and 'market busket'
	  ```
	  \copy (Select distinct community_board, created_date, complaint_type, Descriptor From table311small Order By community_board, created_date, complaint_type, Descriptor) To '/Users/peter/Study/17Fall/6111/project3/311_2015_remove2.csv' With CSV HEADER;
	  ```
	
	* Generate the INTEGRATED-DATASET.csv file 
	
	  An 'item' is generated as a format of 'Complaint_Type(Descriptor)'. A 'market busket' is consisted of all complaints that happend at the same community in the same day. That is, let (Created_Date, Community_Board) as the 'transaction id', and the items in this 'transaction' are 'Complaint_Type(Descriptor)'s with the same 'Created_Date' and 'Community_Board'.
	
	  To generate the INTEGRATED-DATASET.csv file, run ```python clean.py```
	
3. INTEGRATED-DATASET file 
	
	We believe complaints happened in a community at one day are most likely related with each other. And this is also the reason why we consider ('Community_Board', 'Created_Date') as the 'transaction id' to generate 'market busket'.


Internal Design
---------


Command Line Specification
---------
The parameter value we choose are min_Supp = 0.35,  min_Conf = 0.82
  ```
  python app.py INTEGRATED-DATASET.csv 0.35 0.82
  ```
And here are some typical rules that we got.

  1. \[blocked driveway(no access), noise - residential(banging/pounding)] => \[noise - residential(loud music/party)] (Conf: 90.1384%, Supp: 49.5273%)
  
  2. \[noise - residential(banging/pounding)] => \[noise - residential(loud music/party)] (Conf: 89.8577%, Supp: 61.7281%)

  3. \[illegal parking(posted parking sign violation), noise - residential(banging/pounding)] => \[noise - residential(loud music/party)] (Conf: 88.641%, Supp: 36.6024%)
  
  4. \[blocked driveway(no access)] => \[noise - residential(loud music/party)] (Conf: 87.9943%, Supp: 59.9702%)

  5. \[sanitation condition(15 street cond/dump-out/drop-off)] => \[blocked driveway(no access)] (Conf: 82.1097%, Supp: 38.1069%)






Original dataset: https://data.cityofnewyork.us/dataset/311-Service-Requests-From-2015/57g5-etyj

		create table table311 (
			Unique_Key int ,
			Created_Date date ,
			Closed_Date date ,
			Agency text ,
			Agency_Name text ,
			Complaint_Type text ,
			Descriptor text ,
			Location_Type text ,
			Incident_Zip text ,
			Incident_Address text ,
			Street_Name text ,
			Cross_Street_1 text ,
			Cross_Street_2 text ,
			Intersection_Street_1 text ,
			Intersection_Street_2 text ,
			Address_Type text ,
			City text ,
			Landmark text ,
			Facility_Type text ,
			Status text ,
			Due_Date date ,
			Resolution_Description text ,
			Resolution_Action_Updated_Date date ,
			Community_Board text ,
			Borough text ,
			X_Coordinate_State_Plane real ,
			Y_Coordinate_State_Plane real ,
			Park_Facility_Name text ,
			Park_Borough text ,
			School_Name text ,
			School_Number text ,
			School_Region text ,
			School_Code text ,
			School_PhoneP_Number text ,
			School_Address text ,
			School_City text ,
			School_State text ,
			School_Zip text ,
			School_Not_Found text ,
			School_or_Citywide_Complaint text ,
			Vehicle_Type text ,
			Taxi_Company_Borough text ,
			Taxi_Pick_Up_Location text ,
			Bridge_Highway_Name text ,
			Bridge_Highway_Direction text ,
			Road_Ramp text ,
			Bridge_Highway_Segment text ,
			Garage_Lot_Name text ,
			Ferry_Direction text ,
			Ferry_Terminal_Name text ,
			Latitude real ,
			Longitude real ,
			Location text  
		);


		\copy table311 FROM '/Users/peter/Study/17Fall/6111/project3/311_Service_Requests_from_2015.csv'  DELIMITER ',' CSV HEADER

		\copy (Select Unique_Key, Created_Date, Complaint_Type, Descriptor, Community_Board From table311) To '/Users/peter/Study/17Fall/6111/project3/311_2015_tmp.csv' With CSV HEADER;


```sql
	create table table311small (
	Unique_Key int ,
	Created_Date date ,
	Complaint_Type text ,
	Descriptor text ,
	Community_Board text  
	);

	\copy table311small FROM '/Users/peter/Study/17Fall/6111/project3/311_2015_tmp.csv'  DELIMITER ',' CSV HEADER

	DELETE FROM table311small where Community_Board = '0 Unspecified';
	DELETE FROM table311small where Complaint_Type = 'Missed Collection (All Materials)';

	\copy (Select distinct community_board, created_date, complaint_type From table311small Order By community_board, created_date, complaint_type) To '/Users/peter/Study/17Fall/6111/project3/311_2015_remove0.csv' With CSV HEADER;

	\copy (Select distinct community_board, created_date, Descriptor From table311small Order By community_board, created_date, Descriptor) To '/Users/peter/Study/17Fall/6111/project3/311_2015_remove1.csv' With CSV HEADER;

    \copy (Select distinct community_board, created_date, complaint_type, Descriptor From table311small Order By community_board, created_date, complaint_type, Descriptor) To '/Users/peter/Study/17Fall/6111/project3/311_2015_remove2.csv' With CSV HEADER;
```
