from playground1 import *
import unittest
from typing import *

class newObjectTests(unittest.TestCase):
    def test_new_object_1(self):
        ob = newObject("key")
        self.assertIsNotNone(ob)
        self.assertIsInstance(ob, Object)
        self.assertIsInstance(ob.name, str)
        self.assertEqual(ob.name, "key")
        self.assertIsInstance(ob.where, Location)
        self.assertEqual(ob.where.xpos, 0)
        self.assertEqual(ob.where.ypos, 0)

    def test_new_object_2(self):
        try:
            ag = newObject("__!__")
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_new_object_3(self):
        ob = newObject("big_box")
        self.assertIsNotNone(ob)
        self.assertIsInstance(ob, Object)
        self.assertIsInstance(ob.name, str)
        self.assertEqual(ob.name, "big_box")
        self.assertEqual(ob.where.xpos, 0)
        self.assertEqual(ob.where.ypos, 0)
        self.assertIsInstance(ob.where, Location)

class newAgentTests(unittest.TestCase):
    def test_new_agent_1(self):
        ag = newAgent("robot")
        self.assertIsNotNone(ag)
        self.assertIsInstance(ag, Agent)
        self.assertIsInstance(ag.name, str)
        self.assertEqual(ag.name, "robot")
        self.assertIsInstance(ag.where, Location)
        self.assertEqual(ag.where.xpos, 0)
        self.assertEqual(ag.where.ypos, 0)
        self.assertEqual(ag.objects, [])

    def test_new_agent_2(self):
        ag = newAgent("2A__robotx")
        self.assertIsNotNone(ag)
        self.assertIsInstance(ag, Agent)
        self.assertIsInstance(ag.name, str)
        self.assertEqual(ag.name,"2A__robotx")
        self.assertIsInstance(ag.where, Location)
        self.assertEqual(ag.where.xpos, 0)
        self.assertEqual(ag.where.ypos, 0)
        self.assertEqual(ag.objects, [])

    def test_new_agent_3(self):
        try:
            ag = newAgent("2robot$x")
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

def oklist(g:Ground,w:int,h:int)->bool:
    if (w!=g.width or h!=g.height):
        return False
    l = g.space
    if type(l)!=list:
        return False
    if len(l)==g.width:
        for i in range(len(l)):
            if len(l[i])!=g.height:
                return False
            if type(l[i])!=list:
                return False
            for j in range(len(l[i])):
                if l[i][j]!=0:
                    return False
    else:
        return False   
    return True

class newWorldTests(unittest.TestCase):

    def test_new_world_0(self):
        n ="playG0"
        w = newWorld(n,1,1)
        self.assertIsNotNone(w)
        self.assertIsInstance(w,World)
        self.assertEqual(n, w.ground.name)
        self.assertEqual(w.state, {})
        self.assertTrue(oklist(w.ground,1,1))

    def test_new_world_1(self):
        n = "playG2"
        w = newWorld(n,10,10)
        self.assertIsNotNone(w)
        self.assertIsInstance(w,World)
        self.assertEqual(w.state, {})
        self.assertEqual(n, w.ground.name)
        self.assertTrue(oklist(w.ground,10,10))

    def test_world_world_2(self):
        try:
            ag = newWorld("pZ?buggy",0,0)
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_world_world_3(self):
        try:
            ag = newWorld("playG3",-1,0)
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_world_world_4(self):
        try:
            ag = newWorld("playG4",0,0)
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_world_world_5(self):
        try:
            ag = newWorld("playG5",0,-2)
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_world_world_6(self):
        try:
            ag = newWorld("",10,10)
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')
        
