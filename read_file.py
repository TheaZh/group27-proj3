import csv
"""
Read from file INTEGRATED-DATASET.csv
Generate backets
"""

def read(filename, num_line = 1000):
    baskets = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if reader.line_num == 1:
                continue
            baskets.append(row)
            if reader.line_num == num_line:
                break

    return baskets

if __name__ == '__main__':
    baskets = read("INTEGRATED-DATASET.csv", 200)
    print baskets
