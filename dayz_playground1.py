# playGroundD

from dataclasses import dataclass
from copy import deepcopy
from typing import Callable
LArray = list[list[int]]

@dataclass
class Ground:
    name: str
    width: int
    height: int
    space: LArray

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
State = dict[str,Thing]

@dataclass
class World:
    ground: Ground
    state: State

@dataclass
class PlayGroundError(Exception):
    pass

def newAgent(name:str) -> Agent:
    for i in name:
        if not (i.isalnum() or i == "_"):
            raise(PlayGroundError)
    ag = Agent(name, Location(0,0), [])
    return(ag)

def newObject(name:str) -> Object:
    for ch in name:
            if not (ch.isalnum() or ch == "_"):
                raise(PlayGroundError)
    ob = Object(name, Location(0,0))
    return(ob)

def newWorld(name:str, width:int, height:int) -> World:
    for ch in name:
        if not (ch.isalnum() or ch == "_"):
            raise(PlayGroundError)
    if name == "":
        raise(PlayGroundError)
    if (width <= 0 or height <= 0):
        raise(PlayGroundError)
    matriz = matrix(LArray, width, height)
    g = Ground(name, width, height, matriz)
    return World(g, {})

# makes state matrix
def matrix(space: LArray, width: int, height: int):
    space = LArray()
    # for each x in width inserts a list
    for row in range(width):
        space.insert(row, list())
        # for each y in height inserts 0
        for col in range(height):
            space[row].append(0)
    return(space)

def setAltitude(w:World, loc:Location, width:int, heigth:int, alt:int) -> None:
    # checks if its within ground bounds
    if (loc.xpos+width > w.ground.width) or (loc.ypos+heigth > w.ground.height):
        raise(PlayGroundError)
    if (loc.xpos < 0) or (loc.ypos < 0):
        raise(PlayGroundError)
    if (alt < 0):
        raise(PlayGroundError)
    for i in range(loc.xpos, loc.xpos+width):
        for j in range(loc.ypos, loc.ypos+heigth):
            w.ground.space[i][j] = alt

initialAltitude = {} # dictionary Agent name,int that keeps as key the name of the agent
# and for value the altitude of the inicial location, for all agents
def putThing(w:World, thing:Thing, loc:Location) -> Thing:
    if thing.name in w.state.keys():
        raise PlayGroundError
    for val in w.state.values():
        if str(loc) == str(val.where):
            raise PlayGroundError
    thing.where = Location(loc.xpos, loc.ypos)
    w.state[thing.name] = thing
    if isinstance(thing, Agent):
        initialAltitude[thing.name] = w.ground.space[thing.where.xpos][thing.where.ypos]
    return(thing)

# creates a dictionary with keys as locations strings and values as the corresponding things
def stateToLocDict(w:World) -> dict[str,Thing]:
    dicionario = dict()
    for val in w.state.values():
        dicionario[str(val.where)] = val
    return dicionario

# funtion to visualize code, prints a matrix with coordinates A for agents, X for objects
# and numbers of the corresponding altitude
def printWorld(w:World):
    loc_dicionario = stateToLocDict(w)
    for row in range(w.ground.width-1, -1, -1):
        for col in range(w.ground.height):
            currLoc = Location(row, col)
            if (str(currLoc) in loc_dicionario.keys()):
                if (isinstance(loc_dicionario[str(currLoc)],Agent)):
                    print("A", end=" ")
                else:
                    print("X", end=" ")
            else:
                print(w.ground.space[col][row], end=" ")
        print()
    print()

# deepcopies world state and mantains world ground
def copyWorld(src:World) -> World:
    w = World(src.ground, (deepcopy(src.state)))
    return(w)

# gets the altitude difference between two things
def getAltDiff(w:World, th1:Thing, th2:Thing) -> int:
    return abs((w.ground.space[th1.where.xpos][th1.where.ypos]) - (w.ground.space[th2.where.xpos][th2.where.ypos]))

def moveAgent(w:World, ag:Agent, dir:str) -> World | None:
    new_loc = Location(ag.where.xpos, ag.where.ypos)
    if (dir == "R"):
        new_loc.xpos += 1
        if (new_loc.xpos > w.ground.width - 1):
            return None
    elif (dir == "U"):
        new_loc.ypos += 1
        if (new_loc.ypos > w.ground.height - 1):
            return None
    elif (dir == "L"):
        new_loc.xpos -= 1
        if (new_loc.xpos < 0):
            return None
    elif (dir == "D"):
        new_loc.ypos -= 1
        if (new_loc.ypos < 0):
            return None
    
    # checks if new location is occupied
    for item in w.state.values():
        if isinstance(item, object) and item.where == new_loc:
            return None

    # checks if it is possible to move to new location, due to altitude difference
    if abs(w.ground.space[new_loc.xpos][new_loc.ypos] - initialAltitude[ag.name]) > len(ag.objects):
        return None
    
    new_w = copyWorld(w)
    new_ag = new_w.state[ag.name]
    new_ag.where = new_loc
    return(new_w)

