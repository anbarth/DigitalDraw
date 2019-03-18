import csv



def cleanEmail(email):
    parts = email.split("@")
    return parts[0]

emailToPlan = {}

responses = open("ddraw-responses.csv")
reader = csv.reader(responses,delimiter=',')
next(reader) # skip the first row

for row in reader:
    email = cleanEmail(row[1])
    # a list of plans
    # each plan is of form (room type, pull list, lock pull list)
    plans = []

    # cycle through plans
    for i in range(0,4): # 4 plans max rn
        if row[4*i+2] == "": break
        room = row[4*i+2]

        pullsStr = row[4*i+3]
        pullsMessy = pullsStr.split(",")
        pulls = [cleanEmail(x) for x in pullsMessy]

        lockPullStr = row[4*i+4]
        lockPullsMessy = lockPullStr.split(",")
        lockPulls = [cleanEmail(x) for x in lockPullsMessy]

        plans += (room, pulls, lockPulls)
    
    emailToPlan[email] = plans


    

