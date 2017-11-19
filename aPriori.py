from itertools import combinations

class aPriori(object):
    """docstring for aPriori."""

    def __init__(self, baskets, minconf = 0.75, minsupp = 0.7):
        self.baskets = baskets
        self.minconf = minconf
        self.minsupp = minsupp
        self.supp_table = {}
        self.generate_tuples()
        self.filter_by_conf()

    def supp(self, c):
        if c in self.supp_table:
            return self.supp_table[c]

        cnt = 0
        for basket in self.baskets:
            # if items in c are all in basket
            allin = True
            for item in c:
                if item not in basket:
                    allin = False
                    break
            if allin:
                cnt += 1
        confidence = float(cnt) / len(self.baskets)
        self.supp_table[c] = confidence
        return confidence

    def conf(self, tup1, tup1Ntup2):
        return self.supp(tup1Ntup2) / self.supp(tup1)

    def generate_tuples(self):
        """
        generate every supportive tuples
        """
        ItemSet = set()
        for basket in self.baskets:
            for item in basket:
                ItemSet.add(item)

        k = 0
        Lk = set()
        Lk.add(tuple())

        # generate every supportive tuple add to res
        res = []
        while True:
            if len(Lk) == 0:
                break
            k += 1
            Lkp1 = set()

            # generate candidates Ckp1
            Ckp1 = set()
            for l in Lk:
                # ItemSet - l
                lset = set(l)
                ItemSet_l = ItemSet - lset

                for i in ItemSet_l:
                    Ckp1.add(tuple(sorted(l + (i,))))

            # check every candidate's support
            for c in Ckp1:
                print "c", c
                print "min",self.minsupp
                if self.supp(c) >= self.minsupp:
                    res.append(c)
                    Lkp1.add(c)
                    print res
                    print Lkp1
            Lk = Lkp1

        self.supportive_tuples = res

    def filter_by_conf(self):
        """
        compute conf
        """
        for tup in self.supportive_tuples:
            size = len(tup)

            if size > 1:
                for i in range(1, size):
                    # LHS of size i
                    LHSs_size_i = combinations(tup, i)
                    for LHS in LHSs_size_i:
                        RHS = tuple(sorted(set(tup) - set(LHS)))
                        confidence = self.conf(LHS, tup)
                        if confidence >= self.minconf:
                            print "{} => {}: conf = {}".format(LHS, RHS, confidence)



def main():
    baskets = []
    baskets.append(["pen", "ink", "diary", "soap"])
    baskets.append(["pen", "ink", "diary"])
    baskets.append(["pen", "diary"])
    baskets.append(["pen", "ink", "soap"])

    apriori = aPriori(baskets)


if __name__ == '__main__':
    main()
