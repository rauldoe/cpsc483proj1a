import math
import numpy
import pandas as pd

#Attempt on creating a general algorithm
##data = pd.read_csv("project_1.csv") #read CSV file
##
##len_of_columns = len(data.columns) # gets the numbers of columns in the csv
##print(len_of_columns)
##print(data.columns)
##
##
##a = data.iloc[:,-1].unique()[0].count(data.iloc[:,-1].unique()[0]) #tried to store the element types in a/b so for Total column, it'd be yes/no
##b = data.iloc[:,-1].unique()[1]
##print("a is: ", a)
##print("b is: ", b)


#For Initial E(S)
print("initial statement is 6 leave-alone and 4 force-into")
print ("For to get E(S), we use -P(x)logbase2P(X)")
print("E(S) is: -6/10 * logbase2(9/14) - 4/10 logbase2(4/10)")
E_S = (-.6 * math.log(6/10,2))- (4/10 * math.log(4/10,2))
print("E(S) = ", E_S)


#For IG(S,Job)
print("IG(S,Job) = E(S) - E(S,Job)")
print("= E(S) - P(Syes) * E(Syes) - P(Sno) * E(Sno)")
print("P(Syes) = 6/10")
P_Syes = 6/10
print("E(Syes) = -4/6 * logbase2(4/6) - 2/6 * logbase2(2/6)")
E_Syes = (-4/6 * math.log(4/6,2)) - (2/6 * math.log(2/6,2))
print("P(Sno) = 4/10")
P_Sno = 4/10
print("E(Sno) = -2/4 * logbase2(2/4) - 2/4 * logbase2(2/4)")
E_Sno = (-2/4 * math.log(2/4,2)) - (2/4 * math.log(2/4,2))
print("IG(S,Job) = ", E_S - P_Syes * E_Syes - P_Sno * E_Sno)
IG_S_Job = E_S - P_Syes * E_Syes - P_Sno * E_Sno


#For IG(S,Insurance)
print("IG(S,Insurance) = E(S) - E(S,Insurance)")
print("= E(S) - P(Syes) * E(Syes) - P(Sno) * E(Sno)")
print("P(Syes) = 2/10")
P_Syes = 2/10
print("E(Syes) = -2/2 * logbase2(2/2) - 0/2 *logbase(0/2)")
E_Syes = (-2/2 * math.log(2/2,2)) # - 0/2 * math.log(0/2,2)) <- rounds up to 0
print("P(Sno) = 8/10")
P_Sno = 8/10
print("E(Sno) = -4/8 * logbase2(4/8) - 4/8 * logbase2(4/8)")
E_Sno = (-4/8 * math.log(4/8,2)) - (4/8 * math.log(4/8,2))
print("IG(S,Insurance) = ", E_S - P_Syes * E_Syes - P_Sno * E_Sno)
IG_S_Insurance = E_S - P_Syes * E_Syes - P_Sno * E_Sno


#For IG(S,Votes)
print("IG(S,Votes) = E(S) - E(S,Votes)")
print("= E(S) - P(Syes) * E(Syes) - P(Sno) * E(Sno)")
print("P(Syes) = 6/10")
P_Syes = 6/10
print("E(Syes) = -6/6logbase2(6/6) - 0/6logbase2(0/6)")
#E_Syes = (-6/6 * math.log(6/6,2)) - (0/6 * math.log(0/6,2)) <- rounds up to 0
E_Syes = (-6/6 * math.log(6/6,2)) # 0 - 0
print("P(Sno) = 4/10")
P_Sno = 4/10
print("E(Sno) = 0/4logbase2(0/4) - 4/4logbase2(4/4)")
#E_Sno = (-0/4 * math.log(0/4,2)) - (4/4 * math.log(4/4,2))
E_Sno = 0 # log of 0 will return an error but since log(0) -> 0, we round it to 0
print("IG(S,Votes) = ", E_S - P_Syes * E_Syes - P_Sno * E_Sno)
IG_S_Votes = E_S - P_Syes * E_Syes - P_Sno * E_Sno







