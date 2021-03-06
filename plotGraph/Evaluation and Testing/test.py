#START OF TEST DATA PREPARATION
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import concurrent.futures


print(datetime.datetime.now())

#for test data
df = pd.read_csv('DE1_0_2008_to_2010_Inpatient_Claims_Sample_7.csv',dtype ='str')

df= df[:3000]
df.to_csv('out_test.csv', sep=',')


df_selected_cols = df[['DESYNPUF_ID', 'CLM_ADMSN_DT', 'ADMTNG_ICD9_DGNS_CD', 'ICD9_DGNS_CD_1']].copy()
ccn = pd.read_csv('/Users/aashara/Documents/Study/Research Credit/Seasonal_Trends/icd_ccs.csv',dtype ='str')#ccn data import

#Joining With ADMTNG_ICD9_DGNS_CD
joined_df = pd.merge(df_selected_cols, ccn, left_on='ADMTNG_ICD9_DGNS_CD', right_on='ICD9_Code')

#dropping unwanted columns:
columns = ['ICD9_Code', 'ICD_9_CM_CODE_DESCRIPTION', 'CCS_CATEGORY_DESCRIPTION','OPTIONAL_CCS_CATEGORY', 'OPTIONAL_CCS_CATEGORY_DESCRIPTION', 'ADMTNG_ICD9_DGNS_CD']
joined_df.drop(columns, inplace=True, axis=1)
joined_df = joined_df.rename(columns={'CCS_CATEGORY': 'ADMTNG_ICD9_DGNS_CD'})

 #Joining With ICD9_DGNS_CD_1
joined_df = pd.merge(joined_df, ccn, left_on='ICD9_DGNS_CD_1', right_on='ICD9_Code')

#dropping unwanted columns:out_train

columns = ['ICD9_Code', 'CCS_CATEGORY_DESCRIPTION', 'ICD_9_CM_CODE_DESCRIPTION', 'OPTIONAL_CCS_CATEGORY', 'OPTIONAL_CCS_CATEGORY_DESCRIPTION', 'ICD9_DGNS_CD_1']
joined_df.drop(columns, inplace=True, axis=1)
joined_df = joined_df.rename(columns={'CCS_CATEGORY': 'ICD9_DGNS_CD_1'})


joined_df['CLM_ADMSN_DT']=pd.to_datetime(joined_df['CLM_ADMSN_DT'], format="%Y%m%d") #parsing the date field CLM_ADMSN_DT.

joined_df['CLM_ADMSN_WEEK'] = pd.DatetimeIndex(joined_df['CLM_ADMSN_DT']).week #Extracting week only from CLM_ADMSN_DT and creating new column (CLM_ADMSN_WEEK from it

#Removing CLM_ADMSN_DT
joined_df.drop(['CLM_ADMSN_DT'], inplace=True, axis=1)


#selecting only admission diag codes and week:
df_symp_week = joined_df[['ADMTNG_ICD9_DGNS_CD', 'CLM_ADMSN_WEEK','ICD9_DGNS_CD_1']].copy()
df_symp_week['ADMTNG_ICD9_DGNS_CD'] =  'S_' + df_symp_week['ADMTNG_ICD9_DGNS_CD'].map(str)
df_symp_week['CLM_ADMSN_WEEK'] =  'W_' + df_symp_week['CLM_ADMSN_WEEK'].map(str)
df_symp_week['ICD9_DGNS_CD_1'] =  'D_' + df_symp_week['ICD9_DGNS_CD_1'].map(str)


# df_disease = joined_df[['ICD9_DGNS_CD_1']].copy()
# df_symp_week.to_csv('out_test.csv', sep=',')


df_symp_week['key_sym_week'] = list(zip(df_symp_week.ADMTNG_ICD9_DGNS_CD, df_symp_week.CLM_ADMSN_WEEK))#Converting list of columns to tuple to form new column

df_symp_week['value_dis_null'] = list(zip(df_symp_week.ICD9_DGNS_CD_1))#Converting list of columns to tuple to form new column

