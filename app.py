from read_file import read
from aPriori import aPriori
import sys

def main(filename, min_supp, min_conf):
    baskets = read(filename, 30000) # read such number of lines
    apriori = aPriori(baskets, min_supp, min_conf)
    output_file = open('output.txt', 'w')
    apriori.print_tuples(output_file)
    apriori.print_rules(output_file)


if __name__ == '__main__':
    # run.sh INTEGRATED-DATASET.csv 0.01 0.5
    filename = "INTEGRATED-DATASET.csv"
    min_supp = 0.1
    min_conf = 0.5

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        min_supp = float(sys.argv[2])
        min_conf = float(sys.argv[3])

    main(filename, min_supp, min_conf)
