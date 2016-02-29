import csv
import re


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

main(0.05, 0.6)

# output = createC1(readCSV("5000-out1.csv"))
# print(output)
# print(test[0])
# print(test[1])
# print(test[2])
# print(test[3])

# for i in test:
#     print(i)

