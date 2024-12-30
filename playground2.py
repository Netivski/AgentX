from dataclasses import dataclass, field
from queue import Queue
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
    commonWing: BoolGrid
    wormholes: LocationGrid

    def __init__(self, name:str, width:int, height:int):
        self.name = name
        self.width = width
        self.height = height
        self.space = [[0 for _ in range(self.height)] for _ in range(self.width)]
        self.commonWing = [[False for _ in range(self.height)] for _ in range(self.width)]
        self.wormholes = [[None for _ in range(self.height)] for _ in range(self.width)]

@dataclass
class Thing:
    name: str
    where: Location
    initialLocation: Location

State = dict[str, Thing]

@dataclass
class World:
    ground: Ground
    state: State

@dataclass
class Object(Thing):
    pass

@dataclass
class Agent(Thing):
    objects: list[Object]
    world: World

    def isInWing(self) -> bool:
        return self.world.ground.commonWing[self.where.xpos][self.where.ypos]

class PlayGroundError(Exception):
    pass

class NoCookieProblemError(Exception):
    pass

class NoGatheringProblemError(Exception):
    pass

Path = tuple[str,]

directions = {'U':Location(0,1), 'D':Location(0,-1), 'L':Location(-1,0), 'R':Location(1,0)}

# Transforms state of a world in a dictionary[str(location), Thing]
def getStateByLocation(w: World) -> State:
    s = dict()
    for val in w.state.values():
        s[str(val.where)] = val
    return s

def copyGround(src: Ground) -> Ground:
    g = Ground(src.name, src.width, src.height)
    for col in range(g.height):
        for row in range(g.width):
            g.space[row][col] = src.space[row][col]
            g.commonWing[row][col] = src.commonWing[row][col]
            if (src.wormholes[row][col] != None):
                wh = src.wormholes[row][col]
                g.wormholes[row][col] = Location(wh.xpos, wh.ypos)
            else:
                g.wormholes[row][col] = None
    return g

# Creates a copy of the world and a copy of all its agents and objects, keeping the same ground
def copyWorld(src: World) -> World:
        w = newWorld(src.ground.name, src.ground.width, src.ground.height)
        # w.ground = src.ground
        w.ground = copyGround(src.ground)

        for thing in src.state.values():
            if (isinstance(thing, Agent)):
                newThing = newAgent(thing.name)
                newThing.world = w
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
    return Agent(name,Location(0,0), None, [], None)

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
            w.ground.commonWing[i][j] = True

def setWormhole(w:World, loc1:Location, loc2:Location) -> None:

    if (not (checkBounds(w, loc1)) or not (checkBounds(w, loc2))):
        raise PlayGroundError
    
    # Ensure wormhole ends are at least 2 positions apart
    if (abs(loc1.xpos-loc2.xpos) < 2 or abs(loc1.ypos-loc2.ypos) < 2):
        raise PlayGroundError
    
    # Ensure wormhole ends are not adjacent to any other wormhole
    for dir in directions.values():
        for locToCheck in [Location(loc1.xpos + dir.xpos, loc1.ypos + dir.ypos), Location(loc2.xpos + dir.xpos, loc2.ypos + dir.ypos)]:
            if (checkBounds(w, locToCheck) and w.ground.wormholes[locToCheck.xpos][locToCheck.ypos] != None):
                raise PlayGroundError
    
    # Ensure wormhole ends don't land on any agent or object
    for thing in w.state.values():
        if (thing.where == loc1 or thing.where == loc2):
            raise PlayGroundError
    
    # Add ends of the wormhole to the grid
    w.ground.wormholes[loc1.xpos][loc1.ypos] = loc2
    w.ground.wormholes[loc2.xpos][loc2.ypos] = loc1


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
    if (isinstance(thing, Agent)):
        thing.world = w
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

    if (w.ground.wormholes[newLocation.xpos][newLocation.ypos] != None):
        whEnd = w.ground.wormholes[newLocation.xpos][newLocation.ypos]
        newLocation = Location(whEnd.xpos + directions[dir].xpos, whEnd.ypos + directions[dir].ypos)

    if not(checkBounds(w, newLocation)) or (checkAltDiff(w, newLocation, ag.initialLocation) > (len(ag.objects))):
        return None
    
    if not(w.ground.commonWing[newLocation.xpos][newLocation.ypos]):
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
            cast(Agent, newWorld.state[ag.name]).objects.append(newWorld.state.pop(ob.name))
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

