from dataclasses import dataclass, field
from typing import Callable
from typing import TypeVar


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
    objects: list[object]

Thing = Agent | Object
State = dict[str, Thing]

@dataclass
class World:
    ground: Ground
    state: State

class PlayGroundError:
    pass

Path = tuple[str,]

def copyWorld(src: World) -> World:
        w = newWorld(src.ground.name, src.ground.width, src.ground.height)
        for thing in src.state.values():
            if (isinstance(thing, Agent)):
                agent = newAgent(thing.name)
                agent.where = Location(thing.where.xpos, thing.where.ypos)
                for agObj in thing.objects:
                    o = newObject(agObj.name)
                    o.where = Location(agObj.where.xpos, agObj.where.ypos)
                    agent.objects.append(o)
                w.state[agent.name] = agent
            elif (isinstance(thing, Object)):
                obj = newObject(thing.name)
                obj.where = Location(thing.where.xpos, thing.where.ypos)
                w.state[obj.name] = obj
        return w

def newAgent(name:str) -> Agent:
    if (not name.isascii()):
        raise PlayGroundError
    return Agent(name,Location(0,0), [])

def newObject(name:str) -> Object:
    if (not name.isascii()):
        raise PlayGroundError
    return Object(name,Location(0,0))

def newWorld (name:str, width: int, height: int) -> World: 
    if (not name.isascii()) or (width < 0 or width > MAX_WIDTH) or (height < 0 or height > MAX_HEIGHT):
        raise PlayGroundError
    g = Ground(name, width, height)
    return World(g, {})

def setAltitude (w:World, loc: Location, width:int, height:int, alt:int) -> None:
    if (loc.xpos+width > w.ground.width) or (loc.ypos+height > w.ground.height):
        raise PlayGroundError
    if (alt < 0):
        raise PlayGroundError
    for i in range(loc.ypos, loc.ypos+height):
        for j in range(loc.xpos, loc.xpos+width):
            w.ground.space[i][j] = alt

'''
Checks if thingA and thingB are in adjacent positions without considering diagonals
'''
def isAdjacent (thingA:Thing, thingB:Thing) -> bool:
    if (thingA.where.ypos == thingB.where.ypos):
        if ((thingA.where.xpos+1 == thingB.where.xpos) or (thingA.where.xpos-1 == thingB.where.xpos)):
            return True
    if (thingA.where.xpos == thingB.where.xpos):
        if ((thingA.where.ypos+1 == thingB.where.ypos) or (thingA.where.ypos-1 == thingB.where.ypos)):
            return True
    return False

'''
Checks if a Thing with the same name already exists in the world
If it does raises a PlayGroundError
If not adds the Thing's name and a key and its instance as the value
'''
def putThing (w:World, thing:Thing, loc:Location) -> Thing:
    if (thing.name in w.state.keys()):
        raise PlayGroundError
    for val in w.state.values():
        if (str(loc) == str(val.where)):
            raise PlayGroundError
    w.state[thing.name] = thing
    thing.where = Location(loc.xpos, loc.ypos)
    return thing

'''
Creates a newLocation setting it's positions according to the supplied direction
Validates that the newLocation falls within limits
If it doesn't returns None
Validates if there is another Thing in the same position
If it is raises an exception
If it's not creates a deep copy of the world and sets the agent to its newLocation
'''
def moveAgent (w:World, ag:Agent,dir:str)-> World|None:
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
    for val in w.state.values():
        if (str(newLocation) == str(val.where)):
            print("Something is there!")
            return None

    #newWorld = copy.deepcopy(w)
    newWorld = copyWorld(w)
    newWorld.state[ag.name].where = newLocation

'''
Checks to see if the Agent and the Object are adjacent
If not returns None
If they are adjacent, creates a deep copy of the world
In the new world remove the object and adds it to the Agent's object list
'''
def pickObject (w:World, ag: Agent , ob: Object)->World|None:
    if (ob.name in w.state.keys() and isAdjacent(ag, ob)):
        #newWorld = copy.deepcopy(w)
        newWorld = copyWorld(w)
        newWorld.state[ag.name].objects.append(newWorld.state.pop(ob.name))
        return newWorld
    return None

#def pathToWorlds (w:World, path: Path) -> list [World]: 
#def findGoal (w:World, goal:Callable [[State],bool])->Path:

'''
Print the world in the console
If the cell is an Agent prints an 'A'
If it's an Object prints an 'X'
Otherwise prints the altitude of the cell

TODO: Needs to be updated because it's not listing Things
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
putThing(w, o, Location(1,1))


PrintWorld(w)
if (pickObject(w, b, o) == None):
    print("Nothing to pick!")
PrintWorld(w)
moveAgent(w, b, "U")
PrintWorld(w)
if (pickObject(w, b, o) != None):
    print("Picked something!")
PrintWorld(w)

exit(0)
for i in range(0,6):
    moveAgent(w, b, "U")
    moveAgent(w, b, "R")
    PrintWorld(w)


x = Location(2,3)
print (x)