class newSetAltitude(unittest.TestCase):

    def test_setAltitude_0(self)->None:
        n ="playG0"
        w:World = newWorld(n,2,2)
        setAltitude(w,Location(0,0),1,1,0)
        t = [[0,0],[0,0]]
        self.assertTrue(w.ground.space==t)

    def test_setAltitude_1(self)->None:
        n ="playG0"
        w:World = newWorld(n,2,2)
        setAltitude(w,Location(0,0),1,1,1)
        t = [[1,0],[0,0]]
        self.assertTrue(w.ground.space==t)

    def test_setAltitude_2(self)->None:
        n ="playG0"
        w:World = newWorld(n,2,2)
        setAltitude(w,Location(1,1),1,1,2)
        t = [[0,0],[0,2]]
        self.assertTrue(w.ground.space==t)

    def test_setAltitude_3(self)->None:
        n ="playG0"
        w:World = newWorld(n,3,3)
        setAltitude(w,Location(1,1),2,1,3)
        t = [[0,0,0],[0,3,0],[0,3,0]] 
        self.assertTrue(w.ground.space==t)
        
        '''
        w = |0 0 0|   expected = |0 0 0|  
            |0 3 3|              |0 3 0|
            |0 0 0|              |0 3 0|
        '''

    def test_setAltitude_4(self)->None:
        n ="playG0"
        w:World = newWorld(n,3,3)
        try:
            setAltitude(w,Location(3,3),2,1,3)
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_setAltitude_5(self)->None:
        n ="playG0"
        w:World = newWorld(n,3,3)
        try:
            setAltitude(w,Location(-1,0),1,1,3)
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_setAltitude_6(self)->None:
        n ="playG0"
        w:World = newWorld(n,3,3)
        try:
            setAltitude(w,Location(2,-2),1,1,3)
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_setAltitude_7(self)->None:
        n ="playG0"
        w:World = newWorld(n,3,3)
        try:
            setAltitude(w,Location(0,0),5,1,3)
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_setAltitude_8(self)->None:
        n ="playG0"
        w:World = newWorld(n,3,3)
        try:
            setAltitude(w,Location(0,0),1,4,3)
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_setAltitude_9(self)->None:
        w = newWorld("Playground",20,20)
        setAltitude(w,Location(1,0),2,17,1) 
        setAltitude(w,Location(6,4),10,5,2) 
        setAltitude(w,Location(10,10),4,6,1)
        setAltitude(w,Location(11,0),2,18,0)
        setAltitude(w,Location(0,10),18,1,0)
        setAltitude(w,Location(0,0),1,4,3)
        sp = w.ground.space
        self.assertEqual(sp[1][0],1)
        self.assertEqual(sp[0][0],3)
        self.assertEqual(sp[12][1],0)
        self.assertEqual(sp[10][5],2)
        self.assertEqual(sp[2][14],1)
        self.assertEqual(sp[9][4],2)

    def test_setAltitude_10(self)->None:
        w1 = newWorld("Playground2",7,7)
        sp = w1.ground.space
        setAltitude(w1,Location(2,2),2,2,4)  
        self.assertEqual(sp[0][0],0)
        self.assertEqual(sp[3][3],4)

