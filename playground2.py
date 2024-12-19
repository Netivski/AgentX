from dataclasses import dataclass, field
from typing import Callable
from typing import cast
from collections import deque

@dataclass
class Location:
    xpos: int
    ypos: int

LArray = list[list[int]]
BoolGrid = list[list[bool]]
LocationGrid = list[list[Location]]

MAX_WIDTH = 50
MAX_HEIGHT = 50

@dataclass
class Ground:
    name: str
    width: int
    height: int
    space: LArray
    wings: BoolGrid
    wormHoles: LocationGrid

    def __init__(self, name:str, width:int, height:int):
        self.name = name
        self.width = width
        self.height = height
        self.space = [[0 for _ in range(self.height)] for _ in range(self.width)]
        self.wings = [[False for _ in range(self.height)] for _ in range(self.width)]
        self.wormHoles = [[None for _ in range(self.height)] for _ in range(self.width)]

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

class NoCookieProblemError(Exception):
    pass

Path = tuple[str,]

directions = {'U':Location(0,1), 'D':Location(0,-1), 'L':Location(-1,0), 'R':Location(1,0)}

# Transforms state of a world in a dictionary[str(location), Thing]
def getStateByLocation(w: World) -> State:
    s = dict()
    for val in w.state.values():
        s[str(val.where)] = val
    return s

# Creates a copy of the world and a copy of all its agents and objects, keeping the same ground
def copyWorld(src: World) -> World:
        w = newWorld(src.ground.name, src.ground.width, src.ground.height)
        w.ground = src.ground

        for thing in src.state.values():
            if (isinstance(thing, Agent)):
                newThing = newAgent(thing.name)
                for obj in thing.objects:
                    o = newObject(obj.name)
                    o.where = Location(obj.where.xpos, obj.where.ypos)
                    newThing.objects.append(o)
            elif (isinstance(thing, Object)):
                newThing = newObject(thing.name)

            newThing.where = Location(thing.where.xpos, thing.where.ypos)
            newThing.initialLocation = Location(thing.initialLocation.xpos, thing.initialLocation.ypos)
            w.state[newThing.name] = newThing
        return w

def newAgent(name:str) -> Agent:
    if (not name.replace("_", "").isalnum()) or (len(name) == 0):
        raise PlayGroundError
    return Agent(name,Location(0,0), None, [])

def newObject(name:str) -> Object:
    if (not name.replace("_", "").isalnum()) or (len(name) == 0):
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
    if (not(checkBounds(w, Location(loc.xpos+width-1, loc.ypos+height-1)))):
        raise PlayGroundError
    if (alt < 0):
        raise PlayGroundError
    for i in range(loc.xpos, loc.xpos+width):
        for j in range(loc.ypos, loc.ypos+height):
            w.ground.space[i][j] = alt

def setComWing (w:World, loc: Location, width:int, height:int) -> None:
    if (not(checkBounds(w, Location(loc.xpos+width-1, loc.ypos+height-1)))):
        raise PlayGroundError
    for i in range(loc.xpos, loc.xpos+width):
        for j in range(loc.ypos, loc.ypos+height):
            w.ground.wings[i][j] = True

def setWormhole(w:World, loc1:Location, loc2:Location) -> None:
    # Ensure wormhole ends are at least 2 positions apart
    if (abs(loc1.xpos-loc2.xpos) < 2 or abs(loc1.ypos-loc2.ypos) < 2):
        raise PlayGroundError
    
    # Ensure wormhole ends are not adjacent to any other wormhole
    for dir in directions.values():
        for locToCheck in [Location(loc1.xpos + dir.xpos, loc1.ypos + dir.ypos), Location(loc2.xpos + dir.xpos, loc2.ypos + dir.ypos)]:
            if (checkBounds(w, locToCheck) and w.ground.wormHoles[locToCheck.xpos][locToCheck.ypos] != None):
                raise PlayGroundError
    
    # Ensure wormhole ends don't land on any agent or object
    for thing in w.state.values():
        if (thing.where == loc1 or thing.where == loc2):
            raise PlayGroundError
    
    # Add ends of the wormhole to the grid
    w.ground.wormHoles[loc1.xpos][loc1.ypos] = loc2
    w.ground.wormHoles[loc2.xpos][loc2.ypos] = loc1


