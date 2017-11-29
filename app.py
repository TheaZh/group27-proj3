from read_file import read
from aPriori import aPriori
import sys

def main(filename, min_supp, min_conf):
    baskets = read(filename, 30000) # read such number of lines
    apriori = aPriori(baskets, min_supp, min_conf)
    association_header = "==Frequent itemsets (min_sup={}%)".format(str(int(round(min_supp*100))))
    associations = apriori.get_tuples_string()
    print association_header
    print associations
    rule_header = "==High-confidence association rules (min_conf={}%)".format(str(int(round(min_conf*100))))
    rules = apriori.filter_by_conf()
    print rule_header
    print rules

    # write to "example-run.txt"
    with open("example-run.txt", "w") as file:
        file.write(association_header)
        file.write("\n")
        for association in associations:
            file.write(association)
            file.write("\n")
        file.write(rule_header)
        file.write("\n")
        for rule in rules:
            file.write(rule)
            file.write("\n")


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
