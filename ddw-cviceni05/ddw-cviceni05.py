from collections import Counter

from pprint import pprint


def frequentItems(transactions, support):
    counter = Counter()
    for trans in transactions:
        counter.update(frozenset([t]) for t in trans)
    return set(item for item in counter if counter[item] / len(transactions) >= support), counter


def generateCandidates(L, k):
    candidates = set()
    for a in L:
        for b in L:
            union = a | b
            if len(union) == k and a != b:
                candidates.add(union)
    return candidates


def filterCandidates(transactions, itemsets, support):
    counter = Counter()
    for trans in transactions:
        subsets = [itemset for itemset in itemsets if itemset.issubset(trans)]
        counter.update(subsets)
    return set(item for item in counter if counter[item] / len(transactions) >= support), counter


def apriori(transactions, support):
    result = list()
    resultc = Counter()
    candidates, counter = frequentItems(transactions, support)
    result += candidates
    resultc += counter
    k = 2
    while candidates:
        candidates = generateCandidates(candidates, k)
        candidates, counter = filterCandidates(transactions, candidates, support)
        result += candidates
        resultc += counter
        k += 1
    resultc = {item: (resultc[item] / len(transactions)) for item in resultc}
    return result, resultc


def createRule(item):
    result = []
    for word in item:
        left = list(item)
        left.remove(word)
        right = list()
        right.append(word)
        result.append((left, right))
    return result


def genereateRules(frequentItemsets, supports, minLevel):
    rules = []
    for item in frequentItemsets:
        if len(item) < 2:
            continue
        res = createRule(item)
        for left, right in res:
            support = supports[frozenset(item)]
            confidence = support / supports[frozenset(left)]
            lift = support / ((supports[frozenset(left)] * supports[frozenset(right)]))
            if confidence != 1:
                conviction = (1 / supports[frozenset(right)]) / (1 - confidence)
            else:
                conviction = float("inf")
            if confidence >= minLevel:
                rules.append((left, right, confidence, support, lift, conviction))
                # rules.append((left, right, confidence, support))
    return rules


# dataset = [
#     ['bread', 'milk'],
#     ['bread', 'diaper', 'beer', 'egg'],
#     ['milk', 'diaper', 'beer', 'cola'],
#     ['bread', 'milk', 'diaper', 'beer'],
#     ['bread', 'milk', 'diaper', 'cola'],
# ]

import pandas as pd

# df = pd.read_csv("./bank-data.csv")
df = pd.read_csv("./zoo.csv")
# del df["id"]
# df["income"] = pd.cut(df["income"], 10)
dataset = []
for index, row in df.iterrows():
    row = [col + "=" + str(row[col]) for col in list(df)]
    dataset.append(row)

frequentItemsets, supports = apriori(dataset, 0.5)
res = genereateRules(frequentItemsets, supports, 0.95)
# for rule in sorted(res, key=lambda item: len(item[0]), reverse=True)[:100]:
for rule in sorted(res, key=lambda item: item[2], reverse=False)[:100]:
    print("{{{}}} -> {{{}}}, conf={}, supp={}, lift={}, conv={}".format(rule[0], rule[1], rule[2], rule[3], rule[4],
                                                                        rule[5]))
    # print("{{{}}} -> {{{}}}, conf={}, supp={}".format(rule[0], rule[1], rule[2], rule[3]))
