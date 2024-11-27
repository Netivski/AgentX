from dataclasses import dataclass, field

LArray = list[list[int]]

@dataclass
class Ground:        
    def __init__(self, name:str, width:int, height:int):
        self.name = name
        self.width = width
        self.height = height
        self.space = LArray()
        for row in range(0, height):
            self.space.insert(row, list())
            for col in range(0, width):
                self.space[row].append(0)

@dataclass
class Location:
    xpos: int
    ypos: int

@dataclass
class Object:
    name: str
    where: Location

@dataclass
class Agent(Object):
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
    if (not name.isascii()) or (width < 0 or width > 50) or (height < 0 or height > 50):
        raise PlayGroundError
    return World(Ground(name, width, height), None)

def setAltitude (w:World, loc: Location, width:int, height:int, alt:int)->None:
    if (loc.xpos+width > len(w.ground.space[0])) or (loc.ypos+height > len(w.ground.space)):
        raise PlayGroundError
    if (alt < 0):
        raise PlayGroundError
    for i in range(loc.ypos, loc.ypos+height):
        for j in range(loc.xpos, loc.xpos+width):
            w.ground.space[i][j] = alt

def putThing (w:World, thing:Thing, loc:Location)-> Thing:
    if (loc in w.state.keys()):
        raise PlayGroundError
    w.state[loc] = thing
    return thing

#def moveAgent (w:World, ag:Agent,dir:str)-> World|None:
#def pickObject (w:World, ag: Agent , ob: Object)->World|None:

#def pathToWorlds (w:World, path: Path) -> list [World]: 
#def findGoal (w:World, goal:Callable [[State],bool])->Path:

def PrintWorld(w: World):
    for row in range(len(w.ground.space), 0, -1):
        print (w.ground.space[row-1])
    

w = newWorld("Earth",5, 5)
setAltitude(w, Location(0, 0), 3, 3, 9)
PrintWorld(w)