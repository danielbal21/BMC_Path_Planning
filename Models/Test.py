from z3 import Bool, Solver, solve

from Models.Robot import Robot
from Models.System import System
from Services.KripkeGenerator import KripkeGenerator

#x = Bool('p1,2,3')
#s = Solver()
#s.add(x)
#print(s.check())
#print(s.model())

kg = KripkeGenerator()
n = 10
sys = System()
r1 = Robot()
r1.initial_pos = (4,4)
r1.add_movement(4,4,False,False,True,True,False,True)
r1.add_movement(3,4,True,False,False,False,False,False)
r1.add_movement(5,4,True,False,False,False,False,False)
r1.add_movement(3,5,False,False,False,True,False,False)
r1.add_movement(5,5,False,False,True,False,False,False)
r1.add_movement(4,5,False,True,False,False,False,False)
sys.add_robot(r1)

r2 = Robot()
r2.initial_pos = (8,7)
r2.add_movement(8,7,True,False,False,False,False,True)
r2.add_movement(8,8,True,True,False,False,False,False)
r2.add_movement(8,9,False,True,False,False,False,False)
sys.add_robot(r2)
kg.generate_from_system(sys,n)

