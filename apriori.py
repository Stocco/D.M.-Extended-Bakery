import csv
import re
from numpy import *
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler


def map_bin(num):
    bin_map = {
        #  Cakes (0)
        0: 'cake',  # Chocolate
        1: 'cake',  # Lemon
        2: 'cake',  # ...
        3: 'cake',
        4: 'cake',
        5: 'cake',
        9: 'cake',  # Napoleon
        #  Eclairs (1)
        6: 'eclair',
        7: 'eclair',
        8: 'eclair',
        #  Tart (2)
        10: 'tart',
        12: 'tart',
        13: 'tart',
        14: 'tart',
        15: 'tart',
        16: 'tart',
        17: 'tart',
        18: 'tart',
        19: 'tart',
        20: 'tart',
        #  Pie (3)
        11: 'pie',
        # Cookies (4)
        21: 'cookie',
        22: 'cookie',
        23: 'cookie',
        24: 'cookie',
        27: 'cookie',
        28: 'cookie',
        29: 'cookie',
        # Meringue (5)
        25: 'meringue',
        26: 'meringue',
        # Croissant (6)
        30: 'croissant',
        31: 'croissant',
        32: 'croissant',
        33: 'croissant',
        34: 'croissant',
        # Danish (7)
        35: 'danish',
        36: 'danish',
        39: 'danish',
        # Twist (8)
        37: 'twist',
        # Bear Claw (9)
        38: 'bear claw',
        # Lemonade (10)
        40: 'lemonade',
        41: 'lemonade',
        # Juice (11)
        42: 'juice',
        # Tea (12)
        43: 'tea',
        # Water (13)
        44: 'bottled water',
        # Coffee (14)
        45: 'coffee',
        46: 'coffee',
        # Frappuccino (15)
        47: 'frap',
        # Soda (16)
        48: 'soda',
        # Espresso (17)
        49: 'espresso'
    }
    return str(bin_map[num])


def map_num(num):
    bin_map = {
    # Cakes (0)
    0: '0', # Chocolate
    1: '0', # Lemon
    2: '0', # ...
    3: '0',
    4: '0',
    5: '0',
    9: '0', # Napoleon
    # Eclairs (1)
    6: '1',
    7: '1',
    8: '1',
    # Tart (2)
    10: '2',
    12: '2',
    13: '2',
    14: '2',
    15: '2',
    16: '2',
    17: '2',
    18: '2',
    19: '2',
    20: '2',
    # Pie (3)
    11: '3',
    # Cookies (4)
    21: '4',
    22: '4',
    23: '4',
    24: '4',
    27: '4',
    28: '4',
    29: '4',
    # Meringue (5)
    25: '5',
    26: '5',
    # Croissant (6)
    30: '6',
    31: '6',
    32: '6',
    33: '6',
    34: '6',
    # Danish (7)
    35: '7',
    36: '7',
    39: '7',
    # Twist (8)
    37: '8',
    # Bear Claw (9)
    38: '9',
    # Lemonade (10)
    40: '10',
    41: '10',
    # Juice (11)
    42: '11',
    # Tea (12)
    43: '12',
    # Water (13)
    44: '13',
    # Coffee (14)
    45: '14',
    46: '14',
    # Frappuccino (15)
    47: '15',
    # Soda (16)
    48: '16',
    # Espresso (17)
    49: '17'
    }
    return str(bin_map[int(num)])

def createC1(data):
  c1=[]
  for transaction in data:
     for item_num,item in enumerate(transaction):
       if(item_num != 0):
         # item = map_bin(int(item))
         if not [item] in c1:
           c1.append([item])
  c1.sort()
  return list(map(frozenset,c1))

def scanD(D,ck,minsuport):
  ssCnt = {}
  for tid in D:
    for can in ck:
     if can.issubset(tid):
       if not can in ssCnt: ssCnt[can]=1
       else: ssCnt[can] += 1
  numItems = float(len(D))
  retList = []
  suportData = {}
  for key in ssCnt:
    suport = ssCnt[key]/numItems
    if suport >= minsuport:
      retList.insert(0,key)
    suportData[key] = suport
  return retList, suportData

def aprioriGen(Lk,k):
  retList = []
  lenLk = len(Lk)
  for i in range(lenLk):
    for j in range(i+1, lenLk):
      L1 = list(Lk[i]) [:k-2]; L2 = list(Lk[j])[:k-2]
      L1.sort(); L2.sort()
      if L1==L2:
        retList.append(Lk[i] | Lk[j])
  return retList


#Apriori Function and its helpers
def apriori(dataSet, minSuport = 0.5):
  C1 = createC1(dataSet)
  D = list(map(set, dataSet))
  L1, suportData = scanD(D,C1,minSuport)
  L = [L1]
  k=2
  while(len(L[k-2]) > 0):
    Ck = aprioriGen(L[k-2],k)
    Lk, supK = scanD(D,Ck,minSuport)
    suportData.update(supK)
    L.append(Lk)
    k += 1
  return L,suportData

def readCSV2(url):
    with open(url) as file:
        content = file.readlines()
        data = []
        for line in content:
            line = re.sub('[\s+]', '', line)
            line = line.split(',')
            line = line[1:]
            data.append(list(list(line)))
    return bin(data)

