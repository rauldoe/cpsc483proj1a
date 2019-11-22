
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

def displayPath(parentFeature, linkOutcome, childFeature):

    if (linkOutcome is None):
        displayParentFeature = 'root' if (parentFeature is None) else parentFeature
        print(f'{displayParentFeature} --> {childFeature}')
    else:
        displayParentFeature = 'root' if (parentFeature is None) else parentFeature
        print(f'{displayParentFeature} -- {linkOutcome} --> {childFeature}')

def isDecisionable(df, decisionAttribute, feature, outcomes):
    status = [False, '']

    uniqueCount = df[decisionAttribute].nunique()
    if (uniqueCount == 1):
        # this outcome will result in same decision
        decision = df[decisionAttribute].iloc[0]
        status = [True, [{'' : decision}]]
    else:
        isDecisionableOutcomes = True
        decisionList = []
        for outcome in outcomes:
            subDf = df.query(f"{feature} == '{outcome}'")
            subUniqueCount = subDf[decisionAttribute].nunique()
            if (subUniqueCount > 1):
                isDecisionableOutcomes = False
                break
            else:
                decision = subDf[decisionAttribute].iloc[0]
                decisionList.append({'outcome' : outcome, 'decision' : decision})
        if (isDecisionableOutcomes):
            status = [True, decisionList]
    
    return status

def processID3(df, fList, decisionAttribute, feature, outcomes):

    if len(fList) > 1:

        if (feature is None):
            subDf = df

            outcome = None
            igList = computeInformationGain(subDf, decisionAttribute, fList)
            if (len(igList.items()) > 0):
                maxItem = findMax(igList)
                maxItemFeature = maxItem[0]
                # displayFeature = 'root' if (feature is None) else feature
                # print(f'{displayFeature} --> {maxItemFeature}')
                displayPath(feature, None, maxItemFeature)
                maxItemOutcomes = toStringList(np.unique(subDf[maxItemFeature].to_numpy(), return_counts=False))
                fList.remove(maxItemFeature)
                # print(fList)

                processID3(subDf, fList, decisionAttribute, maxItemFeature, maxItemOutcomes)
        else:
            for outcome in outcomes:
                # print(f"{feature} == '{outcome}'")
                subDf = df.query(f"{feature} == '{outcome}'")
            
                isDecision = isDecisionable(subDf, decisionAttribute)
                if (isDecision[0]):
                    # this outcome will result in same decision
                    decision = isDecision[1]
                    # print(f'{feature} -- {outcome} --> {decision}')
                    displayPath(feature, outcome, decision)
                else:
                    igList = computeInformationGain(subDf, decisionAttribute, fList)
                    if (len(igList.items()) > 0):
                        maxItem = findMax(igList)
                        maxItemFeature = maxItem[0]
                        # displayFeature = 'root' if (feature is None) else feature
                        # print(f'{displayFeature} -- {outcome} --> {maxItemFeature}')
                        displayPath(feature, outcome, maxItemFeature)
                        maxItemOutcomes = toStringList(np.unique(subDf[maxItemFeature].to_numpy(), return_counts=False))
                        fList.remove(maxItemFeature)
                    
                        isDecision = isDecisionable(subDf, decisionAttribute)
                        if (isDecision[0]):
                            decision = isDecision[1]
                            fList = []
                            displayPath(maxItemFeature, None, decision)
                        else:
                            processID3(subDf, fList, decisionAttribute, maxItemFeature, maxItemOutcomes)
                # if (uniqueCount == 1):
        # if (feature is None):
    else:
        if (len(fList) == 1):
            lastFeature = fList[0]
            # print(f'{feature} --> {lastFeature}')
            displayPath(feature, None, lastFeature)

            lastOutcomes = toStringList(np.unique(df[lastFeature].to_numpy(), return_counts=False))
            for outcome in lastOutcomes:
                # print(f'{lastFeature} --> {outcome}')
                displayPath(lastFeature, None, outcome)
    # if len(fList) > 1:

os.chdir('C:/temp/cpsc483proj1a')

decisionAttribute = 'play'
df = pd.read_csv('tennis.csv')
fList = getFeatureList(df.axes[1], decisionAttribute)

processID3(df, fList, decisionAttribute, None, None)


