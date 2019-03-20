import csv

# a person has only:
# a name, a list of room draw plans, and a list of people who can pull them
# because as RALs, that is all we care about
class Person:
    def __init__(self, email, plans, pullBuddies):
        self.email = email
        self.plans = plans
        self.pullBuddies = pullBuddies

def cleanEmail(email):
    parts = email.split("@")
    return parts[0].strip().lower()

emailToPerson = {}

responses = open("ddraw-responses.csv")
reader = csv.reader(responses,delimiter=',')
next(reader) # skip the first row

MAX_NUM_PLANS = 4

for row in reader:
    email = cleanEmail(row[1])

    pullBuds = []
    pullBudsStr = row[4*MAX_NUM_PLANS + 2]
    if pullBudsStr.lower().strip() != 'none':
            pullBudsMessy = pullBudsStr.split(",")
            pullBuds = [cleanEmail(x) for x in pullBudsMessy]

    # a list of plans
    # each plan is of form (room type, pull list, lock pull list)
    plans = []

    # cycle through plans
    for i in range(0,MAX_NUM_PLANS):
        if row[4*i+2] == "": break
        room = row[4*i+2]

        pulls = []
        pullsStr = row[4*i+3]
        if pullsStr.lower().strip() != 'none':
            pullsMessy = pullsStr.split(",")
            pulls = [cleanEmail(x) for x in pullsMessy]

        lockPulls = []
        lockPullStr = row[4*i+4]
        if lockPullStr.lower().strip != 'none':
            lockPullsMessy = lockPullStr.split(",")
            lockPulls = [cleanEmail(x) for x in lockPullsMessy]

        plans.append([room, pulls, lockPulls])
    
    emailToPerson[email] = Person(email, plans, pullBuds)


emailToNum = {
    "a" : 0,
    "b" : 1,
    "c" : 2,
    "d" : 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7
}


numToEmail = dict((reversed(item) for item in emailToNum.items()))
