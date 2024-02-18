from z3 import Bool, Solver, solve, sat, Not, is_true

from Models.Robot import Robot
from Models.System import System
from Services.Formulizer import create_base, formulise
from Services.KripkeGenerator import generate_from_system, create_M1, auto_generate_system
import Services.FileManager

exit(0)
n = 10
sys, m2_1 = auto_generate_system(5, 1, 0.7, 1)
exit(0)
sys = System()
r1 = Robot()
r1.initial_pos = (4, 4)
r1.add_movement(4, 4, False, False, True, True, False, True)
r1.add_movement(3, 4, True, False, False, False, False, False)
r1.add_movement(5, 4, True, False, False, False, False, False)
r1.add_movement(3, 5, False, False, False, True, False, False)
r1.add_movement(5, 5, False, False, True, False, False, False)
r1.add_movement(4, 5, False, True, False, False, False, False)
sys.add_robot(r1)

r2 = Robot()
r2.initial_pos = (8, 7)
r2.add_movement(8, 7, True, False, False, False, False, True)
r2.add_movement(8, 8, True, True, False, False, False, False)
r2.add_movement(8, 9, False, True, False, False, False, False)
sys.add_robot(r2)
m2 = generate_from_system(sys, n)

# TEST 2

n = 9
k = 18
sys = System()
r1 = Robot()
r1.initial_pos = (0, 1)
r1.add_movement(0, 1, False, True, False, False, False, True)
r1.add_movement(0, 0, False, False, False, False, True, False)
sys.add_robot(r1)

r2 = Robot()
r2.initial_pos = (1, 0)
r2.add_movement(1, 0, False, False, True, False, False, True)
r2.add_movement(0, 0, False, False, False, False, True, False)
sys.add_robot(r2)

# Generate M1 and M2
M2 = generate_from_system(sys, n)
M1 = create_M1(n)

solver = Solver()
solver.add(formulise(M2, n, k))

# Check satisfiability
if solver.check() == sat:
    model = solver.model()
    print("Satisfiable")

    # Get declarations and sort them based on _t_
    declarations = sorted(model, key=lambda x: int(x.name().split('_')[1]))

    # Iterate through sorted declarations and print true assignments
    for decl in declarations:
        assignment = model[decl]
        if is_true(assignment):
            print(f"{decl}: {assignment}")
else:
    print("Not satisfiable")

# Check if the formula is satisfiable
# if solver.check() == sat:
#  model = solver.model()
# print(model)
# else:
# print("No solution exists.")