class putThingTests(unittest.TestCase):

    def test_putthing_0(self):
        n ="playG0"
        w = newWorld(n,10,10)
        ag = newAgent("rob")
        th = putThing(w,ag,Location(0,0))
        self.assertEqual(th,ag)

    def test_putthing_1(self):
        n ="playG0"
        w = newWorld(n,10,10)
        ag = newAgent("rob")
        ob = newObject("ob")
        try:
            _ = putThing(w,ag,Location(9,1))
            _ = putThing(w,ob,Location(9,1))
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_putthing_12(self):
        n ="playG0"
        w = newWorld(n,20,20)
        ag = newAgent("rob")
        ob = newObject("ob")
        setAltitude(w,Location(2,2),2,2,4)  
        agn=putThing(w,ag,Location(9,1))
        obn=putThing(w,ob,Location(0,0))
        self.assertEqual(ag.where,Location(9,1))
        self.assertEqual(ag.name,"rob")
        self.assertEqual(ag.objects,[])
        self.assertEqual(ob,obn)

    def test_putthing_2(self):
        n ="playG0"
        w = newWorld(n,10,10)
        ag = newAgent("rob")
        ob = newObject("rob")
        try:
            putThing(w,ag,Location(1,1))
            putThing(w,ob,Location(1,0))
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_putthing_3(self):
        n ="playG0"
        w = newWorld(n,5,5)
        ag = newAgent("rob")
        ob = newObject("ob")
        l1 = Location(1,1)
        self.assertEqual("rob" in w.state,False)
        putThing(w,ag,l1)
        putThing(w,ob,Location(1,0))
        self.assertEqual("rob" in w.state,True)
        self.assertEqual(w.state["rob"].name,"rob")
        self.assertEqual(w.state["rob"].where,l1)
        self.assertEqual(w.state["rob"].objects,[])

    def test_putthing_4(self):
        n ="playG0"
        w = newWorld(n,5,5)
        for i in range(5):
            for j in range(5):
                if (i+j)%2 == 0:
                    th = newAgent("rob"+str(i)+str(j))
                else:
                    th = newObject("rob"+str(i)+str(j))
                putThing(w,th,Location(i,j))

def getAgent(w:World,n:str)->Agent:
    return cast(Agent,w.state[n])

def getObject(w:World,n:str)->Object:
    return cast(Object,w.state[n])

class moveAgentTests(unittest.TestCase):

    def test_move_0(self):
        n ="playGMove"
        w = newWorld(n,10,10)
        ag = newAgent("rob")
        th = putThing(w,ag,Location(0,0))
        wn=moveAgent(w,ag,"R")
        self.assertEqual(ag.where,Location(0,0))
        self.assertEqual(getAgent(wn,ag.name).where,Location(1,0))
        wn=moveAgent(wn,getAgent(wn,ag.name),"U")
        wn=moveAgent(wn,getAgent(wn,ag.name),"R")
        self.assertEqual(getAgent(wn,ag.name).where,Location(2,1))

    def test_move_1(self):
        n ="playGMove"
        w = newWorld(n,10,10)
        ag = newAgent("rob")
        th = putThing(w,ag,Location(0,0))
        wn=moveAgent(w,ag,"L")
        self.assertEqual(wn,None)
        wn=moveAgent(w,ag,"D")
        self.assertEqual(wn,None)
        wn=moveAgent(w,ag,"U")
        self.assertEqual(getAgent(wn,"rob").where,Location(0,1))
        self.assertEqual(getAgent(w,"rob").where,Location(0,0))

    def test_move_2(self):
        n ="playGMove"
        w = newWorld(n,10,10)
        ag = newAgent("x")
        l = 2
        th = putThing(w,ag,Location(l,l))
        for _ in range(9-l):
            w = moveAgent(w,getAgent(w,"x"),"U")
            w = moveAgent(w,getAgent(w,"x"),"R")
        getAgent(w,"x").where=Location(9,9)

    def test_move_2a(self):
        n ="playGMove"
        w = newWorld(n,10,10)
        ag = newAgent("x")
        l = 4
        th = putThing(w,ag,Location(l,l))
        for _ in range(9-l):
            w = moveAgent(w,getAgent(w,"x"),"U")
            w = moveAgent(w,getAgent(w,"x"),"R")
        getAgent(w,"x").where=Location(9,9)

    def test_move_3(self):
        n ="playGMove"
        w = newWorld(n,10,10)
        setAltitude(w,Location(0,1),1,1,1)
        ag = newAgent("rob")
        l = 3
        th = putThing(w,ag,Location(l,l))
        for _ in range(l):
            w = moveAgent(w,getAgent(w,"rob"),"D")
            w = moveAgent(w,getAgent(w,"rob"),"L")
        getAgent(w,"rob").where=Location(0,0)

    def test_move_3a(self):
        n ="playGMove"
        w = newWorld(n,10,10)
        setAltitude(w,Location(0,1),1,1,1)
        ag = newAgent("rob")
        l = 8
        th = putThing(w,ag,Location(l,l))
        for _ in range(l):
            w = moveAgent(w,getAgent(w,"rob"),"D")
            w = moveAgent(w,getAgent(w,"rob"),"L")
        getAgent(w,"rob").where=Location(0,0)

