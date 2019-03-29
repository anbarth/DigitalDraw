##############################################################
####################### ROOMS ################################
##############################################################

rooms = {
    # room type : [# people allowed, # rooms of this type]
    "Atwood single" : [1, 48],
    "Atwood suite double" : [2, 12], 
    "Atwood triple" : [3, 12], 
    "Atwood column double" : [2, 4], 
    "Atwood efficiency" : [2, 6],
    "Case single" : [1, 32],
    "Case double" : [2, 32],
    "Case triple" : [3, 1],
    "Case quad" : [4, 4],
    "Drinkward single in a suite with 3 singles, 1 triple" : [1, 24],
    "Drinkward triple in a suite with 3 singles, 1 triple" : [3, 8],
    "Drinkward single in a suite with 2 singles, 1 triple" : [1, 4],
    "Drinkward triple in a suite with 2 singles, 1 triple" : [3, 2],
    "Drinkward O-side single" : [1, 37],
    "Drinkward O-side triple" : [3, 25],
    "East single" : [1, 16],
    "East double" : [2, 36],
    "Linde single in a suite with 2 singles, 2 doubles" : [1, 12],
    "Linde double in a suite with 2 singles, 2 doubles" : [2, 12],
    "Linde single in a suite with 4 singles, 1 double" : [1, 8],
    "Linde double in a suite with 4 singles, 1 double" : [2, 2],
    "Linde double in a suite with 3 doubles" : [2, 12],
    "Linde double in a suite with 2 doubles" : [2, 2],
    "North single" : [1, 16],
    "North double" : [2, 36],
    "Sontag single in a suite with 3 singles, 1 double" : [1, 36], 
    "Sontag double in a suite with 3 singles, 1 double" : [2, 12],
    "Sontag single in a suite with 2 singles, 1 double" : [1, 6],
    "Sontag double in a suite with 2 singles, 1 double" : [2, 3],
    "Sontag single in a suite with 1 single, 1 double" : [1, 2],
    "Sontag double in a suite with 1 single, 1 double" : [2, 2],
    "South single in a suite with 4 singles" : [1, 32], 
    "South single in a suite with 3 singles" : [1, 24],
    "South single in a suite with 2 singles" : [1, 8],
    "South double" : [2, 4],
    "West single" : [1, 16],
    "West double" : [2, 36]
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

        # TODO implement in-dorm? at all?

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

            if isValid:
                # pull myself into the room
                emailToRoom[myEmail] = desiredRoom

                # pull all my friends
                for friendEmail in plan[1]:
                    emailToRoom[friendEmail] = desiredRoom

                # mark this room as occupied
                rooms[desiredRoom][1] = rooms[desiredRoom][1] - 1
                if(rooms[desiredRoom][1] <= 0): print(desiredRoom+" closed on "+str(myNum))