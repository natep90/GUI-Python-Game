import random

# class for the users player character
class Player:
    def __init__(self, name, age, location, school):
        self.name = name
        self.age = age
        self.location = location
        self.school = school
        self.items = []
        self.totems = []
        self.health = 100
        self.max_health = 100
        self.route = ["Geography Classroom"] # this is the first location. (next locations added on player.move)
        self.correct_route_direction = True # this is used to ensure route direction is reset when route is viewed
        
    # view a reversed route 
    def reverse_route(self):
        if self.correct_route_direction == True:
            self.route.reverse()
            self.correct_route_direction = False
        else:
            self.route.reverse()
            self.correct_route_direction = True

    # this method is used when the view_route screen is exited
    # it ensures the route is put back in the correct order
    # so that when new locations are added, the route remains in correct order
    def ensure_correct_route_direction(self):
        if self.correct_route_direction == False:
            self.route.reverse()
            self.correct_route_direction = True

    # move player to new location and add new location to route list               
    def move(self, new_location):
        self.location = new_location
        self.route.append(self.location.name)

    # pick up item/totem and append to the appropriate player list
    def pick_up_item(self, item):
        if isinstance(item, Consumable):
            self.items.append(item)
        else:
            self.totems.append(item)

# class to create the rooms and navigable map (via the connections list)    
class Area:
    def __init__(self, name, connections, characters, items_to_collect, story, message=""):
        self.name = name
        self.connections = connections
        self.characters = characters
        self.items_to_collect = items_to_collect
        self.story = story # plays the first time a location is visited (when area.visited attribute == False)
        self.message = message
        self.visited = False # will be switched to True when Player visits Area

# class to create the quiz master characters
class Character:
    def __init__(self, name, questions, weapon, items):
        self.name = name
        self.questions = questions
        self.weapon = weapon
        self.items = items # refers to the totem - list is popped when quiz is won by player
        self.damage = random.randint(10, 50) 

# class to create food/drink to replenish health
class Consumable:
    def __init__(self, name, value):
        self.name = name
        self.value = value

# class to create totems to be collected
class Totem:
    # totem count used to check against players current totem amount
    # game is won when player collects all totems
    totem_count = 0
    def __init__(self, name):
        self.name = name
        Totem.totem_count += 1 # auto increment totem_count when Totem object is created

