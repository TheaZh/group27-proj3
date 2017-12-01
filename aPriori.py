from itertools import combinations

class aPriori(object):
    """docstring for aPriori."""

    def __init__(self, baskets, minsupp = 0.01, minconf = 0.5):
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
        # Lk.add(tuple())

        # generate every supportive tuple add to res
        res = []
        while True:
            if k != 0 and len(Lk) == 0:
                break
            k += 1
            Lkp1 = set()
            # print Lk

            # generate candidates Ckp1
            ''' # old method
            Ckp1 = set()
            for l in Lk:
                # ItemSet - l
                lset = set(l)
                ItemSet_l = ItemSet - lset

                for i in ItemSet_l:
                    Ckp1.add(tuple(sorted(l + (i,))))
            '''

            if k == 1:
                Ckp1 = self.generate_C1(ItemSet)
            else:
                Ckp1 = self.generate_from_Lk(Lk)
            # check every candidate's support
            for c in Ckp1:
                if self.supp(c) >= self.minsupp:
                    res.append(c)
                    Lkp1.add(c)
            Lk = Lkp1
        final_res = sorted(res, key= lambda x : (-self.supp(x), x))
        # print 'res:', final_res
        self.supportive_tuples = final_res

    def generate_C1(self, ItemSet):
        C1 = set()
        for item in ItemSet:
            C1.add((item,))
        return C1

    def generate_from_Lk(self, Lk):
        Ckp1 = set()
        for p in Lk:
            p_items = set(p)
            for q in Lk:
                q_items = set(q)
                intersention = p_items & q_items
                if len(intersention) == (len(p_items) - 1):
                    p_k = (p_items - intersention).pop()
                    q_k = (q_items - intersention).pop()
                    if p_k < q_k:
                        Ckp1.add(tuple(sorted(p + (q_k,))))
        return Ckp1

    def print_tuples(self, output_file):
        tmp_line = '==Frequent itemsets (min_sup = '+str(self.minsupp) + ')'
        self.write_output_file(output_file, tmp_line)
        print '==Frequent itemsets (min_sup =', str(self.minsupp) + ')'
        # print self.supportive_tuples
        for tup in self.supportive_tuples:
            tmp_itemset = ', '.join(tup)
            print "[{}], {}".format(tmp_itemset, "{0:g}%".format(self.supp(tup)*100))
            tmp_line = str("[{}], {}".format(tmp_itemset, "{0:g}%".format(self.supp(tup)*100)))
            self.write_output_file(output_file, tmp_line)
            # output_file.write(tmp_line)
            # print "--[{}], {}".format(tmp_itemset, "{0:.0f}%".format(self.supp(tup)*100))

    def print_rules(self, output_file):
        print '==High-confidence association rules (min_conf =', str(self.minconf) + ')'
        tmp_line = '\n==High-confidence association rules (min_conf = '+ str(self.minconf) + ')'
        self.write_output_file(output_file, tmp_line)
        res_rules = sorted(self.rules_list, key = lambda x : (-x[1], x[0]))
        # print res_rules
        for rule in res_rules:
            print "{} (Conf: {}, Supp: {})".format(rule[0],  "{0:g}%".format(rule[1]*100), "{0:g}%".format(rule[2]*100))
            tmp_line = str("{} (Conf: {}, Supp: {})".format(rule[0],  "{0:g}%".format(rule[1]*100), "{0:g}%".format(rule[2]*100)))
            self.write_output_file(output_file, tmp_line)
            # output_file.write(tmp_line)

    def write_output_file(self,output_file, str_line):
        output_file.write(str_line)
        output_file.write("\n")

    def filter_by_conf(self):
        """
        compute conf
        """
        ## rule_strs = []

        self.rules_list = []
        for tup in self.supportive_tuples:
            size = len(tup)

            if size > 1:
                # LHS size
                # only have one item on the right side
                LHSs_size = combinations(tup, size-1)
                for LHS in LHSs_size:
                    RHS = tuple(sorted(set(tup) - set(LHS)))
                    confidence = self.conf(LHS, tup)
                    supp = self.supp(tup)
                    if confidence >= self.minconf:
                        # print "{} => {} conf = {}".format(LHS, RHS, confidence)
                        LHS_str = ', '.join(LHS)
                        cur_rule = "[{}] => [{}]".format(LHS_str, RHS[0])
                        self.rules_list.append([cur_rule, confidence, supp])
        # print self.rules_list
        # print "[{}] => [{}] (Conf: {}, Supp: {})".format(LHS_str, RHS[0], confidence, supp)
        # self.print_rules();

def main():
    baskets = []
    baskets.append(["pen", "ink", "diary", "soap"])
    baskets.append(["pen", "ink", "diary"])
    baskets.append(["pen", "diary"])
    baskets.append(["pen", "ink", "soap"])
    output_test = open('output_test.txt', 'w')
    apriori = aPriori(baskets, 0.75, 0.8)
    apriori.print_tuples(output_test)
    apriori.print_rules(output_test)


if __name__ == '__main__':
    main()