def bin(data):
    for i, transaction in enumerate(data):
        for j, item in enumerate(transaction):
            data[i][j] = map_bin(int(item))
    return data

def generateRules(L,supportData, minConf=0.7):
  bigRulelist=[]
  for i in range(1,len(L)):
    for freqSet in L[i]:
      H1= [frozenset([item]) for item in freqSet]
      if(i > 1):
        rulesFromConseq(freqSet,H1,supportData,bigRulelist,minConf)
      else:
        calcConf(freqSet,H1,supportData,bigRulelist,minConf)
  return bigRulelist

def calcConf(freqSet, H, supportData, brl, minConf=0.7):
  prunedH = []
  for conseq in H:
    conf = supportData[freqSet]/supportData[freqSet-conseq]
    if conf >= minConf:
      print(freqSet-conseq,"-->",conseq," conf: ", conf)
      brl.append((freqSet-conseq, conseq, conf))
      prunedH.append(conseq)
  return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
  m = len(H[0])
  if (len(freqSet) > (m + 1)):
    Hmp1 = aprioriGen(H, m + 1)
    Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
    if (len(Hmp1) > 1):
      rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)

#Clustering Function
def loadDataSet(fileName):
 dataMat = []
 fr = open(fileName)
 for line in fr.readlines():
   curLine = line.strip().split(',')
   del curLine[0]
   fltLine = curLine
   dataMat.append(fltLine)
 return dataMat

def distEclud(vecA, vecB): return sqrt(sum(power(vecA - vecB, 2)))

def randCent(dataSet, k):
 n = shape(dataSet)[1]
 centroids = mat(zeros((k,n)))
 for j in range(n):
   minJ = min(dataSet[:,j])
   rangeJ = float(max(dataSet[:,j]) - minJ)
   centroids[:,j] = minJ + rangeJ * random.rand(k,1)
 return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
 m = shape(dataSet)[0]
 clusterAssment = mat(zeros((m,2)))
 centroids = createCent(dataSet, k)
 clusterChanged = True
 while clusterChanged:
   clusterChanged = False
   for i in range(m):
    minDist = inf; minIndex = -1
    for j in range(k):
      distJI = distMeas(centroids[j,:],dataSet[i,:])
      if distJI < minDist:
        minDist = distJI; minIndex = j
    if clusterAssment[i,0] != minIndex: clusterChanged = True
    clusterAssment[i,:] = minIndex,minDist**2
   print(centroids)
   for cent in range(k):
    ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
    centroids[cent,:] = mean(ptsInClust, axis=0)
 return centroids, clusterAssment




#action functions

def main(support, confidence):
  print('5000 receipts')
  test, sup = apriori(list(readCSV2("5000-out1.csv")), support)
  generateRules(test, sup, confidence)

  print("   ")

  print('20000 receipts')
  test, sup = apriori(list(readCSV2("20000-out1.csv")), support)
  generateRules(test, sup, confidence)

  print("   ")

  print('75000 receipts')
  test, sup = apriori(list(readCSV2("75000-out1.csv")), support)
  generateRules(test, sup, confidence)

def booleanMap(value):
    map ={
        "0":"?",
        "1":"t"
    }
    return map[value]


def filter(filename):
    newFile=[]
    fr = open(filename)
    for line in fr.readlines():
         curLine = line.strip().split(',')
         del curLine[0]
         curLine = [booleanMap(i) for i in curLine]
         newFile.append(curLine)

    output = open("output.arff", "w")
    for line in newFile:
        for i,value in enumerate(line):
            if(i == len(line)-1):output.write(value)
            else: output.write(value+",")
        output.write("\n")
    output.close()


def vectorize(filename):
    newFile=[]
    vectorized=[]
    fr = open(filename)


    for line in fr.readlines():
        line = re.sub('[\s+]','',line)
        line = line.split(',')
        del line[0]
        line = [map_num(i) for i in line]
        newFile.append(line)

    for tid in newFile:
        curVec=[]
        for build in range(18):
            if(tid.count(str(build))): curVec.append("t")
            else: curVec.append("?")
        vectorized.append(curVec)


    output = open("output2.arff", "w")
    for line in vectorized:
        for i,value in enumerate(line):
            if(i == len(line)-1):output.write(value)
            else: output.write(value+",")
        output.write("\n")
    output.close()
    return vectorized

def transposer(matrix):
    transpose_mat = []
    for col in range(len(matrix[0])):
        transposed_row = []
        for row in range(len(matrix)):

            if(matrix[row][col] == 't'):
                transposed_row.append('t')
            else:
                transposed_row.append('?')

        transpose_mat.append(transposed_row)

    output = open("transposed_output.arff", "w")
    for line in transpose_mat:
        for i,value in enumerate(line):
            if(i == len(line)-1):output.write(value)
            else: output.write(value+",")
        output.write("\n")
    output.close()
    return transpose_mat

matrix = vectorize("5000-out1.csv")
transposed_matrix = transposer(matrix)
print(transposed_matrix)





# emptymatrix=[]
# for i in range(18):
#     row=[]
#     for j in range(75000):
#         row.append("?")
#     emptymatrix.append(row)
#
#
# for line in emptymatrix:
#     print(line)