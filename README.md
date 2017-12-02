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
	./group27-proj3/
	├── 311_2015.csv
	├── INTEGRATED-DATASET.csv
	├── README.md
	├── aPriori.py
	├── app.py
	├── clean.py
	├── example-run.txt
	├── output.txt
	└── read_file.py

Run
--------

1. Clone project
	Install git if you haven't

		sudo apt-get install git

	then, clone project

		git clone https://github.com/petercanmakit/group27-proj3.git

2. Navigate to folder

		cd ./group27-proj3

3. Run program

		python app.py INTEGRATED-DATASET.csv [min_supp] [min_conf]

Description
---------
1. The data set

	We use the [311 Service Requests From 2015](https://data.cityofnewyork.us/dataset/311-Service-Requests-From-2015/57g5-etyj) dataset. It contains information of 311 complaint service records, including complaint types, date, communities and other details.

2. Map the original NYC Open Data data set into our INTEGRATED-DATASET file

	* After downloading the data csv file, we use <b>postgreSQL</b> to store all data in a SQL table (i.e. talbe 'table311'). The table contains all attributes of the dataset.

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
	  \copy table311 FROM 'path/to/311_Service_Requests_from_2015.csv'  DELIMITER ',' CSV HEADER
	  ```

	* We create a new table (i.e. table 'small311') where we select attributes(i.e. 'Created_Date', 'Complaint_Type', 'Descriptor', 'Community_Board') that we need.

	  SQL

	  ```sql
	  CREATE table small311
	  AS
	  SELECT Community_Board, Created_Date, Complaint_Type, Descriptor
	  From table311;
	  ```

	  And then, we eliminate useless records whose 'Community Board' contains 'Unspecified' or 'Complaint_Type' is 'Missed Collection (All Materials)'.

	  ```
	  DELETE FROM small311 where Community_Board LIKE '%Unspecified%';
	  DELETE FROM small311 where Complaint_Type = 'Missed Collection (All Materials)';
	  ```
	  Create a new csv file (311_2015.csv) to store data from small311 table without duplicate records.

	  ```
	  COPY (SELECT DISTINCT Community_Board, Created_Date, Complaint_Type, Descriptor FROM small311 order by Community_Board, Created_Date, Complaint_Type, Descriptor) To 'path/to/group27-proj3/311_2015.csv' With CSV HEADER
	  ```

	* Generate the INTEGRATED-DATASET.csv file

	  An 'item' is generated as a format of 'Complaint_Type(Descriptor)'. A 'market busket' is consisted of all complaints that happend at the same community in the same day. That is, let (Created_Date, Community_Board) as the 'transaction id', and the items in this 'transaction' are 'Complaint_Type(Descriptor)'s with the same 'Created_Date' and 'Community_Board'.

	  To generate the INTEGRATED-DATASET.csv file, run ```python clean.py```

3. INTEGRATED-DATASET file

	We believe complaints happened in a community at one day are most likely related with each other. And this is also the reason why we consider ('Community_Board', 'Created_Date') as the 'transaction id' to generate 'market busket'. That is, all complaints happend on the same date in the same community are itemsets in one market busket.


Internal Design
---------

1. Get the support of itemsets

	We have a dictionary to store itemset and its support value. When we call the ```supp(itemset)``` function, if the itemset has already been in the dictionary, we return the value. If it hasn't, we calculate the support value, add them into the support dictionary, and then return the value.

2. Itemsets

* Generate Itemsets
    * Generate Candidate set Ck by iteration:   
    	* The datastructure we use for Lk is ```set()```. And Lk is initialized as a ```new set()```.
        * When generating candidate set C1, which contains one element in the each set.       
        * When generating candidate set Ck, k > 1, we compute it from Lk-1 according to the refinement described in [paper](http://www.cs.columbia.edu/~gravano/Qual/Papers/agrawal94.pdf). That is, we use two ```for``` loop, where we have two set ```q``` and ```p``` , which represent one itemset in Lk-1, to realize the join step. If the p and q only have one different item (i.e. the intersection of these two sets is only one item), we consider it as a new candidate and we add it into Ck+1.
    * Prune Step 
    	* For each candidate in Ck, we firstly transfer the candidate tuple into a set. And then, we use ```itertools.combinations(candidate, k-1)``` to get its all (k-1)-subsets. If one subset of this candidate are not in Lk-1, we delete this candidate from Ck.
    * Filter candidates by supp value and get the new Lk.
    * If we cannot generate new Lk, stop iteration.

* Store Itemsets  
  Tuples (i.e. itemsets) whose support is greater than or equal to min_supp are stored in a list. And we sort the list according to their support value in descending order.

3. Association Rules

	We have a list, called ```rules_list```, contains sublists. Each sublist is generated by one association rule whose confidence value is greater than or equal to min_Conf. In one sublist, the first element is a string of current rule in the format of ```[LHS] => [RHS]```, the second element is the confidence of this rule, and the third element is the support of the frequent itemset.

	The ```rules_list``` is sorted by the second element (i.e. Confidence value) of sublists in descending order.
	

Command Line Specification
---------
The parameter value we choose are min_Supp = 0.35,  min_Conf = 0.82
  ```
  python app.py INTEGRATED-DATASET.csv 0.35 0.82
  ```
And here is a small part of result we got.

  1. \[noise - street/sidewalk(loud music/party)] => \[noise - residential(loud music/party)] (Conf: 92.3019%, Supp: 37.4257%)
  2. \[noise - residential(loud talking)] => \[noise - residential(loud music/party)] (Conf: 92.1059%, Supp: 35.203%)
  3. \[noise - residential(banging/pounding)] => \[noise - residential(loud music/party)] (Conf: 89.8577%, Supp: 66.616%)
  4. \[heat/hot water(apartment only)] => \[noise - residential(loud music/party)] (Conf: 89.4235%, Supp: 54.5431%)
  5. \[derelict vehicle(with license plate)] => \[blocked driveway(no access)] (Conf: 89.0963%, Supp: 36.679%)
  6. \[illegal parking(posted parking sign violation)] => \[noise - residential(loud music/party)] (Conf: 85.711%, Supp: 48.5392%)
  7. \[sanitation condition(15 street cond/dump-out/drop-off)] => \[blocked driveway(no access)] (Conf: 82.1169%, Supp: 41.1244%)

Our result is close to real situation. For example, combining results with the actual situation, if people invite their friends to have a party at home, it's much likely that the music or their talking is loud. And host's friends who drive to the party may park their cars illegally. So when complaint about illegal parking or derelict vehicle happen, there are great possibilities that residents are having noisy parties in their house at the same community.

What surprises us is the rule '\[heat/hot water(apartment only)] => \[noise - residential(loud music/party)]' which has great confidence and support value. We guess that an apartment that often has heat/hot water problem may have poor facility condition, and this leads to the poor sound isolation of walls, which makes noise problem much more serious.
