##############################################################
####################### ROOMS ################################
##############################################################

rooms = {
    # room type : [# people allowed, # rooms of this type]
    "Atwood single" : [1, 48, 0],
    "Atwood suite double" : [2, 12, 0], 
    "Atwood triple" : [3, 12, 0], 
    "Atwood column double" : [2, 4, 0], 
    "Atwood efficiency" : [2, 6, 0],
    "Case single" : [1, 32, 1],
    "Case double" : [2, 32, 1],
    "Case triple" : [3, 1, 1],
    "Case quad" : [4, 4, 1],
    "Drinkward single in a suite with 3 singles, 1 triple" : [1, 24, 2],
    "Drinkward triple in a suite with 3 singles, 1 triple" : [3, 8, 2],
    "Drinkward single in a suite with 2 singles, 1 triple" : [1, 4, 2],
    "Drinkward triple in a suite with 2 singles, 1 triple" : [3, 2, 2],
    "Drinkward O-side single" : [1, 37, 2],
    "Drinkward O-side triple" : [3, 25, 2],
    "East single" : [1, 16, 3],
    "East double" : [2, 36, 3],
    "Linde single in a suite with 2 singles, 2 doubles" : [1, 12, 4],
    "Linde double in a suite with 2 singles, 2 doubles" : [2, 12, 4],
    "Linde single in a suite with 4 singles, 1 double" : [1, 8, 4],
    "Linde double in a suite with 4 singles, 1 double" : [2, 2, 4],
    "Linde double in a suite with 3 doubles" : [2, 12, 4],
    "Linde double in a suite with 2 doubles" : [2, 2, 4],
    "North single" : [1, 16, 5],
    "North double" : [2, 36, 5],
    "Sontag single in a suite with 3 singles, 1 double" : [1, 36, 6], 
    "Sontag double in a suite with 3 singles, 1 double" : [2, 12, 6],
    "Sontag single in a suite with 2 singles, 1 double" : [1, 6, 6],
    "Sontag double in a suite with 2 singles, 1 double" : [2, 3, 6],
    "Sontag single in a suite with 1 single, 1 double" : [1, 2, 6],
    "Sontag double in a suite with 1 single, 1 double" : [2, 2, 6],
    "South single in a suite with 4 singles" : [1, 32, 7], 
    "South single in a suite with 3 singles" : [1, 24, 7],
    "South single in a suite with 2 singles" : [1, 8, 7],
    "South double" : [2, 4, 7],
    "West single" : [1, 16, 8],
    "West double" : [2, 36, 8]
}

# list of lock-pullable situations
# [room you pull, room you get to lock-pull]
lockPullable = {"Sontag single in a suite with 3 singles, 1 double": "Sontag single in a suite with 3 singles, 1 double",
                "Sontag single in a suite with 2 singles, 1 double": "Sontag double in a suite with 2 singles, 1 double",
                "Sontag single in a suite with 1 single, 1 double": "Sontag double in a suite with 1 single, 1 double",
                "South single in a suite with 3 singles": "South single in a suite with 3 singles",
                "Linde single in a suite with 2 singles, 2 doubles": "Linde double in a suite with 2 singles, 2 doubles",
                "Drinkward single in a suite with 2 singles, 1 triple": "Drinkward triple in a suite with 2 singles, 1 triple"}

##############################################################
###################### READING ###############################
##############################################################

import csv

# a person has only a list of plans & a list of people who can pull them
# because as RALs, that is all we care about
class Person:
    def __init__(self, plans, pullBuddies):
        #self.email = email
        self.plans = plans
        self.pullBuddies = pullBuddies


def cleanEmail(email):
    parts = email.split("@")
    return parts[0].strip().lower()

emailToPerson = {}

responses = open("ddraw-responses.csv")
reader = csv.reader(responses,delimiter=',')
next(reader) # skip the first row

MAX_NUM_PLANS = 20

####### read in the plans #########

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
    
    emailToPerson[email] = Person(plans, pullBuds)

####### read in the indorm stati ######

responses = open("indorms.csv")
inDormReader = csv.reader(responses,delimiter=',')

emailToIndorm = {}

# everyone gets no in-dorm by default
for email in emailToPerson:
    emailToIndorm[email] = -1

# but now maybe some people get it
for row in inDormReader:
    myEmail = cleanEmail(row[0])
    indorm = -1
    if row[1] == "AT": indorm = 0
    if row[1] == "CA": indorm = 1
    if row[1] == "DW": indorm = 2
    if row[1] == "EA": indorm = 3
    if row[1] == "LI": indorm = 4
    if row[1] == "NO": indorm = 5
    if row[1] == "SG": indorm = 6
    if row[1] == "SO": indorm = 7
    if row[1] == "WE": indorm = 8
    emailToIndorm[myEmail] = indorm


