from threading import Thread

from z3 import Solver, sat, is_true, unsat, Z3Exception

from Services.Formulizer import formulise

ret = None


def Solve(n, M2, length):
    """
    Solve the given formula using Z3 solver.

    Args:
        n (int): Size of the grid.
        M2 (Kripke): The Kripke structure.
        length (int): The length of the path.

    Returns:
        tuple: A tuple containing the status of the solution and the solution itself.
    """
    solution = []
    solver = Solver()
    solver.add(formulise(M2, n, length))
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
                    solution.append((parse_string_to_tuple(str(decl))))
                    print(f"{decl}: {assignment}")
        else:
            print("Not satisfiable")

    except Z3Exception as e:
        # Handle the timeout exception
        print(f"Solving timeout")
        status = "timeout"

    print("Sol test:")
    print(solution)
    return status, solution


def run_solver_on_thread(n, M2, k):
    """
        Run the solver on a separate thread with a specified timeout.

        Args:
            n (int): Size of the grid.
            M2 (Kripke): The Kripke structure.
            k (int): Length of the path.

        Returns:
            Thread: The thread running the solver.
        """
    global ret
    ret = "running", []
    if k < (2 * n) - 1:
        return unsat, []

    def target():
        global ret
        res = Solve(n, M2, k)
        ret = res

    thread = Thread(target=target)
    thread.start()

    return thread


def get_result():
    """
    Get the result of the solver.

    Returns:
        tuple: A tuple containing the status of the solution and the solution itself.
    """
    global ret
    return ret


def parse_string_to_tuple(input_string):
    """
    Parse a string representation to a tuple.

    Args:
        input_string (str): The input string to parse.

    Returns:
        tuple: The parsed tuple.
    """
    # Split the input string using '_' as a delimiter
    parts = input_string.split('_')

    # Extract the row and column values
    row = int(parts[2])
    col = int(parts[3])

    # Return the values as a tuple
    return row, col