'''
Checks if thingA and thingB are adjacent
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
Moves the agent in the given direction
Defines the agent's new location based on the supplied direction
Returns None if the new location is out of bounds
Raises exception if there is another Thing in the same location
Otherwise returns a copy of the world with the agent in the new location
'''
def moveAgent (w:World, ag:Agent,dir:str)-> World|None:
    newLocation = Location(ag.where.xpos + directions[dir].xpos, ag.where.ypos + directions[dir].ypos)

    if not(checkBounds(w, newLocation)):
        return None

    if (w.ground.wormHoles[newLocation.xpos][newLocation.ypos] != None):
        whEnd = w.ground.wormHoles[newLocation.xpos][newLocation.ypos]
        newLocation = Location(whEnd.xpos + directions[dir].xpos, whEnd.ypos + directions[dir].ypos)

    if not(checkBounds(w, newLocation)) or (checkAltDiff(w, newLocation, ag.initialLocation) > (len(ag.objects))):
        return None
    
    if not(w.ground.wings[newLocation.xpos][newLocation.ypos]):
        for val in w.state.values():
            if (newLocation == val.where):
                raise PlayGroundError()

    newWorld = copyWorld(w)
    newWorld.state[ag.name].where = newLocation
    return newWorld

'''
Orders and agent to pick an object
Returns None if the two aren't adjacent
Otherwise returns a copy of the world with the object aded to the Agent's object list
'''
def pickObject (w:World, ag: Agent , ob: Object)->World|None:
    if (ag.name in w.state.keys() and ob.name in w.state.keys() and isAdjacent(ag, ob)):
        if (checkAltDiff(w, ag.where, ob.where) == 0):
            newWorld = copyWorld(w)
            newWorld.state[ag.name].objects.append(newWorld.state.pop(ob.name))
            return newWorld
    return None

'''
Receives a list of commands in the form of a path and returns a list of resulting worlds
Commands can be to move and agent in a given direction or instruct an agent to pick an object
If a move or a pick command does not result in a possible world and exception is raised
'''
def pathToWorlds (w:World, path: Path) -> list [World]: 
    worlds = [w]
    currWorld = w
    try:
        for p in path:
            cmd = p.split(" ")
            if (len(cmd) == 2): #In this case it's a move command
                currWorld = moveAgent(currWorld, currWorld.state[cmd[1]], cmd[0])
                if (currWorld == None):
                    raise PlayGroundError()
                worlds.append(currWorld)
            else: #In this case it's a pick command
                currWorld = pickObject(currWorld, currWorld.state[cmd[1]], currWorld.state[cmd[2]])
                if (currWorld == None):
                    raise PlayGroundError()
                worlds.append(currWorld)
    except:
        raise PlayGroundError()

    return worlds

'''
Check if location to visit is within bounds, was not visited yet and meets altitude requirements
'''
def isValidMove(w:World, ag:Agent, loc:Location, visited):
    x, y = loc.xpos, loc.ypos
    if checkBounds(w, loc) and not visited[x][y]:
        if checkAltDiff(w, ag.where, loc) <= (len(ag.objects)):
            return True
    return False

