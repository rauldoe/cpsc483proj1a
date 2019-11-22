import pandas as pd
import numpy as np
import math

def getValueCountLookup(dataFrame, attributeName):
    total = 0
    keyLookup = {}
    dependentList = dataFrame[attributeName].to_numpy()
    keyList, countList = np.unique(dependentList, return_counts=True)

    for i in range(0, len(keyList)):
        total += countList[i]
        keyLookup.update({keyList[i] : countList[i]})

    return {'lookup' : keyLookup, 'total' : total}

def getFeatureList(attributeList, dependentAttribute):
    return [i for i in attributeList if i != dependentAttribute]

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

dependentAttribute = 'ACTION'

df = pd.read_csv("project_1.csv") #read CSV file

rowCount = df.shape[0]
colCount = df.shape[1]
data = df.to_numpy()

attribList = df.axes[1]

fList = getFeatureList(attribList, dependentAttribute)

k1 = getValueCountLookup(df, dependentAttribute)
totalEntropy = entropy(k1)
print(totalEntropy)

for feature in fList:
    fm = df[feature].to_numpy()
    featureOutcomes = toStringList(np.unique(fm, return_counts=False))
    # print(featureOutcomes)
    m = df[[feature, dependentAttribute]].to_numpy()
    dict = unique(m)

    outcomeSummation = 0.0
    for outcome in featureOutcomes:
        li = getLookupItem(dict, outcome)
        pOutcome = int(li['total'])/rowCount
        e = entropyWrt(li)
        outcomeSummation -= pOutcome * e
        # print(e)

    informationGain = totalEntropy + outcomeSummation
    print(feature + ': ' + str(informationGain))

# print(data.columns)
# print(data)


# ##a = data.iloc[:,-1].unique()[0].count(data.iloc[:,-1].unique()[0]) #tried to store the element types in a/b so for Total column, it'd be yes/no
# ##b = data.iloc[:,-1].unique()[1]
# ##print("a is: ", a)
# ##print("b is: ", b)
# ##
# Entropy = [] #Created a list that will hold all our entropies

# last_column = data.iloc[:,-1] #gets us the last column values

# print(last_column.shape)

# counter = data.iloc[:,-1].value_counts() #get us the UNIQUE values count in the last column and saves it in an array, array = [unique1, unique2,...]
# print("counter is: ", counter) 

# total_count = 0
# for a in counter: #get us the number of times that unique value appears in the counter
#     print("a is: ", a)
#     total_count += a


# E_S = ((-counter[0] / total_count) * math.log(counter[0]/total_count,2)) - ((counter[1]/total_count) * math.log(counter[1]/total_count,2))
# print("E_S is :", E_S)
# Entropy.append(E_S) #adds our E(S) entropy into the Entropy list

# for b in data.columns: #A for loop that contains the 
#     print("b is: ", b) #get us the unique column name 
#     test = data[b].value_counts() #get us our test values for that unique column name
#     print("test is: ", test) 
    