def nextWorlds(w:World) -> list[tuple[str,World]]:
    possibleWorlds = list()
    for ag in getAgentsInState(w.state):
        possiblePaths = ["U " + ag.name, "D " + ag.name, "L " + ag.name, "R " + ag.name]
        for p in possiblePaths:
            # for all posible actions in one world, appends actions and the the new world to list
            try:
                nextWorld = pathToWorlds(w, [p])
                possibleWorlds.append([p, nextWorld[-1]])
            except:
                continue
        for ob in getObjectsInState(w.state):
            # if an object is found and adjacent, picks object
            if isAdjacent(ag, ob):
                nextWorld = pickObject(w, ag, ob)
                if nextWorld != None:
                    possibleWorlds.append(["P "+ ag.name +" "+ ob.name, nextWorld])
    return possibleWorlds

'''
Check if location to visit is within bounds, was not visited yet and meets altitude requirements
'''
def isValidMove(w:World, ag:Agent, loc:Location, visited):
    x, y = loc.xpos, loc.ypos
    if checkBounds(w, loc) and not visited[x][y]:
        if checkAltDiff(w, ag.where, loc) <= (len(ag.objects)):
            return True
    return False

def getStateKey(s:State) -> str:
    res = ""
    for k in sorted(s.keys()):
        res = res + k + "|" + str(s[k].where) + "|||"
    return res

def findGoal(w:World, goal:Callable [[State],bool]) -> Path:
    '''
    Queue to store path and state needed to generate other worlds
    Keep track of states already visited and to visit

    For each element in queue:
        generate new worlds and paths to get there
        add to the queue current path and new path along with new state
    '''
    toVisit:Queue[tuple[Path, State, str]] = Queue()
    stateKey = getStateKey(w.state)
    toVisit.put(((), w.state, stateKey))

    visited:set[str] = set([])
    nextVisit:set[str] = set([])
    nextVisit.add(stateKey)
    
    while toVisit.qsize() > 0:
        (path, state, stateKey) = toVisit.get()
        nextVisit.discard(stateKey)
        if (goal(state)):
            return path
        visited.add(stateKey)
        for (action, newWorld) in nextWorlds(World(w.ground, state)):
            # Should only be done if state was not visited or not marked as to visit
            newStateKey = getStateKey(newWorld.state)
            if not(newStateKey in visited) and not(newStateKey in nextVisit): 
                toVisit.put((path+(action,),newWorld.state, newStateKey))
                nextVisit.add(newStateKey)
    
    raise PlayGroundError()

# Checks if there's any agent that has the same location as an object
def IsCookieFound_Goal(s:State)->bool:
    for agent in getAgentsInState(s):
        if (len(agent.objects) > 0):
            return True
        # for object in agent.objects:
        #     if (agent.where == object.where):
        #         return True
    return False

# Returns a list of Objects in a state dictionary
def getObjectsInState(s:State) -> list[Object]:
    return getThingsInStateByType(s, Object)

# Returns a list of Agents in a state dictionary
def getAgentsInState(s:State) -> list[Agent]:
    return getThingsInStateByType(s, Agent)

# Returns a list of instances of type 't' in a state dictionary
def getThingsInStateByType(s:State, t:type) -> list[Thing]:
    things = []
    for thing in s.values():
        if (isinstance(thing, t)):
            things.append(thing)
    return things

def validCookieMonster(w:World) -> bool:
    if (w.ground.width * w.ground.height > 400):
        return False
    agents = getAgentsInState(w.state)
    if (len(agents) > 1):
        return False
    cookies = getObjectsInState(w.state)
    if (not(1 <= len(cookies) <= 10)):
        return False
    return True

def CookieMonster(w:World) -> Path:
    return findCookies(w)

# Determines the shortest path that will make an agent collect all the cookies
def findCookies(w:World) -> Path:
    if (not validCookieMonster(w)):
        raise NoCookieProblemError
    finalPath = []
    cookies = getObjectsInState(w.state)
    while (cookies):
        path = findGoal(w, IsCookieFound_Goal)
        getAgentsInState(w.state)[0].objects.clear()
        finalPath.extend(path)
        worlds = pathToWorlds(w, path)
        if (len(worlds) > 0):
            w = worlds[-1]
        cookies = getObjectsInState(w.state)
    return finalPath