'''
Adaptation of what ChatGPT suggested as the BFS algorithm to the domain of the assignment
Original algorithm can be found in bfs_algorithm.pt
'''
def findGoal(w:World, goal:Callable [[State],bool]) -> Path:
    rows, cols = w.ground.height, w.ground.width
    newWorld = copyWorld(w)
    stateByLoc = getStateByLocation(newWorld)

    for ag in newWorld.state.values():
        if not(isinstance(ag, Agent)):
            continue

        start = Location(ag.where.xpos, ag.where.ypos)

        # Create a queue for BFS and a visited array
        queue = deque([(start.xpos, start.ypos, 0, [])])  # (x, y, distance, path)
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        visited[start.xpos][start.ypos] = True  # Mark the start as visited

        # Perform BFS
        while queue:
            x, y, distance, path = queue.popleft()
            ag.where.xpos = x
            ag.where.ypos = y
            # If we reached the destination, return the distance
            if goal(newWorld.state):
                return path
            
            # Explore all 4 possible directions (up, down, left, right)
            for dir in directions.keys():
                nx, ny = x + directions[dir].xpos, y + directions[dir].ypos
                newLoc = Location(nx, ny)

                # Adjust new location if it lands on a wormhole
                if (checkBounds(w, newLoc)) and (w.ground.wormHoles[newLoc.xpos][newLoc.ypos] != None):
                    whEnd = w.ground.wormHoles[newLoc.xpos][newLoc.ypos]
                    newLoc = Location(whEnd.xpos + directions[dir].xpos, whEnd.ypos + directions[dir].ypos)
                if isValidMove(newWorld, ag, newLoc, visited):
                    visited[newLoc.xpos][newLoc.ypos] = True  # Mark the neighbor as visited

                    # Check to see if there's an Object in the neighbor cell
                    if(str(newLoc) in stateByLoc.keys()) and (isinstance(stateByLoc[str(newLoc)], Object)):
                        # Path to add should instruct agent to pick object and then move 
                        pathToAdd = ["P " + ag.name + " " + stateByLoc[str(newLoc)].name] + [dir + " " + ag.name]
                    else:
                        # Path to add should instruct agent to move 
                        pathToAdd = [dir + " " + ag.name]
                    queue.append((newLoc.xpos, newLoc.ypos, distance + 1, path + pathToAdd))  # Enqueue the neighbor with updated distance and path
        
    # If no path is found, raise exception
    raise PlayGroundError()

# Checks if there's any agent that has the same location as an object
def IsCookieFound_Goal(s:State)->bool:
    for agent in getAgentsInState(s):
        for object in getObjectsInState(s):
            if (agent.where == object.where):
                return True
    return False

# Returns a list of Objects in a state dictionary
def getObjectsInState(s:State) -> list[Object]:
    return getThingsInStateByType(s, Object)

# Returns a list of Agents in a state dictionary
def getAgentsInState(s:State) -> list[Agent]:
    return getThingsInStateByType(s, Agent)

# Returns a list of instances of type 't' in a state dictionary
def getThingsInStateByType(s:State, t:type) -> list[object]:
    things = []
    for thing in s.values():
        if (isinstance(thing, t)):
            things.append(thing)
    return things

# Determines the shortest path that will make an agent collect all the cookies
def findCookies(w:World) -> Path:
    cookies = getObjectsInState(w.state)
    finalPath = []
    while (cookies):
        path = findGoal(w, IsCookieFound_Goal)
        finalPath = finalPath + path
        worlds = pathToWorlds(w, path)
        if (len(worlds) > 0):
            w = worlds[len(worlds)-1]
            print(path)
            PrintWorld(w)
        cookies = getObjectsInState(w.state)
    return finalPath

def gatherWizards(w:World)->Path:
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
            elif (w.ground.wormHoles[currLoc.xpos][currLoc.ypos] != None):
                print("W", end="")
            elif (w.ground.wings[currLoc.xpos][currLoc.ypos]):
                print(".", end="")
            else:
                print (w.ground.space[row][col], end="")
        print()
    return
    
'''
Testing area
'''
def getAgent(w:World,n:str)->Agent:
    return cast(Agent,w.state[n])

def getObject(w:World,n:str)->Object:
    return cast(Object,w.state[n])

w:World = newWorld("S",10,10)
a = newAgent("Ze")
b = newAgent("Quim")
o = newObject("Maria")
o1 = newObject("Sophie")
o2 = newObject("Julie")

# putThing(w, a, Location(6,7))
putThing(w, b, Location(2,4))
putThing(w, o, Location(3,4))
putThing(w, o1, Location(7,4))
putThing(w, o2, Location(6,7))

setComWing(w, Location(1,1), 8, 8)
# setWormhole(w, Location(3,4), Location(5,7))
# setWormhole(w, Location(5,4), Location(7,7))

PrintWorld(w)
# wn = moveAgent(w, getAgent(w, "Quim"), "R")
# PrintWorld(wn)
# wn = moveAgent(wn, getAgent(wn, "Quim"), "R")
# PrintWorld(wn)
# print(getAgent(wn, "Quim").where)


res = findCookies(w)
print(res)
