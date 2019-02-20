

namenum = {
    "abarth" : 0,
    "lfriedberg" : 1,
    "tschneider" : 2,
    "jwang" : 3,
    "gotit": 4
}

numname = dict((reversed(item) for item in namenum.items()))

class Room:
    def __init__(self, beds, unit):
        self.beds = beds
        self.unit = unit
        self.occupants = []
    
    def getAttributes(self):
        a = "occupants: "
        for i in self.occupants:
            a = a + i.getEmail() + ", "
        a = a + "  unit: " + str(self.unit)
        return a

    def isFull(self):
        return len(self.occupants) == self.beds

    def pull(self, newKid):
        self.occupants.append(newKid)
        if len(self.occupants) > self.beds:
            print("this is so crowded")



class Person:
    def __init__(self, number, email, plans):
        self.number= number
        self.email = email
        self.plans = plans
       # self.room = 

    def getEmail(self):
        return self.email

    def addPlan(self,newPlan):
        self.plans.append(newPlan)

    def getPlans(self):
        return self.plans

    def pull(self, newRoom):
        self.room = newRoom

 #   def getRoom(self):
        return self.room
  
#rooms        
room1 = Room(1,1)
room2 = Room(1,2)
room3 = Room(1,3)
room4 = Room(1,4)
room5 = Room(1,5)

#test plans
annaplan = [room1]
lilypaln = [room2, room4]
tplan = [room2, room1, room3]
wangplant = [room3, room4]
gotaplan = [room5, room1]

plans = [annaplan,lilypaln,tplan,wangplant,gotaplan]
pals=[]

for i in range(0,5):
    pals.append(Person(i, numname[i], plans[i]))

def draw(ral):
    for plan in ral.getPlans():
        if not plan.isFull():
            plan.pull(ral)
            ral.pull(plan)
            print(plan.getAttributes())
            return
    print("no valid plans :(")

def roomDraw():
    for ral in pals:
        draw(ral)
