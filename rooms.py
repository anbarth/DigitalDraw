rooms = {
    # room type : [# people allowed, # rooms of this type]
    "Atwood single" : [1, 48],
    "Atwood suite double" : [2, 12], 
    "Atwood triple" : [3, 12], 
    "Atwood column double/efficiency" : [2, 10], 
    "Case single" : [1, 32],
    "Case double" : [2, 32],
    "Case triple" : [3, 1],
    "Case quad" : [4, 4],
    "Drinkward suite single" : [1, 28],
    "Drinkward suite triple" : [3, 10],
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
# add drinkward?
# [room you pull, room you get to lock-pull]
lockPullable = {"Sontag single in a suite with 3 singles, 1 double": "Sontag single in a suite with 3 singles, 1 double",
                "Sontag single in a suite with 2 singles, 1 double": "Sontag double in a suite with 2 singles, 1 double",
                "Sontag single in a suite with 1 single, 1 double": "Sontag double in a suite with 1 single, 1 double",
                "South single in a suite with 3 singles": "South single in a suite with 3 singles",
                "Linde single in a suite with 2 singles, 2 doubles": "Linde double in a suite with 2 singles, 2 doubles"}