class pickObjectTests(unittest.TestCase):

    def test_pick_0(self)->None:
        n ="playGPick"
        w = newWorld(n,10,10)
        ag = newAgent("rob")
        ob = newObject("key")
        th1 = putThing(w,ag,Location(0,0))
        th2 = putThing(w,ob,Location(2,0))
        wn=pickObject(w,getAgent(w,"rob"),getObject(w,"key"))
        self.assertEqual(wn,None)

    def test_pick_1(self)->None:
        n ="playGPick"
        w = newWorld(n,4,4)
        x,y = 2,1
        ag = newAgent("rob")
        ob = newObject("key")
        th1 = putThing(w,ag,Location(x,y))
        th2 = putThing(w,ob,Location(x+1,y))
        wn=pickObject(w,getAgent(w,"rob"),getObject(w,"key"))
        self.assertNotEqual(wn,None)
        if(type(wn)==World):
            self.assertNotEqual(wn,None)
            self.assertEqual(len(wn.state),1)
            obs=getAgent(wn,"rob").objects[0]
            self.assertEqual(type(obs),Object)
            self.assertEqual(obs.name,"key")

    def test_pick_2(self)->None:
        n ="playGPick"
        w = newWorld(n,4,4)
        x,y = 0,2
        ag = newAgent("rob")
        ob = newObject("key")
        th1 = putThing(w,ag,Location(x,y))
        th2 = putThing(w,ob,Location(x,y+1))
        wn=pickObject(w,getAgent(w,"rob"),getObject(w,"key"))
        self.assertNotEqual(wn,None)
        if(type(wn)==World):
            self.assertNotEqual(wn,None)
            self.assertEqual(len(wn.state),1)
            obs=getAgent(wn,"rob").objects[0]
            self.assertEqual(type(obs),Object)
            self.assertEqual(obs.name,"key")

    def test_pick_3(self)->None:
        n ="playGPick"
        w = newWorld(n,4,4)
        (x,y) = 2,2
        ag = newAgent("rob")
        ob = newObject("key")
        th1 = putThing(w,ag,Location(x,y))
        th2 = putThing(w,ob,Location(x-1,y))
        wn=pickObject(w,getAgent(w,"rob"),getObject(w,"key"))
        self.assertNotEqual(wn,None)
        if(type(wn)==World):
            self.assertNotEqual(wn,None)
            self.assertEqual(len(wn.state),1)
            obs=getAgent(wn,"rob").objects[0]
            self.assertEqual(type(obs),Object)
            self.assertEqual(obs.name,"key")

    def test_pick_4(self)->None:
        n ="playGPick"
        w = newWorld(n,4,4)
        x,y = 1,2
        ag = newAgent("rob")
        ob = newObject("key")
        th1 = putThing(w,ag,Location(x,y))
        th2 = putThing(w,ob,Location(x,y-1))
        wn=pickObject(w,getAgent(w,"rob"),getObject(w,"key"))
        self.assertNotEqual(wn,None)
        if(type(wn)==World):
            self.assertNotEqual(wn,None)
            self.assertEqual(len(wn.state),1)
            obs=getAgent(wn,"rob").objects[0]
            self.assertEqual(type(obs),Object)
            self.assertEqual(obs.name,"key")

    def test_pick_5(self)->None:
        n ="playGPick"
        w = newWorld(n,4,4)
        ag = newAgent("rob")
        ob = newObject("key")
        th1 = putThing(w,ag,Location(0,0))
        th2 = putThing(w,ob,Location(1,1))
        wn=pickObject(w,getAgent(w,"rob"),getObject(w,"key"))
        self.assertEqual(wn,None)

    def test_pick_6(self)->None:
        n ="playGPick"
        w = newWorld(n,10,10)
        setAltitude(w,Location(1,0),2,2,0)
        ag = newAgent("rob")
        ob = newObject("key")
        th1 = putThing(w,ag,Location(0,0))
        th2 = putThing(w,ob,Location(1,0))
        wn=pickObject(w,getAgent(w,"rob"),getObject(w,"key"))
        self.assertNotEqual(wn,None)

    def test_pick_7(self)->None:
        n ="playGPick"
        w = newWorld(n,4,4)
        setAltitude(w,Location(1,0),2,2,1)
        ag = newAgent("rob")
        ob = newObject("key")
        th1 = putThing(w,ag,Location(0,0))
        th2 = putThing(w,ob,Location(1,0))
        wn=pickObject(w,getAgent(w,"rob"),getObject(w,"key"))
        self.assertEqual(wn,None)

