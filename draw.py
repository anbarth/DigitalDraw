##############################################################
####################### ROOMS ################################
##############################################################

rooms = {
    # room type : [# people allowed, # rooms of this type]
    "r1" : [1, 3],
    "r2" : [2, 1],
    "r3" : [3, 1]
}


##############################################################
###################### READING ###############################
##############################################################

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


##############################################################
##################### ROOM DRAW! #############################
##############################################################

emailToRoom = {}

for myNum in range(len(emailToNum)):
    myEmail = numToEmail[myNum]

    if myEmail not in emailToPerson:
        print(myEmail+" failed to make any plans")
        continue
    
    me = emailToPerson[myEmail]

    for plan in me.plans:

        # don't bother if im already in a room
        if myEmail in emailToRoom: continue

        desiredRoom = plan[0]

        # no more rooms of this type
        if rooms[desiredRoom][1] <= 0:
            continue

        # case 1: pulling a single
        if rooms[desiredRoom][0] == 1:
            # pull myself into the room & mark it occupied
            emailToRoom[myEmail] = desiredRoom
            rooms[desiredRoom][1] = rooms[desiredRoom][1] - 1

            # now try to pull my friend into another room...
            # must be more rooms of this type
            if rooms[desiredRoom][1] > 0: 
                # must have someone to pull
                if len(plan[1]) > 0:

                    friendEmail = plan[1][0]
                    friend = emailToPerson[friendEmail]

                    # i must be allowed to pull this person
                    if myEmail in friend.pullBuddies:
                        # this person cant already have a room
                        if friendEmail not in emailToRoom:
                            # phew! that was a lot of nested ifs
                            # pull my friend into a room & mark it occupied
                            emailToRoom[friendEmail] = desiredRoom
                            rooms[desiredRoom][1] = rooms[desiredRoom][1] - 1
                
            # now try to lock pull iff my pull was successful OR this is a sontag 3-man
            # first, check that i did actually do a pull (or that i pulled a sontag 3-man)
                # ^ i think the easiest way to do that will be to just add a boolean lmao
            # then check that i want to lock-pull the correct # of people
            # then check that my lock-pullable room type is still available
            # then check that my lock pull wants to be pulled & hasnt found a room already
            # then pull!

        # case 2: pulling a double, triple, or quad
        else:
            isValid = True
            # not pulling right number of roomies
            if len(plan[1]) != rooms[desiredRoom][0]-1:
                print(myEmail+" made an invalid pull - not enough roommates")
                isValid = False
            # are my roomies also ok with this plan?
            for friendEmail in plan[1]:
                friend = emailToPerson[friendEmail]

                # am i allowed to pull this person?
                if myEmail not in friend.pullBuddies:
                    isValid = False

                # has this person already found a room?
                if friendEmail in emailToRoom:
                    isValid = False

            if isValid:
                # pull myself into the room
                emailToRoom[myEmail] = desiredRoom

                # pull all my friends
                for friendEmail in plan[1]:
                    emailToRoom[friendEmail] = desiredRoom

                # mark this room as occupied
                rooms[desiredRoom][1] = rooms[desiredRoom][1] - 1