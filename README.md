# COMS6111 Project 2
COMS6111 Project 2

Group Name
--------
Project 2 Group 27

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

2. Map the original NYC Open Data data set into our INTEGRATED-DATASET file

3. INTEGRATED-DATASET file 


Internal Design
---------


Command Line Specification
---------

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
