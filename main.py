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
        self.space = [[0 for _ in range(self.height)] for _ in range(self.width)]

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
    initialLocation: Location

@dataclass
class Agent:
    name: str
    where: Location
    initialLocation: Location
    objects: list[object]

Thing = Agent | Object
State = dict[str, Thing]

@dataclass
class World:
    ground: Ground
    state: State

class PlayGroundError(Exception):
    pass

Path = tuple[str,]

directions = {'U':Location(0,1), 'D':Location(0,-1), 'L':Location(-1,0), 'R':Location(1,0)}

def getStateByLocation(w: World) -> State:
    s = dict()
    for val in w.state.values():
        s[str(val.where)] = val
    return s

def copyWorld(src: World) -> World:
        w = newWorld(src.ground.name, src.ground.width, src.ground.height)
        w.ground = src.ground
        for thing in src.state.values():
            if (isinstance(thing, Agent)):
                agent = newAgent(thing.name)
                agent.where = Location(thing.where.xpos, thing.where.ypos)
                agent.initialLocation = Location(thing.initialLocation.xpos, thing.initialLocation.ypos)
                for agObj in thing.objects:
                    o = newObject(agObj.name)
                    o.where = Location(agObj.where.xpos, agObj.where.ypos)
                    agent.objects.append(o)
                w.state[agent.name] = agent
            elif (isinstance(thing, Object)):
                obj = newObject(thing.name)
                obj.where = Location(thing.where.xpos, thing.where.ypos)
                obj.initialLocation = Location(thing.initialLocation.xpos, thing.initialLocation.ypos)
                w.state[obj.name] = obj
        return w

def newAgent(name:str) -> Agent:
    if (not name.replace("_", "").isalnum()):
        raise PlayGroundError
    return Agent(name,Location(0,0), None, [])

def newObject(name:str) -> Object:
    if (not name.replace("_", "").isalnum()):
        raise PlayGroundError
    return Object(name,Location(0,0), None)

def newWorld (name:str, width: int, height: int) -> World: 
    if (not name.replace("_", "").isalnum()) or (len(name) == 0):
        raise PlayGroundError
    if (width < 0 or width > MAX_WIDTH) or (height < 0 or height > MAX_HEIGHT) or (height == 0 and width == 0):
        raise PlayGroundError
    g = Ground(name, width, height)
    return World(g, {})

def setAltitude (w:World, loc: Location, width:int, height:int, alt:int) -> None:
    if (loc.xpos+width > w.ground.width) or (loc.ypos+height > w.ground.height):
        raise PlayGroundError
    if (loc.xpos < 0) or (loc.ypos < 0):
        raise PlayGroundError
    if (alt < 0):
        raise PlayGroundError
    for i in range(loc.xpos, loc.xpos+width):
        for j in range(loc.ypos, loc.ypos+height):
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
    thing.initialLocation = Location(loc.xpos, loc.ypos)
    return thing

def checkAltDiff(w:World, locA:Location, locB:Location):
    return abs(w.ground.space[locA.xpos][locA.ypos] - w.ground.space[locB.xpos][locB.ypos])

def checkBounds(w:World, loc:Location) -> bool:
    if (0 <= loc.ypos < w.ground.height) and (0 <= loc.xpos < w.ground.width):
        return True
    return False

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
    newLocation.xpos += directions[dir].xpos
    newLocation.ypos += directions[dir].ypos

    if not checkBounds(w, newLocation):
        return None
    if (checkAltDiff(w, newLocation, ag.initialLocation) > (len(ag.objects))):
        return None
    
    #Raise exception if there's a Thing in the Location the agent is moving to
    for val in w.state.values():
        if (str(newLocation) == str(val.where)):
            raise PlayGroundError()

    newWorld = copyWorld(w)
    newWorld.state[ag.name].where = newLocation
    return newWorld

'''
Checks to see if the Agent and the Object are adjacent
If not returns None
If they are adjacent, creates a deep copy of the world
In the new world remove the object and adds it to the Agent's object list
'''
def pickObject (w:World, ag: Agent , ob: Object)->World|None:
    if (ag.name in w.state.keys() and ob.name in w.state.keys() and isAdjacent(ag, ob)):
        if (checkAltDiff(w, ag.where, ob.where) == 0):
            newWorld = copyWorld(w)
            newWorld.state[ag.name].objects.append(newWorld.state.pop(ob.name))
            return newWorld
    return None

def pathToWorlds (w:World, path: Path) -> list [World]: 
    worlds = [World]
    currWorld = w
    try:
        for p in path:
            cmd = p.split(" ")
            if (len(cmd) == 2):
                currWorld = moveAgent(currWorld, currWorld.state[cmd[1]], cmd[0])
                if (currWorld == None):
                    raise PlayGroundError()
                worlds.append(currWorld)
            else:
                currWorld = pickObject(currWorld, currWorld.state[cmd[1]], currWorld.state[cmd[2]])
                if (currWorld == None):
                    raise PlayGroundError()
                worlds.append(currWorld)
    except:
        raise PlayGroundError()

    return worlds

def findGoal (w:World, goal:Callable [[State],bool])->Path:
    return None


'''
Print the world in the console
If the cell is an Agent prints an 'A'
If it's an Object prints an 'X'
Otherwise prints the altitude of the cell
'''
def PrintWorld(w: World):
    print()
    s = getStateByLocation(w)
    for col in range(w.ground.width):
        for row in range(w.ground.height):
            currLoc = Location(row, col)
            if (str(currLoc) in s.keys()):
                if (isinstance(s[str(currLoc)],Agent)):
                    print("A", end="")
                else:
                    print("X", end="")
            else:
                print (w.ground.space[row][col], end="")
        print()
    return
    
# ------------------------------------------
DEBUG = False

w:World = newWorld("S",6,6)
setAltitude(w,Location(1,1),2,1,3)
print(w.ground.space)
PrintWorld(w)

a = newAgent("Ze")
b = newAgent("Quim")
o = newObject("Maria")

putThing(w, a, Location(2,3))
putThing(w, b, Location(0,0))
putThing(w, o, Location(1,1))

# path = navigate_grid(w, a)
    
# # Print the visited path
# if path:
#     print(f"Visited cells: {path}")
# else:
#     print(f"No valid path from start position ({start_x}, {start_y}).")

# exit(0)

PrintWorld(w)
if (pickObject(w, b, o) == None):
    print("Nothing to pick!")
PrintWorld(w)
moveAgent(w, b, "U")
PrintWorld(w)
if (pickObject(w, b, o) != None):
    print("Picked something!")
PrintWorld(w)

#exit(0)
for i in range(0,6):
    moveAgent(w, b, "U")
    moveAgent(w, b, "R")
    PrintWorld(w)


x = Location(2,3)
print (x)



