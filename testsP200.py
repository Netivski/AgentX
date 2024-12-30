from playground2 import *
import unittest
from typing import *

def goalw201(ths:State)->bool:
    r:Agent = cast(Agent,ths["Batman"])
    return r.where == Location(0,0) and len(r.objects) == 2

class wormHolesTest(unittest.TestCase):

    def test_WH_0F(self)->None:
        w2:World= newWorld("BlackHole",6,6)
        robot:Agent = newAgent("Batman")
        putThing(w2,robot,Location(0,0))
        box0:Object = newObject("Key")
        putThing(w2,box0,Location(5,5))
        box1:Object = newObject("Ball")
        putThing(w2,box1,Location(4,1))
        setWormhole(w2,Location(1,1),Location(4,5))

    def test_WH_1F(self)->None:
        w2:World= newWorld("BlackHole",6,6)
        robot:Agent = newAgent("Mary")
        putThing(w2,robot,Location(0,0))
        box0:Object = newObject("Key")
        putThing(w2,box0,Location(5,5))
        box1:Object = newObject("Ball")
        putThing(w2,box1,Location(4,1))
        setWormhole(w2,Location(1,1),Location(5,4))

    def test_WH_2F(self)->None:
        w2:World= newWorld("BlackHole",6,6)
        robot:Agent = newAgent("Mary")
        putThing(w2,robot,Location(0,0))
        box0:Object = newObject("Key")
        putThing(w2,box0,Location(5,5))
        box1:Object = newObject("Ball")
        putThing(w2,box1,Location(4,1))
        try:
            setWormhole(w2,Location(1,1),Location(6,4))
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_WH_3F(self)->None:
        w2:World= newWorld("BlackHole",6,6)
        robot:Agent = newAgent("Mary")
        putThing(w2,robot,Location(0,0))
        box0:Object = newObject("Key")
        putThing(w2,box0,Location(5,5))
        box1:Object = newObject("Ball")
        putThing(w2,box1,Location(4,1))
        try:
            setWormhole(w2,Location(1,1),Location(0,1))
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_WH_4F(self)->None:
        w2:World= newWorld("BlackHole",6,6)
        robot:Agent = newAgent("Mary")
        putThing(w2,robot,Location(0,0))
        box0:Object = newObject("Key")
        putThing(w2,box0,Location(5,5))
        box1:Object = newObject("Ball")
        putThing(w2,box1,Location(4,1))
        try:
            setWormhole(w2,Location(1,1),Location(2,1))
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_WH_5F(self)->None:
        w2:World= newWorld("BlackHole",6,6)
        robot:Agent = newAgent("Mary")
        putThing(w2,robot,Location(0,0))
        box0:Object = newObject("Key")
        putThing(w2,box0,Location(5,5))
        box1:Object = newObject("Ball")
        putThing(w2,box1,Location(4,1))
        try:
            setWormhole(w2,Location(1,2),Location(2,2))
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_WH_6F(self)->None:
        w2:World= newWorld("BlackHole",6,6)
        robot:Agent = newAgent("Mary")
        putThing(w2,robot,Location(0,0))
        box0:Object = newObject("Key")
        putThing(w2,box0,Location(5,5))
        box1:Object = newObject("Ball")     
        putThing(w2,box1,Location(4,1))    
        try:
            setWormhole(w2,Location(1,2),Location(2,3))
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_WH_7F(self)->None:
        w2:World= newWorld("BlackHole",6,6)
        robot:Agent = newAgent("Mary")
        putThing(w2,robot,Location(0,0))
        box0:Object = newObject("Bomb")
        putThing(w2,box0,Location(5,5))
        box1:Object = newObject("Ball")     
        putThing(w2,box1,Location(4,1))    
        try:
            setWormhole(w2,Location(2,2),Location(2,5))
            setWormhole(w2,Location(4,2),Location(3,5))
        except Exception as ex:
            self.assertEqual(type(ex), PlayGroundError)
            return
        self.fail('PlayGroundError not raised')

    def test_WH_1(self)->None:
        w2:World= newWorld("BlackHole",6,6)
        robot:Agent = newAgent("Batman")
        putThing(w2,robot,Location(0,0))
        box0:Object = newObject("Cube")
        putThing(w2,box0,Location(5,5))
        box1:Object = newObject("Knife")
        putThing(w2,box1,Location(4,1))
        setAltitude(w2,Location(3,4),3,2,4) 
        setAltitude(w2,Location(4,5),2,1,0) 
        setAltitude(w2,Location(2,2),2,2,4) 
        setWormhole(w2,Location(1,1),Location(4,4))
        solution = findGoal(w2,goalw201)
        lw = pathToWorlds(w2,solution)
        self.assertEqual(len(lw),13)