####### read in the numbers #########

# all-nums should have ALL room draw participants, listed by hmc email
# listed in order from senior 1 to sophomore worst
# numbers shalt start at 0
emailToNum = {}
allNums = open("all-nums.csv")
numsReader = csv.reader(allNums,delimiter=',')
thisNum = 0
for row in numsReader:
    thisEmail = cleanEmail(row[0])
    emailToNum[thisEmail] = thisNum
    thisNum += 1

'''emailToNum = {
    "a" : 0,
    "b" : 1,
    "c" : 2,
    "d" : 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7
}'''


numToEmail = dict((reversed(item) for item in emailToNum.items()))


##############################################################
##################### ROOM DRAW! #############################
##############################################################

emailToRoom = {}

# what in-dorm round am i on?
# 0 = atwood, 1 = case... 9 = not in-dorm anymore
for dormNum in range(10):

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

            # we're on an in-dorm round and you don't have in-dorm
            if (dormNum != 9 and emailToIndorm[myEmail] != dormNum):
                continue

            # we're on an in-dorm round and this is the wrong dorm
            if (dormNum != 9 and dormNum != rooms[desiredRoom][2]):
                continue


            # case 1: pulling a single
            if rooms[desiredRoom][0] == 1:
                # pull myself into the room & mark it occupied
                emailToRoom[myEmail] = desiredRoom
                rooms[desiredRoom][1] = rooms[desiredRoom][1] - 1
                if(rooms[desiredRoom][1] <= 0): print(desiredRoom+" closed on "+str(myNum))

                # now try to pull my friend into another room...
                pulledFriend = False # boolean that i need for lock-pulling purposes

                # must be more rooms of this type
                if rooms[desiredRoom][1] > 0: 
                    # must not be a sontag 3-man
                    if desiredRoom != "Sontag single in a suite with 1 single, 1 double":
                        # must have someone to pull
                        if len(plan[1]) > 0:

                            friendEmail = plan[1][0]
                            friend = emailToPerson[friendEmail]

                            # i must be allowed to pull this person
                            if myEmail in friend.pullBuddies:
                                # this person cant already have a room
                                if friendEmail not in emailToRoom:
                                    # if this is an in-dorm round, they need in-dorm
                                    if dormNum == 9 or emailToIndorm[friendEmail] == dormNum:
                                        # phew! that was a lot of nested ifs
                                        # pull my friend into a room & mark it occupied
                                        emailToRoom[friendEmail] = desiredRoom
                                        rooms[desiredRoom][1] = rooms[desiredRoom][1] - 1
                                        if(rooms[desiredRoom][1] <= 0): print(desiredRoom+" closed on "+str(myNum))
                                        pulledFriend = True
                        
                # now try to lock pull...
                # must be a lockpullable room
                if desiredRoom in lockPullable:
                    # must have taken the other single, OR it's a sontag 3-man
                    if pulledFriend or desiredRoom == "Sontag single in a suite with 1 single, 1 double":
                        lockPullRoom = lockPullable[desiredRoom]
                        # must be trying to pull the right # of people
                        if len(plan[2]) == rooms[lockPullRoom][0]:
                            # room must still be available
                            if rooms[lockPullRoom][1] > 0:
                                # now check that my friends are OK with being pulled
                                isValid = True
                                for friendEmail in plan[2]:
                                    friend = emailToPerson[friendEmail]

                                    # am i allowed to pull this person?
                                    if myEmail not in friend.pullBuddies:
                                        isValid = False

                                    # has this person already found a room?
                                    if friendEmail in emailToRoom:
                                        isValid = False
                                
                                if isValid:
                                    # pull in all my friends!
                                    for friendEmail in plan[2]:
                                        emailToRoom[friendEmail] = lockPullRoom
                                    # and mark the lock-pulled room as occupied
                                    rooms[lockPullRoom][1] = rooms[lockPullRoom][1] - 1
                                    if(rooms[lockPullRoom][1] <= 0): print(lockPullRoom+" closed on "+str(myNum))

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

                    # if this is an in-dorm round, does this person have it?
                    if indorm != 9 and emailToIndorm[friendEmail] != dormNum:
                        isValid = False

                if isValid:
                    # pull myself into the room
                    emailToRoom[myEmail] = desiredRoom

                    # pull all my friends
                    for friendEmail in plan[1]:
                        emailToRoom[friendEmail] = desiredRoom

                    # mark this room as occupied
                    rooms[desiredRoom][1] = rooms[desiredRoom][1] - 1
                    if(rooms[desiredRoom][1] <= 0): print(desiredRoom+" closed on "+str(myNum))