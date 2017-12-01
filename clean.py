'''
Data cleaning to generate INTEGRATED-DATASET file
'''

import csv

file = open("INTEGRATED-DATASET.csv", "w")

# with open('311_2015_remove0.csv', 'rb') as csvfile:
with open('311_2015.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	prev_community_board = ""
	prev_created_date = ""
	for row in reader:
		if reader.line_num == 1:
			continue
		complaint_type = row[2].strip().replace(',', ' ').lower()
		descriptor = row[3].strip().replace(',', ' ').lower()
		if row[0] == prev_community_board and row[1] == prev_created_date:
			file.write(",")
			file.write(complaint_type)
			file.write("(")
			file.write(descriptor)
			file.write(")")
		else:
			if prev_community_board != "":
				file.write("\n")
			prev_community_board = row[0]
			prev_created_date = row[1]
			file.write(complaint_type)
			file.write("(")
			file.write(descriptor)
			file.write(")")

		# if reader.line_num == 100000:
			# break

file.close()