# checks if two things are directly adjecent
def isAdjacent(thing1:Thing, thing2:Thing) -> bool:
    if (thing1.where.ypos == thing2.where.ypos):
        if ((thing1.where.xpos+1 == thing2.where.xpos) or (thing1.where.xpos-1 == thing2.where.xpos)):
            return True
    if (thing1.where.xpos == thing2.where.xpos):
        if ((thing1.where.ypos+1 == thing2.where.ypos) or (thing1.where.ypos-1 == thing2.where.ypos)):
            return True
    return False

def pickObject(w:World, ag:Agent, ob:Object) -> World | None:
    if getAltDiff(w, ag, ob) != 0:
        return None
    # if exists and in adjacent to agent, removes object from world and adds it to the agent objects list
    if (ob.name in w.state.keys()) and isAdjacent(ag, ob):
        new_w = copyWorld(w)
        new_w.state[ag.name].objects.append(new_w.state.pop(ob.name))
    else:
        return None
    return(new_w)

Path = tuple[str,]
def pathToWorlds(w:World, path:Path) -> World:
    worlds = [w]
    currWorld = w
    for p in path:
        actions = p.split(" ")
        if len(actions) == 2:
            # checks if command valid
            if not actions[1] in w.state.keys():
                raise(PlayGroundError)
            # executes the action given in path
            currWorld = moveAgent(currWorld, currWorld.state[actions[1]], actions[0])
            # checks if action possible
            if currWorld == None:
                raise(PlayGroundError)
            # appends world post action to list
            worlds.append(currWorld)
        
        elif len(actions) == 3:
            # checks if command valid
            if not actions[2] in w.state.keys():
                raise(PlayGroundError)
            # executes the action given in path
            currWorld = pickObject(currWorld, currWorld.state[actions[1]], currWorld.state[actions[2]])
            # checks if action possible
            if currWorld == None:
                raise(PlayGroundError)
            # appends world post action to list
            worlds.append(currWorld)
    return(worlds)

def nextWorlds(w:World) -> list[tuple[str,World]]:
    possibleWorlds = list()
    for ag in w.state.values():
        if isinstance(ag, Agent):
            possiblePaths = ["U " + ag.name, "D " + ag.name, "L " + ag.name, "R " + ag.name]
            for p in possiblePaths:
                # for all posible actions in one world, appends actions and the the new world to list
                try:
                    nextWorld = pathToWorlds(w, [p])
                    possibleWorlds.append([p, nextWorld])
                except:
                    continue
        for ob in w.state.values():
            # if an object is found and adjacent, picks object
            if isinstance(ob, Object):
                if isAdjacent(ag, ob):
                    nextWorld = pickObject(w, ag, ob)
                    if nextWorld != None:
                        possibleWorlds.append(["P "+ ag.name +" "+ ob.name, nextWorld])
    return possibleWorlds

def findGoal(w:World, goal:Callable[[State],bool]) -> Path:
    # list of tuples that represent locations to visit and the list of paths that got us there
    toVisit: list[tuple[Location, list]] = []
    # grid of booleans that indicates every location that will be visited
    toVisitFlag = [[False for _ in range(0, w.ground.width)] for _ in range(0, w.ground.height)]
    
    # grid of booleans that indicates every location that has been visited
    isVisited = [[False for _ in range(0, w.ground.width)] for _ in range(0, w.ground.height)]
    
    # creates a dictionary of the things in world state where the key is their location
    thingsByLoc = stateToLocDict(w)
    
    w = copyWorld(w)
    
    # for each agent try to move it around to see if the goal is achieved
    for ag in w.state.values():
        if not(isinstance(ag, Agent)):
            continue
        
        start = ag.where
        # set start location as visited and to visit
        toVisit.append((start, []))
        isVisited[start.xpos][start.ypos] = True
        toVisitFlag[start.xpos][start.ypos] = True

        while len (toVisit) > 0:
            # currPos is the location to visit and path is the list of paths that got us here
            currPos, path = toVisit.pop(0)
            # put agent on the location to visit
            ag.where = currPos
            
            if goal(w.state):
                return path
            
            isVisited[currPos.xpos][currPos.ypos] = True

            # try to move the agent in all possible directions
            for dir, nx, ny in [["U",0,1], ["D",0,-1], ["L",-1,0], ["R",1,0]]:

                new_loc = Location(currPos.xpos+nx, currPos.ypos+ny)

                # check if target location contains an object
                foundObject = str(new_loc) in thingsByLoc.keys() and isinstance(thingsByLoc[str(new_loc)], Object)
                
                # if it's possible to move the agent or the target location contains an object save path
                if moveAgent(w, ag, dir) != None or foundObject:
                    # if target location contains an object add path to pick it and to move the agent there
                    if foundObject:
                        newPath = ["P "+ ag.name + " " + thingsByLoc[str(new_loc)].name] + [dir + " " + ag.name]
                    # else, if agent can be moved to target location add path to move it there
                    else:
                        newPath = [dir + " " + ag.name]
                    
                    # if target location was not visited or isn't flagged to visit, add it to the toVisit list
                    if not (isVisited[new_loc.xpos][new_loc.ypos] or toVisitFlag[new_loc.xpos][new_loc.ypos]):
                        toVisit.append((new_loc, path + newPath))
                        toVisitFlag[new_loc.xpos][new_loc.ypos] = True

    raise(PlayGroundError)