def goalw0(ths:State)->bool:
    for th in ths.values():
        if type(th) == Agent:
            if not locInRect(th.where,Location(2,3),2,2):
                return False
        else:
            return False
    return True

def goalw1(ths:State)->bool:
    for th in ths.values():
        if type(th) == Agent:
            if not locInRect(th.where,Location(1,1),1,1):
                return False
        else:
            return False
    return True

def goalw2(ths:State)->bool:
    for th in ths.values():
        if type(th) == Agent:
            if not locInRect(th.where,Location(5,5),1,1):
                return False
        else:
            return False
    return True

class WingsTest(unittest.TestCase):

    def test_Wing_0(self)->None:
        w2:World= newWorld("OneWing",6,6)
        setComWing(w2,Location(2,3),2,2)  
        robot1:Agent = newAgent("Mary")
        putThing(w2,robot1,Location(5,0))
        robot2:Agent = newAgent("Jack")
        putThing(w2,robot2,Location(0,5))
        solution = findGoal(w2,goalw0)
        lw = pathToWorlds(w2,solution)
        self.assertEqual(len(lw),9)

    def test_Wing_1(self)->None:
        w2:World= newWorld("BlackHole",6,6)
        setComWing(w2,Location(1,1),1,1)  
        robot1:Agent = newAgent("Mary")
        putThing(w2,robot1,Location(5,0))
        robot2:Agent = newAgent("Jack")
        putThing(w2,robot2,Location(0,5))
        box0:Object = newObject("Key")
        putThing(w2,box0,Location(5,5))
        box1:Object = newObject("Ball")
        putThing(w2,box1,Location(4,1))
        solution = findGoal(w2,goalw1)
        lw = pathToWorlds(w2,solution)
        self.assertEqual(len(lw),19)

    def test_Wing_2(self)->None:
        w2:World= newWorld("OneWing",6,6)
        setComWing(w2,Location(5,5),1,1)  
        robot1:Agent = newAgent("Mary")
        putThing(w2,robot1,Location(5,0))
        robot2:Agent = newAgent("Jack")
        putThing(w2,robot2,Location(0,5))
        solution = findGoal(w2,goalw2)
        lw = pathToWorlds(w2,solution)
        self.assertEqual(len(lw),11)

    def test_Wing_3(self)->None:
        w2:World= newWorld("OneWing",6,6)
        setComWing(w2,Location(5,5),1,1)  
        robot1:Agent = newAgent("Mary")
        putThing(w2,robot1,Location(5,5))
        robot2:Agent = newAgent("Jack")
        putThing(w2,robot2,Location(0,5))
        solution = findGoal(w2,goalw2)
        lw = pathToWorlds(w2,solution)
        self.assertEqual(len(lw),6)