# Checks if the only agent in the world is in a common wing
def IsAgentInWing_Goal(s:State)->bool:
    ag = getAgentsInState(s)[0]
    return ag.isInWing()


def replaceOtherAgentsBySkyscrapper(w:World, agentName:str) -> World:
    newWorld = copyWorld(w)
    agents = getAgentsInState(newWorld.state)
    for ag in agents:
        if (ag.name == agentName):
            continue
        newWorld.ground.space[ag.where.xpos][ag.where.ypos] = 999999
        newWorld.state.pop(ag.name)
    return newWorld

def gatherWizards(w:World)->Path:
    if (w.ground.width * w.ground.height > 400):
        raise NoGatheringProblemError
    agents = getAgentsInState(w.state)
    if (not(1 <= len(agents) <= 10)):
        raise NoGatheringProblemError
    objects = getObjectsInState(w.state)
    if (len(objects) > 0):
        raise NoGatheringProblemError
    w = copyWorld(w)
    finalPath = []
    for ag in agents:
        newWorld = replaceOtherAgentsBySkyscrapper(w, ag.name)
        res = findGoal(newWorld, IsAgentInWing_Goal)
        finalPath.extend(res)
        w.state.pop(ag.name)
    return finalPath

'''
Print the world in the console
If the cell is an Agent prints an 'A'
If it's an Object prints an 'X'
Otherwise prints the altitude of the cell
'''
def PrintWorld(w: World):
    print()
    s = getStateByLocation(w)
    for col in range(w.ground.height):
        for row in range(w.ground.width):
            currLoc = Location(row, col)
            if (str(currLoc) in s.keys()):
                if (isinstance(s[str(currLoc)],Agent)):
                    print("A", end="")
                else:
                    print("X", end="")
            elif (w.ground.wormholes[row][col] != None):
                print("W", end="")
            elif (w.ground.commonWing[row][col]):
                print(".", end="")
            else:
                print (w.ground.space[row][col], end="")
        print()
    return

def getAgent(w:World,n:str)->Agent:
    return cast(Agent,w.state[n])

def getObject(w:World,n:str)->Object:
    return cast(Object,w.state[n])

'''
Testing area
'''
# def g0(s:State)->bool:
#     return cast(Agent, s["Ze"]).where == Location(2,0) and len(cast(Agent, s["Ze"]).objects) == 1


# w = newWorld("Playground",3,3)
# robot1 = newAgent("CookieMonster")
# putThing(w,robot1,Location(0,0))
# box0 = newObject("box0")
# putThing(w,box0,Location(1,1))
# box1 = newObject("box1")
# putThing(w,box1,Location(2,2))
# # box2 = newObject("box2")
# # putThing(w,box2,Location(1,7))
# # box3 = newObject("box3")
# # putThing(w,box3,Location(1,19))
# # setAltitude(w,Location(3,0),2,11,9) ## check this
# # setAltitude(w,Location(3,12),2,8,9) ## check this
# print(CookieMonster(w))


# w:World = newWorld("S",3,1)
# #PrintWorld(w)
# a = newAgent("Ze")
# putThing(w, a, Location(0,0))

# o = newObject("Maria")
# putThing(w, o, Location(1,0))

# print(getStateKey(w.state))

#PrintWorld(w)

# res = findGoal(w, g0)
# print(res)

# b = newAgent("Quim")
# putThing(w, b, Location(3,3))

# c = newAgent("Tó")
# putThing(w, c, Location(0,9))

# d = newAgent("Manel")
# putThing(w, d, Location(9,9))

# # o1 = newObject("Sophie")
# # putThing(w, o1, Location(7,4))

# # o2 = newObject("Julie")
# # putThing(w, o2, Location(7,7))

# setComWing(w, Location(4,4), 4, 4)
# setAltitude(w, Location(0,3), 1, 6, 9)
# # setWormhole(w, Location(3,4), Location(5,7))
# # setWormhole(w, Location(5,4), Location(7,7))

# # wn = moveAgent(w, getAgent(w, "Quim"), "R")
# # PrintWorld(wn)
# # wn = moveAgent(wn, getAgent(wn, "Quim"), "R")
# # PrintWorld(wn)
# # print(getAgent(wn, "Quim").where)

# res = gatherWizards(w)
# print(res)

# w2 = pathToWorlds(w, res)
# PrintWorld(w2[len(w2)-1])