class PTWTests(unittest.TestCase):

    def test_ptw_0(self)->None:
        n ="playGPTW"
        w = newWorld(n,10,10)
        ag = newAgent("rob")
        ob = newObject("key")
        setAltitude(w,Location(0,1),1,1,1)
        th1 = putThing(w,ag,Location(0,0))
        th2 = putThing(w,ob,Location(2,0))
        wf = pathToWorlds(w,("R rob","P rob key","U rob","L rob"))

    def test_ptw_1(self)->None:
        n ="playGPTW"
        w = newWorld(n,10,10)
        ag = newAgent("rob")
        ob = newObject("key")
        th1 = putThing(w,ag,Location(0,0))
        th2 = putThing(w,ob,Location(2,0))
        wl = pathToWorlds(w,("R rob","U rob","R rob","P rob key"))

    def test_ptw_2(self)->None:
        n ="playGPTW"
        w = newWorld(n,10,10)
        ag = newAgent("rob")
        ob = newObject("key")
        th1 = putThing(w,ag,Location(0,0))
        th2 = putThing(w,ob,Location(2,0))
        wl = pathToWorlds(w,("R rob","U rob","R rob","P rob key","L rob"))

    def test_ptw_3(self)->None:
        n ="playGPTW"
        w = newWorld(n,10,10)
        ag = newAgent("rob")
        ob = newObject("key")
        th1 = putThing(w,ag,Location(0,0))
        th2 = putThing(w,ob,Location(2,0))
        try:
            wl = pathToWorlds(w,("R robx",))
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_ptw_4(self)->None:
        n ="playGPTW"
        w = newWorld(n,10,10)
        ag = newAgent("rob")
        ob = newObject("key")
        th1 = putThing(w,ag,Location(0,0))
        th2 = putThing(w,ob,Location(2,0))
        try:
           wl = pathToWorlds(w,("R rob","U rob","R rob","P rob no"))
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_ptw_5(self)->None:
        w1 = newWorld("Playground2",10,10)
        robot1 = newAgent("robot1")
        putThing(w1,robot1,Location(0,0))
        robot2 = newAgent("robot2")
        putThing(w1,robot2,Location(0,4))
        box0 = newObject("box0")
        putThing(w1,box0,Location(3,4))
        setAltitude(w1,Location(3,4),1,1,1)
        box1 = newObject("box1")
        putThing(w1,box1,Location(2,2))
        box2 = newObject("box2")
        putThing(w1,box2,Location(3,0))
        pl = ('U robot1', 'R robot1', 'R robot1', 'R robot1', 'P robot1 box2')
        wl = pathToWorlds(w1,pl)

    def test_ptw_60(self)->None:
        w2:World= newWorld("ToyPlayGround",6,6)
        robot:Agent = newAgent("Mary")
        putThing(w2,robot,Location(0,0))
        box0:Object = newObject("Key")
        putThing(w2,box0,Location(5,5))
        box1:Object = newObject("Ball")
        putThing(w2,box1,Location(4,1))
        setAltitude(w2,Location(2,2),2,2,4)
        pl:list[tuple[str,...]]=[()]*6
        pl[0] = ('R Mary', 'R Mary', 'R Mary', 'R Mary', 'R Mary', 'U Mary', 'U Mary', 'U Mary', 'U Mary', 'P Mary Key', 'U Mary')
        pl[1] = ('U Mary', 'R Mary', 'U Mary', 'U Mary', 'U Mary', 'U Mary', 'R Mary', 'R Mary', 'R Mary', 'P Mary Key', 'R Mary')
        pl[2] = ('U Mary', 'U Mary', 'R Mary', 'U Mary', 'U Mary', 'R Mary', 'R Mary', 'U Mary', 'R Mary', 'P Mary Key', 'R Mary')
        for i in range(3):
            wl = pathToWorlds(w2,pl[i])

    def test_ptw_6(self)->None:
        w1 = newWorld("Playground2",10,10)
        robot1 = newAgent("robot1")
        putThing(w1,robot1,Location(0,0))
        robot2 = newAgent("robot2")
        putThing(w1,robot2,Location(0,4))
        box0 = newObject("box0")
        putThing(w1,box0,Location(3,4))
        setAltitude(w1,Location(3,4),1,1,1)
        box1 = newObject("box1")
        putThing(w1,box1,Location(2,2))
        box2 = newObject("box2")
        putThing(w1,box2,Location(3,0))
        pl = ('U robot1', 'R robot1', 'R robot1', 'R robot1', 'P robot1 box2',\
               'U robot1', 'U robot1', 'R robot1', 'U robot1', 'U robot1', \
                'U robot1', 'U robot1', 'U robot1', 'U robot1', 'R robot1', \
                    'R robot1', 'R robot1', 'D robot2','R robot2','R robot1', 'R robot1', \
                           'R robot2', 'P robot2 box1', 'U robot2', \
                            'U robot2', 'U robot2', 'U robot2', 'U robot2', \
                                'U robot2', 'R robot2', 'R robot2', 'R robot2', \
                                    'R robot2', 'R robot2', 'R robot2')
        wl = pathToWorlds(w1,pl)

    def test_ptw_7(self)->None:
        w1 = newWorld("Playground2",10,10)
        robot1 = newAgent("robot1")
        putThing(w1,robot1,Location(0,0))
        robot2 = newAgent("robot2")
        putThing(w1,robot2,Location(0,4))
        box0 = newObject("box0")
        putThing(w1,box0,Location(3,4))
        setAltitude(w1,Location(3,4),1,1,1)
        box1 = newObject("box1")
        putThing(w1,box1,Location(2,2))
        box2 = newObject("box2")
        putThing(w1,box2,Location(3,0))
        pl = ('R robot2', 'R robot1', 'U robot1', 'R robot2', \
              'D robot2', 'R robot1', 'P robot2 box1', \
                'R robot1', 'R robot2', 'P robot1 box2', 'R robot1', \
                    'U robot1', 'R robot1', 'U robot1', 'R robot2', \
                        'U robot2', 'U robot1', 'R robot1', 'R robot1',\
                              'U robot1', 'U robot2', 'R robot2', \
                                'U robot2', 'R robot1', 'R robot2',\
                                      'U robot2', 'R robot2', 'U robot1',\
                                          'U robot2', 'R robot1', 'R robot2', \
                                            'U robot1', 'U robot1', 'U robot1', \
                                                'U robot2')

        wl = pathToWorlds(w1,pl)

    def test_ptw_8(self)->None:
        w1 = newWorld("Ladder",5,5)
        setAltitude(w1,Location(1,0),4,5,1)
        setAltitude(w1,Location(2,0),3,5,2)
        setAltitude(w1,Location(3,0),2,5,3)
        robot1 = newAgent("rob")
        putThing(w1,robot1,Location(0,0))
        box0 = newObject("box0")
        putThing(w1,box0,Location(0,1))
        box1 = newObject("box1")
        putThing(w1,box1,Location(1,1))
        box2 = newObject("box2")
        putThing(w1,box2,Location(2,1))
        pa = ('P rob box0','R rob','P rob box1',\
              'R rob','P rob box2','R rob','R rob',\
                'U rob','L rob')
        wl = pathToWorlds(w1,pa)

    def test_ptw_9(self)->None:
        w1 = newWorld("Ladder",5,5)
        setAltitude(w1,Location(0,0),5,5,4)
        setAltitude(w1,Location(1,0),4,5,3)
        setAltitude(w1,Location(2,0),3,5,2)
        setAltitude(w1,Location(3,0),2,5,1)
        robot1 = newAgent("rob")
        putThing(w1,robot1,Location(0,0))
        box0 = newObject("box0")
        putThing(w1,box0,Location(0,1))
        box1 = newObject("box1")
        putThing(w1,box1,Location(1,1))
        box2 = newObject("box2")
        putThing(w1,box2,Location(2,1))
        pa = ('P rob box0','R rob','P rob box1','R rob','P rob box2','U rob',\
              'L rob','L rob','D rob')
        wl = pathToWorlds(w1,pa)

    def test_ptw_10(self)->None:
        w1 = newWorld("Ladder",5,5)
        setAltitude(w1,Location(0,0),5,5,4)
        setAltitude(w1,Location(1,0),4,5,3)
        setAltitude(w1,Location(2,0),3,5,2)
        setAltitude(w1,Location(3,0),2,5,1)
        robot1 = newAgent("rob")
        putThing(w1,robot1,Location(0,0))
        box0 = newObject("box0")
        putThing(w1,box0,Location(0,1))
        box1 = newObject("box1")
        putThing(w1,box1,Location(1,1))
        box2 = newObject("box2")
        putThing(w1,box2,Location(2,1))
        pa = ('P rob box0','R rob','U rob')
        try:
            wl = pathToWorlds(w1,pa)
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_ptw_11(self)->None:
        w1 = newWorld("Ladder",5,5)
        setAltitude(w1,Location(0,0),5,5,4)
        setAltitude(w1,Location(1,0),4,5,3)
        setAltitude(w1,Location(2,0),3,5,2)
        setAltitude(w1,Location(3,0),2,5,1)
        robot1 = newAgent("rob")
        putThing(w1,robot1,Location(0,0))
        box0 = newObject("bix0")
        putThing(w1,box0,Location(0,1))
        box1 = newObject("bix1")
        putThing(w1,box1,Location(1,1))
        box2 = newObject("bix2")
        putThing(w1,box2,Location(2,1))
        pa = ('P rob bix0','U rob','P rob bix1')
        try:
            wl = pathToWorlds(w1,pa)
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_ptw_12(self)->None:
        w1 = newWorld("Ladder",5,5)
        setAltitude(w1,Location(0,0),5,5,4)
        setAltitude(w1,Location(1,0),4,5,3)
        setAltitude(w1,Location(2,0),3,5,2)
        setAltitude(w1,Location(3,0),2,5,1)
        robot1 = newAgent("rob")
        putThing(w1,robot1,Location(0,0))
        box0 = newObject("bix0")
        putThing(w1,box0,Location(0,1))
        box1 = newObject("bix1")
        putThing(w1,box1,Location(1,1))
        box2 = newObject("bix2")
        putThing(w1,box2,Location(2,1))
        pa = ('P rob bix0','R rob','P rob bix1','R rob','R rob')
        try:
            wl = pathToWorlds(w1,pa)
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

