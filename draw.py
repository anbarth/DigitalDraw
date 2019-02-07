

namenum = {
    "abarth" : 1,
    "lfriedberg" : 2,
    "tschneider" : 3,
    "jwang" : 4,
    "gotit": 5
}

numname = dict((reversed(item) for item in namenum.items()))

numname = {
    1 : Person(1, "abarth", [])
}

room1 = Room(1,0)
room2 = Room(1,0)
room3 = Room(1,0)
room4 = Room(1,0)
room5 = Room(1,0)


class Room:
    def __init__(self, beds, unit):
        self.beds = beds
        self.unit = unit
        self.occupants = []

    def isFull():
        return len(self.occupants) == self.beds

    def pull(name):
        self.occupants.append(name)

class Person:
    def __init__(self, number, email, plans):
        self.number= number
        self.email = email
        self.plans = plans

    def addPlan():
        return

    def getPlans():
        return self.plans

annaplan = [room1]
lilypaln = [room2]
tplan = [room2, room1, room3]
wangplant = [room3, room4]
gotaplan = [room5, room1]

planclan = [annaplan,lilypaln,tplan,wangplant,gotaplan]
pals = []

for i in range(1:6):
    pals.append(Person(numname[i], planclan[i])

for i in range(1,6): #1 thru number of people + 1
    
        