class CKMTests(unittest.TestCase):

    def test_CKM_04(self) -> None:
        w = newWorld("Playground",20,20)
        robot1 = newAgent("CookieMonster")
        putThing(w,robot1,Location(0,9))
        box0 = newObject("box0")
        putThing(w,box0,Location(1,1))
        box1 = newObject("box1")
        putThing(w,box1,Location(1,3))
        box2 = newObject("box2")
        putThing(w,box2,Location(1,7))
        box3 = newObject("box3")
        putThing(w,box3,Location(1,19))
        setAltitude(w,Location(3,0),2,11,9) ## check this
        setAltitude(w,Location(3,12),2,8,9) ## check this
        self.assertEqual(validCookieMonster(w),True)
        CookieMonster(w)

    def test_CKM_06(self) -> None:
        w = newWorld("Playground",20,20)
        robot1 = newAgent("CookieMonster")
        putThing(w,robot1,Location(0,9))
        box0 = newObject("box0")
        putThing(w,box0,Location(1,1))
        box1 = newObject("box1")
        putThing(w,box1,Location(1,3))
        box2 = newObject("box2")
        putThing(w,box2,Location(1,7))
        box3 = newObject("box3")
        putThing(w,box3,Location(1,19))
        box4 = newObject("box4")
        putThing(w,box4,Location(1,17))
        box5 = newObject("box5")
        putThing(w,box5,Location(1,16))
        setAltitude(w,Location(3,0),2,11,9) ## check this
        setAltitude(w,Location(3,12),2,8,9) ## check this
        self.assertEqual(validCookieMonster(w),True)
        CookieMonster(w)

    def test_CKM_08(self) -> None:
        w = newWorld("Playground",20,20)
        robot1 = newAgent("CookieMonster")
        putThing(w,robot1,Location(0,9))
        box0 = newObject("box0")
        putThing(w,box0,Location(1,1))
        box1 = newObject("box1")
        putThing(w,box1,Location(1,3))
        box2 = newObject("box2")
        putThing(w,box2,Location(1,7))
        box3 = newObject("box3")
        putThing(w,box3,Location(1,19))
        box4 = newObject("box4")
        putThing(w,box4,Location(1,17))
        box5 = newObject("box5")
        putThing(w,box5,Location(1,16))
        setAltitude(w,Location(3,0),2,11,9) 
        setAltitude(w,Location(3,12),2,8,9) 
        self.assertEqual(validCookieMonster(w),True)
        CookieMonster(w)

    def test_CKM_07(self) -> None:
        w = newWorld("Playground",20,20)
        robot1 = newAgent("CookieMonster")
        putThing(w,robot1,Location(0,9))
        box0 = newObject("box0")
        putThing(w,box0,Location(1,1))
        box1 = newObject("box1")
        putThing(w,box1,Location(1,3))
        box2 = newObject("box2")
        putThing(w,box2,Location(1,7))
        box3 = newObject("box3")
        putThing(w,box3,Location(1,19))
        box4 = newObject("box4")
        putThing(w,box4,Location(1,17))
        box5 = newObject("box5")
        putThing(w,box5,Location(1,16))
        box6 = newObject("box6")
        putThing(w,box6,Location(10,15))
        setAltitude(w,Location(3,0),2,11,9) 
        setAltitude(w,Location(3,12),2,8,9) 
        self.assertEqual(validCookieMonster(w),True)
        CookieMonster(w)

    def test_CKM_10(self) -> None:
        w = newWorld("Playground",15,15)
        robot1 = newAgent("CookieMonster")
        putThing(w,robot1,Location(0,9))
        box0 = newObject("box0")
        putThing(w,box0,Location(1,1))
        box1 = newObject("box1")
        putThing(w,box1,Location(1,3))
        box2 = newObject("box2")
        putThing(w,box2,Location(1,7))
        box3 = newObject("box3")
        putThing(w,box3,Location(1,14))
        box4 = newObject("box4")
        putThing(w,box4,Location(1,13))
        box5 = newObject("box5")
        putThing(w,box5,Location(1,12))
        box6 = newObject("box6")
        putThing(w,box6,Location(10,3))
        box7 = newObject("box7")
        putThing(w,box7,Location(12,10))
        box8 = newObject("box8")
        putThing(w,box8,Location(8,8))
        setAltitude(w,Location(3,0),2,11,9) ## check this
        setAltitude(w,Location(3,12),2,1,9) ## check this
        self.assertEqual(validCookieMonster(w),True)
        CookieMonster(w)


def locInRect(loc:Location,locr:Location,w:int,h:int)->bool:
    return locr.xpos <= loc.xpos < locr.xpos+w and \
    locr.ypos <= loc.ypos < locr.ypos+h

def goalwg0(ths:State)->bool:
    for th in ths.values():
        if type(th) == Agent:
            if not locInRect(th.where,Location(0,0),2,2):
                return False
    return True

class WGTestsR(unittest.TestCase):

    def test_wg_0(self) -> None:
        w1 = newWorld("Room",6,6)
        robot1 = newAgent("robot1")
        putThing(w1,robot1,Location(0,3))
        robot2 = newAgent("robot2")
        putThing(w1,robot2,Location(0,5))
        robot3 = newAgent("robot3")
        putThing(w1,robot3,Location(5,0))
        setAltitude(w1,Location(1,1),2,2,4)  
        robot4 = newAgent("robot4")
        putThing(w1,robot4,Location(5,5))
        setComWing(w1,Location(0,0),2,2)
        res = gatherWizards(w1)
#       findGoal
        sol = pathToWorlds(w1,res)
        self.assertEqual(len(sol),20)
        lw = sol[-1]
        self.assertTrue(goalwg0(lw.state))

    def test_wg_1(self) -> None:
        w1 = newWorld("Room",6,6)
        robot1 = newAgent("robot1")
        putThing(w1,robot1,Location(0,3))
        robot2 = newAgent("robot2")
        putThing(w1,robot2,Location(0,5))
        robot3 = newAgent("robot3")
        putThing(w1,robot3,Location(5,0))
        setAltitude(w1,Location(1,1),2,2,4)  
        robot4 = newAgent("robot4")
        putThing(w1,robot4,Location(5,5))
        robot5 = newAgent("robot5")
        putThing(w1,robot5,Location(5,4))
        setComWing(w1,Location(0,0),2,2)  
        res = gatherWizards(w1)
#       findGoal
        sol = pathToWorlds(w1,res)
        self.assertEqual(len(sol),28)
        lw = sol[-1]
        self.assertTrue(goalwg0(lw.state))

if __name__ == '__main__':
    unittest.main(failfast=True)