df_symp_week.drop(['ADMTNG_ICD9_DGNS_CD','CLM_ADMSN_WEEK','ICD9_DGNS_CD_1'], inplace=True, axis=1)

df_symp_week.to_csv('out_test_3cols.csv', sep=',')

test_data = []

for index, row in df_symp_week.iterrows():
    dict_test= {}
    dict_test[row['key_sym_week']] = row['value_dis_null']
    test_data.append(dict_test.copy())

print("test data preparation complete")

#END OF TEST DATA PREPARATION


"""
Description     : Simple Python implementation of the Apriori Algorithm
Usage:
    $python apriori.py -f DATASET.csv -s minSupport  -c minConfidence
    $python apriori.py -f DATASET.csv -s 0.15 -c 0.6
"""

import sys
import datetime
import pandas as pd

from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser

print(datetime.datetime.now())


def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    """calculates the support for items in the itemSet and returns a subset
   of the itemSet each of whose elements satisfies the minimum support"""
    _itemSet = set()
    localSet = defaultdict(int)
    testCount = 0
    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1

    for item, count in localSet.items():
        support = float(count) / len(transactionList)

        if support >= minSupport:
            _itemSet.add(item)
    return _itemSet


def joinSet(itemSet, length):
    """Join a set with itself and returns the n-element itemsets"""
    return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))  # Generate 1-itemSets
    return itemSet, transactionList


def runApriori(data_iter, minSupport, minConfidence):
    """
    run the apriori algorithm. data_iter is a record iterator
    Return both:
     - items (tuple, support)
     - rules ((pretuple, posttuple), confidence)
    """
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    assocRules = dict()
    # Dictionary which stores Association Rules
    oneCSet = returnItemsWithMinSupport(itemSet,
                                        transactionList,
                                        minSupport,
                                        freqSet)
    currentLSet = oneCSet
    k = 2
    while (currentLSet != set([])):
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                transactionList,
                                                minSupport,
                                                freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
        """local function which Returns the support of an item"""
        return float(freqSet[item]) / len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item))
                           for item in value])

    toRetRules = []
    for key, value in largeSet.items()[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item) / getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)),
                                           confidence))
    print("Yaha Pugyo")
    return toRetItems, toRetRules


def printResults(items, rules, filterData=None):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    # for item, support in sorted(items, key=lambda (item, support): support):
    # min(points, key=lambda p: (lambda x, y: (x * x + y * y))(*p))

    # print ("item: %s , %.3f" % (str(item), support))
    print ("\n------------------------ RULES:")
    for rule, confidence in sorted(rules, key=lambda (rule, confidence): confidence):
        pre, post = rule
        if (filterData == None):
            print ("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))

        elif filterData in post:
            print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))

def createDictionAssoc(items, rules, filterData=None):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    # for item, support in sorted(items, key=lambda (item, support): support):
    # min(points, key=lambda p: (lambda x, y: (x * x + y * y))(*p))

    # print ("item: %s , %.3f" % (str(item), support))
    print ("\n------------------------ RULES:")
    listOfRules = {}

    for rule, confidence in sorted(rules, key=lambda (rule, confidence): confidence):
        pre, post = rule
        if (len(pre) == 2 and "D_" in str(post) and len(post) == 1):
            print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))
            # print listOfRules[pre]
            dictConfidence = {}

            dictConfidence[post] = confidence
            if pre not in listOfRules:
                listOfRules[pre] = [[post, dictConfidence[post]]]
            else:
                listOfRules[pre].append([post, dictConfidence[post]])

        # print("Create Diction: ", listOfRules)
    return listOfRules


