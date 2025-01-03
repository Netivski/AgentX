from dataclasses import dataclass, field
from typing import Callable
from collections import deque

LArray = list[list[int]]

MAX_WIDTH = 50
MAX_HEIGHT = 50

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
    if (checkAltDiff(w, newLocation, ag.initialLocation) > (len(ag.objects))):
        return None
    
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
            for key in directions.keys():
                nx, ny = x + directions[key].xpos, y + directions[key].ypos
                newLoc = Location(nx, ny)
                if isValidMove(newWorld, ag, newLoc, visited):
                    visited[nx][ny] = True  # Mark the neighbor as visited

                    # Check to see if there's an Object in the neighbor cell
                    if(str(newLoc) in stateByLoc.keys()) and (isinstance(stateByLoc[str(newLoc)], Object)):
                        # Path to add should instruct agent to pick object and then move 
                        pathToAdd = ["P " + ag.name + " " + stateByLoc[str(newLoc)].name] + [key + " " + ag.name]
                    else:
                        # Path to add should instruct agent to move 
                        pathToAdd = [key + " " + ag.name]
                    queue.append((nx, ny, distance + 1, path + pathToAdd))  # Enqueue the neighbor with updated distance and path
        
        # If no path is found, raise exception
        raise PlayGroundError()

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
    
'''
Testing area
'''

# w:World = newWorld("S",6,6)
# setAltitude(w,Location(1,1),2,1,3)
# print(w.ground.space)
# PrintWorld(w)

# a = newAgent("Ze")
# b = newAgent("Quim")
# o = newObject("Maria")

# putThing(w, a, Location(2,3))
# putThing(w, b, Location(0,0))
# putThing(w, o, Location(1,1))


# PrintWorld(w)
# if (pickObject(w, b, o) == None):
#     print("Nothing to pick!")
# PrintWorld(w)
# moveAgent(w, b, "U")
# PrintWorld(w)
# if (pickObject(w, b, o) != None):
#     print("Picked something!")
# PrintWorld(w)

# #exit(0)
# for i in range(0,6):
#     moveAgent(w, b, "U")
#     moveAgent(w, b, "R")
#     PrintWorld(w)


# x = Location(2,3)
# print (x)

# def g1(s:State)->bool:
#     return s["R2D2"].where == Location(2,2)

# w = newWorld("Playground",20,20)
# robot1 = newAgent("R3D3")
# robot = newAgent("R2D2")
# putThing(w,robot1,Location(2,2))
# putThing(w,robot,Location(0,0))
# res = findGoal(w,g1)
# print(res)