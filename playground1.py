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

# criação de entidades básicas ahead
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
 
def matrix(space: LArray, width: int, height: int):
    space = LArray()
    for row in range(width):
        space.insert(row, list())
        for col in range(height):
            space[row].append(0)
    return(space)

def setAltitude(w:World, loc:Location, width:int, heigth:int, alt:int) -> None:
    if (loc.xpos+width > w.ground.width) or (loc.ypos+heigth > w.ground.height):
        raise(PlayGroundError)
    if (loc.xpos < 0) or (loc.ypos < 0):
        raise(PlayGroundError)
    if (alt < 0):
        raise(PlayGroundError)
    for i in range(loc.xpos, loc.xpos+width):
        for j in range(loc.ypos, loc.ypos+heigth):
            w.ground.space[i][j] = alt

initialAltitude = {}
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

def stateToLocDict(w:World) -> dict[str,Thing]:
    dicionario = dict()
    for val in w.state.values():
        dicionario[str(val.where)] = val
    return dicionario
    
def printWorld(w:World):
    loc_dicionario = x(w)
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

def copyWorld(src:World) -> World:
    w = World(src.ground, (deepcopy(src.state)))
    #w.state = deepcopy(src.state)
    '''for thing in w.state.values():
        if isinstance(thing, Agent):
            agent = newAgent(thing.name)
            agent.where = Location(thing.where.xpos, thing.where.ypos)
            w.state[agent.name] = agent
            w.state[agent.name].where = agent.where
            for agOb in thing.objects:
                w.state[agent.name].objects = agOb
        if isinstance(thing, Object):
            object = newObject(thing.name)
            object.where = Location(thing.where.xpos, thing.where.ypos)
            w.state[object.name] = object
            w.state[object.name] = object.where'''
    return(w)

def getAltDiff(w:World, th1:Thing, th2:Thing) -> int:
    return abs((w.ground.space[th1.where.xpos][th1.where.ypos]) - (w.ground.space[th2.where.xpos][th2.where.ypos]))

def moveAgent(w:World, ag:Agent, dir:str) -> World | None:
    new_loc = Location(ag.where.xpos, ag.where.ypos)
    if (dir == "L"):
        new_loc.xpos -= 1
        if (new_loc.xpos < 0):
            return None
    elif (dir == "R"):
        new_loc.xpos += 1
        if (new_loc.xpos > w.ground.width - 1):
            return None
    elif (dir == "U"):
        new_loc.ypos += 1
        if (new_loc.ypos > w.ground.height - 1):
            return None
    elif (dir == "D"):
        new_loc.ypos -= 1
        if (new_loc.ypos < 0):
            return None
    
    for item in w.state.values():
        if isinstance(item, object) and item.where == new_loc:
            return None
    
    if abs(w.ground.space[new_loc.xpos][new_loc.ypos] - initialAltitude[ag.name]) > len(ag.objects):
        return None
    
    new_w = copyWorld(w)
    new_ag = new_w.state[ag.name]
    new_ag.where = new_loc
    return(new_w)

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
            currWorld = moveAgent(currWorld, currWorld.state[actions[1]], actions[0])
            # checks if action possible
            if currWorld == None:
                raise(PlayGroundError)
            worlds.append(currWorld)
        
        elif len(actions) == 3:
            # checks if command valid
            if not actions[2] in w.state.keys():
                raise(PlayGroundError)
            currWorld = pickObject(currWorld, currWorld.state[actions[1]], currWorld.state[actions[2]])
            # checks if action possible
            if currWorld == None:
                raise(PlayGroundError)
            worlds.append(currWorld)
    return(worlds)

def nextWorlds(w:World) -> list[tuple[str,World]]:
    possibleWorlds = list()
    for ag in w.state.values():
        if isinstance(ag, Agent):
            possiblePaths = ["U " + ag.name, "D " + ag.name, "L " + ag.name, "R " + ag.name]
            for p in possiblePaths:
                try:
                    nWorld = pathToWorlds(w, [p])
                    possibleWorlds.append([p, nWorld])
                except:
                    continue
        for ob in w.state.values():
            if isinstance(ob, Object):
                if isAdjacent(ag, ob):
                    nWorld = pickObject(w, ag, ob)
                    if nWorld != None:
                        possibleWorlds.append(["P "+ ag.name +" "+ ob.name, nWorld])
    return possibleWorlds

def findGoal(w:World, goal:Callable[[State],bool]) -> Path:
    toVisit: list[tuple[Location, list]] = []
    distance:dict[str, int] = {}
    isVisited = [[False for _ in range(0, w.ground.width)] for _ in range(0, w.ground.height)]
    toVisitFlag = [[False for _ in range(0, w.ground.width)] for _ in range(0, w.ground.height)]
    thingsByLoc = stateToLocDict(w)
    
    w = copyWorld(w)
    
    for ag in w.state.values():
        if isinstance(ag, Agent):
            start = ag.where
    
        toVisit.append((start, []))
        distance [str(start)] = 0
        isVisited[start.xpos][start.ypos] = True
        toVisitFlag[start.xpos][start.ypos] = True

        while len (toVisit) > 0:
            tv, path = toVisit.pop(0)
            ag.where = tv
            
            if goal(w.state):
                return path
            isVisited[tv.xpos][tv.ypos] = True
        
            for dir, nx, ny in [["U",0,1], ["D",0,-1], ["L",-1,0], ["R",1,0]]:
                new_loc = Location(tv.xpos+nx, tv.ypos+ny)
                foundObject = str(new_loc) in thingsByLoc.keys() and isinstance(thingsByLoc[str(new_loc)], Object)
                if moveAgent(w, ag, dir) != None or foundObject:
                    if foundObject:
                        newPath = ["P "+ ag.name + " " + thingsByLoc[str(new_loc)].name] + [dir + " " + ag.name]
                    else:
                        newPath = [dir + " " + ag.name]
                    if not (isVisited[new_loc.xpos][new_loc.ypos] or toVisitFlag[new_loc.xpos][new_loc.ypos]):
                        toVisit.append((new_loc, path + newPath))
                        toVisitFlag[new_loc.xpos][new_loc.ypos] = True
                        distance[str(new_loc)] = distance[str(tv)]+1

    raise(PlayGroundError)