def evaluate(testdata, listOfRules):
    # testdata = [{('W_10', 'S_157'): ('D_2',)}, {('W_10', 'S_157'): 'D_12', }, {('W_10', 'S_156'): 'D_14', }]
    print("Test Data inside evaluate: ", testdata)
    print("List of Rules:", listOfRules)
    # listOfRules = {('W_10', 'S_157'): [[('D_127',), 0.8], [('D_2',), 0.2]]}
    df = pd.DataFrame(columns=["symweek", "actual", "predicted"])
    test_counter = 0

    while test_counter < len(testdata):

        for symptomweek in testdata[test_counter]:
            # print("evaluating: ", test_counter)
            # print(type(sympto  /mweek ))
            x = reversed(symptomweek)
            symptomweekReverse = tuple(x)#Reversed also taken in consideration as, rule [W_1, D_1] <=> [D_1, W_1]
            actual = testdata[test_counter][symptomweek]
            if (symptomweek not in listOfRules) and (symptomweekReverse in listOfRules):
                    symptomweek = symptomweekReverse


            if (symptomweek in listOfRules):
                # print("SymptomWeek inside evaluate: ", symptomweek)#('SymptomWeek inside evaluate: ', ('S_55', 'W_25'))
                for item in listOfRules[symptomweek]: #('Item', [('D_157',), 1.0])
                    # print("Item", item)
                    df = df.append({
                        "symweek": symptomweek,
                        "actual": actual,
                        "predicted": item[0]}, ignore_index=True)
            else:  # In case key is not in the predicted class
                df = df.append({
                    "symweek": symptomweek,
                    "actual": actual,
                    "predicted": 'Null'}, ignore_index=True)
            test_counter += 1

    actual = df['actual'].unique().tolist()
    df.to_csv('out_df_value.csv', sep=',')
    # predicted = df['predicted'].unique().tolist()
    truePositive = 0
    trueNegative = 0
    falsePositive = 0
    falseNegative = 0
    print ("reached here")
    for positive_class in actual:
        counter = 0
        while counter <= len(df.index) - 1:
            if (df['predicted'][counter] == positive_class):
                truePositive += 1
            elif (df['predicted'][counter] == df['actual'][counter]):
                trueNegative += 1
            elif (df['predicted'][counter] != df['actual'][counter] and positive_class == df['actual'][counter]):
                falsePositive += 1
            else:
                falseNegative += 1
            counter += 1
    print(truePositive, trueNegative, falsePositive, falseNegative)
    print(
    'Accuracy', float((truePositive + trueNegative)) / (truePositive + trueNegative + falsePositive + falseNegative))
    counter = 0
    correct = 0
    print(len(df.index))
    while counter <= len(df.index) - 1:
        if (df['predicted'][counter] == df['actual'][counter]):
            correct += 1
        counter += 1


def dataFromFile(fname):
    """Function which reads from the file and yields a generator"""
    file_iter = open(fname, 'rU')
    for line in file_iter:
        line = line.strip().rstrip(',')  # Remove trailing comma
        record = frozenset(line.split(','))
        yield record


if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing csv',
                         default='out_train.csv')
    optparser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support value',
                         default=0.00015,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence value',
                         default=0.00002,
                         type='float')
    optparser.add_option('-y', '--filter',
                         dest='filter',
                         help='Filter based on value',
                         default=None,
                         type='string')

    (options, args) = optparser.parse_args()

    inFile = None
    if options.input is None:
        inFile = sys.stdin
    elif options.input is not None:
        inFile = dataFromFile(options.input)
    else:
        print ('No dataset filename specified, system with exit\n')
        sys.exit('System will exit')
    minSupport = options.minS
    minConfidence = options.minC
    filterData = options.filter
    items, rules = runApriori(inFile, minSupport, minConfidence)
    # print("Items, Rules: ", items, "and", rules)
    print("Yeta Pugyo")
    list_of_rules = createDictionAssoc(items, rules,filterData)
    # print('Tala ko list of rules: ',list_of_rules)
    # evaluate(testdata, listOfRules):
    print("Aba yeta pugyo")
    evaluate(test_data, list_of_rules)
    # # if(filterData):
    # printResults(items, rules,filterData)
    # else:
    #     printResults(items, rules)
print(datetime.datetime.now())