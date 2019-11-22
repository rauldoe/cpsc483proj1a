
import pandas as pd
import numpy as np
import math
import os

def getValueCountLookup(dataFrame, attributeName):
    total = 0
    keyLookup = {}
    dependentList = dataFrame[attributeName].to_numpy()
    keyList, countList = np.unique(dependentList, return_counts=True)

    for i in range(0, len(keyList)):
        total += countList[i]
        keyLookup.update({keyList[i] : countList[i]})

    return {'lookup' : keyLookup, 'total' : total}

def getFeatureList(attributeList, decisionAttribute):
    return [i for i in attributeList if i != decisionAttribute]

def entropy(valueCountLookup):
    entropy = 0.0
    lookup = valueCountLookup['lookup']
    total = valueCountLookup['total']

    for key in lookup:
        px = lookup[key]/total
        entropy -= px * math.log(px, 2)
    return entropy

def join(arr, delim):
    joined = ''
    for i in range(0, len(arr)):
        joined = joined + str(arr[i]) + delim
    return joined

def toStringList(list):
    strList = []
    for i in list:
        strList.append(str(i))
    return strList

def unique(matrix):
    d = {}

    for i in range(0, len(matrix)):
        listKey = toStringList(matrix[i].tolist())
        key = join(listKey, '/')
        if (key in d.keys()):
            count = int(d[key]['count']) + 1
            d[key] = {'listkey' : listKey, 'count' : count}
        else:
            d.update({key : {'listkey' : listKey, 'count' : 1}})
    return d

def getLookupItem(lookup, attribute):
    list = []
    total = 0
    for i in lookup.keys():
        if (lookup[i]['listkey'][0] == attribute):
            list.append(lookup[i])
            total += int(lookup[i]['count'])
    return {'list' : list, 'total' : total}

def entropyWrt(lookupItem):
    entropy = 0.0

    total = int(lookupItem['total'])
    lookup = lookupItem['list']

    for i in lookup:
        # attribValue = i['listkey'][0]
        count = int(i['count'])
        
        p = count/total
        entropy -= p * math.log(p, 2)
    return entropy

def findMax(lookupList):
    maxItem = ('', 0.0)

    for i in lookupList.items():
        if (float(maxItem[1]) < float(i[1])):
            # print('setting max')
            # print(i)
            maxItem = i
    return maxItem

def computeInformationGain(df1, decisionAttribute, fList):
    igList = {}

    rowCount = df1.shape[0]

    k1 = getValueCountLookup(df1, decisionAttribute)
    totalEntropy = entropy(k1)
    # print(f'Total Entropy: {totalEntropy}')

    if (totalEntropy == 0.0):
        informationGain = 0.0
    else:
        for feature in fList:
            fm = df1[feature].to_numpy()
            featureOutcomes = toStringList(np.unique(fm, return_counts=False))
            # print(featureOutcomes)
            m = df1[[feature, decisionAttribute]].to_numpy()
            dict = unique(m)

            outcomeSummation = 0.0
            for outcome in featureOutcomes:
                li = getLookupItem(dict, outcome)
                pOutcome = int(li['total'])/rowCount
                e = entropyWrt(li)
                outcomeSummation -= pOutcome * e
                # print(e)

            informationGain = totalEntropy + outcomeSummation
            igList.update({ feature : informationGain})
            # print(feature + ': ' + str(informationGain))

    return igList

def processID3(df, fList, feature, outcomes):

    if len(fList) > 1:

        if (feature is None):
            subDf = df

            outcome = None
            igList = computeInformationGain(subDf, decisionAttribute, fList)
            if (len(igList.items()) > 0):
                maxItem = findMax(igList)
                maxItemFeature = maxItem[0]
                print(f'create node: {maxItemFeature} with parent: {feature} via outcome: {outcome}')
                maxItemOutcomes = toStringList(np.unique(subDf[maxItemFeature].to_numpy(), return_counts=False))
                fList.remove(maxItemFeature)
                # print(fList)

                processID3(subDf, fList, maxItemFeature, maxItemOutcomes)
        else:
            for outcome in outcomes:
                print(f"{feature} == '{outcome}'")
                subDf = df.query(f"{feature} == '{outcome}'")
            
                rowCountDf = df.shape[0]
                rowCountQuery = subDf.shape[0]
                print(rowCountDf)
                print(rowCountQuery)
                if (rowCountQuery == rowCountDf):
                    # this outcome will result in same decision
                    decision = subDf[decisionAttribute][0]
                    print(f'connect: {decision} with parent: {feature} via outcome: {outcome}')
                else:
                    igList = computeInformationGain(subDf, decisionAttribute, fList)
                    if (len(igList.items()) > 0):
                        maxItem = findMax(igList)
                        maxItemFeature = maxItem[0]
                        print(f'create node: {maxItemFeature} with parent: {feature} via outcome: {outcome}')
                        maxItemOutcomes = toStringList(np.unique(subDf[maxItemFeature].to_numpy(), return_counts=False))
                        fList.remove(maxItemFeature)
                        # print(fList)

                        processID3(subDf, fList, maxItemFeature, maxItemOutcomes)

os.chdir('C:/temp/cpsc483proj1')

decisionAttribute = 'play'
df = pd.read_csv('tennis.csv')
fList = getFeatureList(df.axes[1], decisionAttribute)

processID3(df, fList, None, None)