def g0(s:State)->bool:
    return s["R2D2"].where == Location(0,0)

def g1(s:State)->bool:
    return s["R2D2"].where == Location(2,2)

def g2(s:State)->bool:
    return s["R2D2"].where == Location(10,10)

def g3(s:State)->bool:
    return s["R2D2"].where == Location(7,7)

def gi(s:State)->bool:
    return s["R2D2"].where == Location(70,70)


class PFGTests(unittest.TestCase):

    def test_fg_0(self) -> None:
        w = newWorld("Playground",20,20)
        robot = newAgent("R2D2")
        putThing(w,robot,Location(0,0))
        res = findGoal(w,g1)
        self.assertEqual(len(res),4)
        lw=pathToWorlds(w,res)
        self.assertEqual(g1(lw[-1].state),True)

    def test_fg_00(self) -> None:
        w = newWorld("Playground",20,20)
        robot = newAgent("R2D2")
        putThing(w,robot,Location(0,0))
        res = findGoal(w,g0)
        self.assertEqual(len(res),0)
        lw=pathToWorlds(w,res)
        self.assertEqual(g0(lw[0].state),True)

    def test_fg_1(self) -> None:
        w = newWorld("Playground",20,20)
        robot = newAgent("R2D2")
        setAltitude(w,Location(0,0),1,1,1)
        putThing(w,robot,Location(0,0))
        try:
            res = findGoal(w,g1)
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_fg_11(self) -> None:
        w = newWorld("Playground",20,20)
        robot = newAgent("R2D2")
        putThing(w,robot,Location(0,0))
        try:
            res = findGoal(w,gi)
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_fg_2(self) -> None:
        w = newWorld("Playground",20,20)
        robot = newAgent("R2D2")
        putThing(w,robot,Location(0,0))
        res = findGoal(w,g2)
        self.assertEqual(len(res),20)
        lw=pathToWorlds(w,res)
        self.assertEqual(g2(lw[-1].state),True)

    def test_fg_3(self) -> None:
        w = newWorld("Playground",20,20)
        setAltitude(w,Location(2,0),4,17,1)
        robot = newAgent("R2D2")
        putThing(w,robot,Location(0,0))
        res = findGoal(w,g2)
        self.assertEqual(len(res),34)
        lw=pathToWorlds(w,res)
        self.assertEqual(g2(lw[-1].state),True)

    def test_fg_4(self) -> None:
        w = newWorld("Playground",8,8)
        setAltitude(w,Location(2,0),4,6,1)
        robot = newAgent("R2D2")
        putThing(w,robot,Location(0,0))
        res = findGoal(w,g3)
        self.assertEqual(len(res),14)
        lw=pathToWorlds(w,res)
        self.assertEqual(g3(lw[-1].state),True)

    def test_fg_5(self) -> None:
        w = newWorld("Playground",20,20)
        robot = newAgent("R2D2")
        putThing(w,robot,Location(0,0))
        res = findGoal(w,g0)
        self.assertEqual(len(res),0)

    def test_fg_6(self) -> None:
        w = newWorld("Playground",20,20)
        robot = newAgent("R2D2")
        putThing(w,robot,Location(0,0))
        ob1,ob2=newObject("f0"),newObject("f1")
        putThing(w,ob1,Location(0,1))
        putThing(w,ob2,Location(1,0))
        res = findGoal(w,g1)
        self.assertEqual(len(res),5)
        lw=pathToWorlds(w,res)
        self.assertEqual(g1(lw[-1].state),True)

    def test_fg_7(self) -> None:
        w2:World= newWorld("ToyPlayGround",6,6)
        robot:Agent = newAgent("Mary")
        putThing(w2,robot,Location(0,0))
        box0:Object = newObject("Key")
        putThing(w2,box0,Location(5,5))
        box1:Object = newObject("Ball")
        putThing(w2,box1,Location(4,1))
        setAltitude(w2,Location(2,2),2,2,4)
        res = findGoal(w2,g77)
        self.assertEqual(len(res),11)
        lw=pathToWorlds(w2,res)
        self.assertEqual(len(lw)>0,True)
        self.assertEqual(g77(lw[-1].state),True)

def g77(ths:State)->bool:
    r:Thing = ths["Mary"]
    return r.where == Location(5,5) 

if __name__ == '__main__':
    unittest.main(failfast=True)