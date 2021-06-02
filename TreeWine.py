import time
t1 = time.time()
Nodes = [] 

tree = []
def getData(file_path):
    """a function to get data from file and transform into float"""
    file = open(file_path,"r")
    file = [row.replace('\n','') for row in file]
    dataSet = [row.split(",") for row in file]
    labels = dataSet.pop(0)
    for item in dataSet:
        for index, col in enumerate(item):
            item[index] = float(col)
    return labels, dataSet

# set a class to store the information of split point (node)
class Node:
    def __init__(self, value = None, label = None, parent = None, index = 0):
        self.value = value
        self.label = label
        self.parent = parent
        self.index = index

    def getSize(self):
        return self.index

    def getInfo(self):
        print(self.value, self.label, self.parent, self.index)

def getGini(value, dataSet):
    numbers = []
    for i in dataSet:
        pro = dataSet.count(value)/len(dataSet)
        numbers.append(pro * pro)
    gini = 1 - sum(numbers)
    return gini

def getSplitValue(kindSet):
    """ get the spilt point"""
    gini = 99999
    kindNumber = set(kindSet)
    value = 0
    for i in kindNumber:
        giniIndex = getGini(i, kindSet)
        if giniIndex < gini:
            gini = giniIndex
            value = i
    # value = sum(kindSet)/len(kindSet)
    return value

def getSplitPoint(kindSet, label, index):
    """base the value to judge the split point"""
    global Nodes
    judgePoint = getSplitValue(kindSet)
    if index == 0:
        Nodes.append(Node(judgePoint, label, None, index))
    else:
        Nodes.append(Node(judgePoint, label, Nodes[index - 1], index))

def builuTree(dataSet, labels):
    length = len(labels)
    for index, label in enumerate(labels):
        kindSet = [dataSet[i][index] for i in range(len(dataSet))]
        getSplitPoint(kindSet, label, index)

    for data in dataSet:
        cell = []
        for i in range(len(labels)):
            if float(data[i]) <= Nodes[i].value:
                cell.append("left")
            else:
                cell.append("right")
        tree.append(cell)
    return tree

def prePrediction(Nodes, testSet, labels):
    test = []
    for testElement in testSet:
        cell = []
        for i in range(len(labels)):
            if float(testElement[i]) <= Nodes[i].value:
                cell.append("left")
            else:
                cell.append("right")
        test.append(cell)
    return test

def exchange(trainSet):
    trainSet_copy = trainSet[:]
    number = 0
    for index, i in enumerate(trainSet):
        i[number] = trainSet_copy[index][number + 1]
    for index, i in enumerate(trainSet):
        i[number + 1] = trainSet_copy[index][number]
    return trainSet




def predict(train, trainSet, test):
    result = []
    for item in test:
        if item in train:
            result.append(True)
    return len(result)/len(test)


def run():
    labels, trainSet = getData('/Applications/CSCassignment/TeamProject/test.csv')
    labels, testSet = getData('/Applications/CSCassignment/TeamProject/train.csv')
    trainSet = exchange(trainSet)
    trainTree = builuTree(trainSet, labels)
    test = prePrediction(Nodes, testSet, labels)
    # for i in range(len(trainSet)):
    #     print(trainTree[i], test[i])
    print(predict(trainTree, trainSet, test))

    t2 = time.time()
    print(t2-t1)

run()