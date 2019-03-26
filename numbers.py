import csv
import random

# namesFileName is where all the people in this class year doing room draw are listed
# numbersFileName is where you want to put the numbers
# classYr is a string: "Sophomore", "Junior", or "Senior"
def assignNumbers(namesFileName, numbersFileName, classYr):

    namesFile = open(namesFileName)
    reader = csv.reader(namesFile)
    names = []
    for row in reader:
        names.append(row[0])
    namesFile.close()

    random.shuffle(names)

    numsFile = open(numbersFileName, 'w', newline='')
    writer = csv.writer(numsFile)

    for i in range(len(names)):
        writer.writerow([names[i],classYr+" "+str(i+1)])

    numsFile.close()

def sortHelper(val):
    return val[1]

# Tiers:
# 1: Good Medium Bad
# 2: Good Bad Medium
# 3: Medium Good Bad
# 4: Medium Bad Good
# 5: Bad Good Medium
# 6: Bad Medium Good
# namesFileName is the name of a file with *everyone* in the class year
# numbersFileName is where you want to put the names & tiers
def assignTiers(namesFileName, tiersFileName):

    namesFile = open(namesFileName)
    reader = csv.reader(namesFile)
    names = []
    for row in reader:
        names.append([row[0],0])
    namesFile.close()

    random.shuffle(names)

    for i in range(len(names)):
        names[i][1] = str((i % 6) +1)
    names.sort(key = sortHelper)

    tiersFile = open(tiersFileName,'w',newline='')
    writer = csv.writer(tiersFile)

    for name in names:
        writer.writerow([name[0], name[1]])


# namesAndTiersFileName is a list of all the people in this class year doing room draw, with their tier #s
# numbersFileName is where you want to put the numbers
# yearNum: 0 for rising sophomores, 1 for rising juniors, 2 for rising seniors
def assignTieredNumbers(namesFileName, numbersFileName, yearNum):
    namesFile = open(namesFileName)
    reader = csv.reader(namesFile)
    names = []
    for row in reader:
        names.append([row[0],int(row[1])])
    namesFile.close()

    goodNames = []
    medNames = []
    badNams = []
    classYr = ""

    if yearNum == 0:
        goodNames = [name[0] for name in names if name[1] == 1 or name[1] == 2]
        medNames = [name[0] for name in names if name[1] == 3 or name[1] == 4]
        badNames = [name[0] for name in names if name[1] == 5 or name[1] == 6]
        classYr = "Sophomore"

    if yearNum == 1:
        goodNames = [name[0] for name in names if name[1] == 3 or name[1] == 5]
        medNames = [name[0] for name in names if name[1] == 1 or name[1] == 6]
        badNames = [name[0] for name in names if name[1] == 2 or name[1] == 4]
        classYr = "Junior"

    if yearNum == 2:
        goodNames = [name[0] for name in names if name[1] == 4 or name[1] == 6]
        medNames = [name[0] for name in names if name[1] == 2 or name[1] == 5]
        badNames = [name[0] for name in names if name[1] == 1 or name[1] == 3]
        classYr = "Senior"

    random.shuffle(goodNames)
    random.shuffle(medNames)
    random.shuffle(badNames)

    orderedNames = []
    orderedNames.extend(goodNames)
    orderedNames.extend(medNames)
    orderedNames.extend(badNames)
    # if there are people who took a leave of absence or super seniors,
    # you should randomly insert them into orderedNames here
    # probably assign those people tier 7 or something to mark them

    numsFile = open(numbersFileName, 'w', newline='')
    writer = csv.writer(numsFile)

    for i in range(len(orderedNames)):
        writer.writerow([orderedNames[i],classYr+" "+str(i+1)])

    numsFile.close()



#assignNumbers("ral-names.csv","ral-numbers.csv","RAL")
#assignTiers("ral-names.csv","ral-tiers.csv")
#assignTieredNumbers("ral-tiers.csv","ral-numbers.csv",0)

#assignNumbers("senior-names.csv","senior-numbers.csv")
#assignNumbers("junior-names.csv","junior-numbers.csv")
#assignTiers("sophomore-names.csv","sophomore-tiers.csv")
#assignTieredNumbers("sophomore-tiers.csv","sophomore-numbers.csv",0)
