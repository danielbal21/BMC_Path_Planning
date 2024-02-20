from threading import Thread

from z3 import Solver, sat, is_true, unsat, solve, Z3Exception

from Services.Formulizer import formulise

ret = None


def Solve(n, M2, length, timeout_seconds):
    solution = []
    solver = Solver()
    solver.add(formulise(M2, n, length))
    # solver.set("timeout", timeout_seconds * 1000)
    print(f"running with k={length}")
    try:
        # Check satisfiability with a timeout
        status = solver.check()
        if status == sat:
            model = solver.model()
            print("Satisfiable")

            # Get declarations and sort them based on _t_
            declarations = sorted(model, key=lambda x: int(x.name().split('_')[1]))

            # Iterate through sorted declarations and print true assignments
            for decl in declarations:
                assignment = model[decl]
                if is_true(assignment):
                    solution.append(assignment)
                    print(f"{decl}: {assignment}")
        else:
            print("Not satisfiable")

    except Z3Exception as e:
        # Handle the timeout exception
        print(f"Solving timeout")
        status = "timeout"

    return status, solution


def run_solver_on_thread(n, M2, timeout_sec, k):
    global ret
    ret = "running", []
    if k < (2 * n) - 1:
        return unsat, []

    def target():
        global ret
        res = Solve(n, M2, k, timeout_sec)
        ret = res

    thread = Thread(target=target)
    thread.start()

    return thread


def get_result():
    global ret
    return ret
