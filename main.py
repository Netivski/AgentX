from dataclasses import dataclass, field

LArray = list[list[int]]

MAX_WIDTH = 50
MAX_HEIGHT = 50

DEBUG = False

@dataclass
class Ground:
    name: str
    width: int
    height: int
    space: LArray

    def initGround(self):
        for row in range(0, self.height):
            self.space.append(list())
            for col in range(0, self.width):
                self.space[row].append(0)

    def __init__(self, name:str, width:int, height:int):
        self.name = name
        self.width = width
        self.height = height
        self.space = LArray()
        self.initGround()

@dataclass
class Location:
    xpos: int
    ypos: int

@dataclass
class Object:
    name: str
    where: Location

@dataclass
class Agent:
    name: str
    where: Location
    objects: list[Object] = field(init=False)

Thing = Agent | Object
State = dict[str, Thing]

@dataclass
class World:
    ground: Ground
    state: State

class PlayGroundError:
    pass

def newAgent(name:str)->Agent:
    if (not name.isascii()):
        raise PlayGroundError
    return Agent(name,Location(0,0))

def newObject(name:str)->Object:
    if (not name.isascii()):
        raise PlayGroundError
    return Object(name,Location(0,0))

def newWorld (name:str, width: int, height: int)->World: 
    if (not name.isascii()) or (width < 0 or width > MAX_WIDTH) or (height < 0 or height > MAX_HEIGHT):
        raise PlayGroundError
    g = Ground(name, width, height)
    return World(g, {})

def setAltitude (w:World, loc: Location, width:int, height:int, alt:int)->None:
    if (loc.xpos+width > w.ground.width) or (loc.ypos+height > w.ground.height):
        raise PlayGroundError
    if (alt < 0):
        raise PlayGroundError
    for i in range(loc.ypos, loc.ypos+height):
        for j in range(loc.xpos, loc.xpos+width):
            w.ground.space[i][j] = alt

'''
Checks if the Thing's location already exists in the dictionary.
If it does raises a PlayGroundError
Otherwise adds the Thing's location and a key to the dictionary and the Thing as the value
'''
def putThing (w:World, thing:Thing, loc:Location)-> Thing:
    if (str(loc) in w.state.keys()):
        raise PlayGroundError
    w.state[str(loc)] = thing
    thing.where = Location(loc.xpos, loc.ypos)
    return thing

'''
1. Creates a newLocation var to store the coordinates the agent is supposed to move
based on the direction (e.g. if Up then increases y by 1)
2. Checks if the location that changed sits inside the ground limits
   If not returns None
3. Checks in the state dictionary if there's a key equal to the target location
   If there's a matching key (meaning there's a Thing there) returns None
4. Removes from the dictionary the Agent's current location
5. Sets the Agent location to the newLocation
6. Adds the new Agent location as a key to the dictionary and the Agent as the value
'''
def moveAgent (w:World, ag:Agent,dir:str)-> World|None:
    if (DEBUG):
        print(str(ag.where))
        print(dir)

    newLocation = Location(ag.where.xpos, ag.where.ypos)
    if (dir == "U"):
        newLocation.ypos += 1
        if (newLocation.ypos >= w.ground.height - 1):
            return None
    elif (dir == "D"):
        newLocation.ypos -= 1
        if (newLocation.ypos - 1 < 0):
            return None
    elif (dir == "L"):
        newLocation.xpos -= 1
        if (newLocation.xpos - 1 < 0):
            return None
    elif (dir == "R"):
        if (newLocation.xpos + 1 >= w.ground.width):
            return None
        newLocation.xpos += 1
        
    #Raise exception if there's a Thing in the Location the agent is moving to
    if (str(newLocation) in w.state.keys()):
        print("Something is there!")
        return None

    w.state.pop(str(ag.where))
    ag.where = newLocation
    w.state[str(ag.where)] = ag

#def pickObject (w:World, ag: Agent , ob: Object)->World|None:
#def pathToWorlds (w:World, path: Path) -> list [World]: 
#def findGoal (w:World, goal:Callable [[State],bool])->Path:

'''
Print the world in the console
If the cell is an Agent prints an 'A'
If it's an Object prints an 'X'
Otherwise prints the altitude of the cell
'''
def PrintWorld(w: World):
    print()
    for row in range(w.ground.height-1, -1, -1):
    #for row in range(0, w.ground.height):
        for col in range(0, w.ground.width):
            currLoc = Location(col, row)
            if (str(currLoc) in w.state.keys()):
                if (isinstance(w.state[str(currLoc)],Agent)):
                    print("A", end="")
                else:
                    print("X", end="")
            else:
                print (w.ground.space[row][col], end="")
        print()
    print()
    
# ------------------------------------------
DEBUG = False

w = newWorld("Earth",6, 6)
setAltitude(w, Location(1, 1), 3, 3, 9)

a = newAgent("Ze")
b = newAgent("Quim")
o = newObject("Maria")

putThing(w, a, Location(2,3))
putThing(w, b, Location(0,0))
putThing(w, o, Location(5,5))

PrintWorld(w)

for i in range(0,6):
    moveAgent(w, b, "U")
    moveAgent(w, b, "R")
    PrintWorld(w)

