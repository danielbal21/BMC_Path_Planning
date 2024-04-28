from z3 import Bool, Implies, And, Or, AtMost, PbEq


def create_base(n, k):
    """
    Create a base grid of Boolean variables.

    Args:
        n (int): Size of the grid.
        k (int): Number of time steps.

    Returns:
        list: A 3D list representing the base grid.
    """
    base = [[[Bool(f'p_{t}_{r}_{c}') for c in range(n)] for r in range(n)] for t in range(k)]
    return base


def alpha_initial(base):
    """
    Define the initial position.

    Args:
        base (list): The base grid.

    Returns:
        z3.BoolRef: The Boolean variable representing the initial position.
    """
    return base[0][0][0]


def alpha_final(base, n, k):
    """
    Define the final position.

    Args:
        base (list): The base grid.
        n (int): Size of the grid.
        k (int): Number of time steps.

    Returns:
        z3.BoolRef: The Boolean variable representing the final position.
    """
    return base[k - 1][n - 1][n - 1]


def alpha_k(base, n, k):
    """
    Define valid steps.

    Args:
        base (list): The base grid.
        n (int): Size of the grid.
        k (int): Number of time steps.

    Returns:
        z3.BoolRef: A Boolean formula representing valid steps.
    """
    alph_k = (k >= ((2 * n) - 1))
    for t in range(k - 1):
        for r in range(n):
            for c in range(n):
                left = right = up = down = True
                total = []
                if c == 0:
                    left = False
                elif c == n - 1:
                    right = False
                if r == 0:
                    up = False
                elif r == n - 1:
                    down = False

                if up:
                    total.append(base[t + 1][r - 1][c])
                if down:
                    total.append(base[t + 1][r + 1][c])
                if right:
                    total.append(base[t + 1][r][c + 1])
                if left:
                    total.append(base[t + 1][r][c - 1])

                # Stay
                # total.append(base[t + 1][r][c])
                alph_k = And(alph_k,
                             Implies(base[t][r][c], Or(base[t + 1][r][c], PbEq([(var, 1) for var in total], 1))))
    return alph_k


def alpha_s(base, M2, n, k):
    """
    Define safety conditions.

    Args:
        base (list): The base grid.
        M2 (object): Object representing the system.
        n (int): Size of the grid.
        k (int): Number of time steps.

    Returns:
        z3.BoolRef: A Boolean formula representing safety conditions.
    """
    current = M2.get_initial_state()
    s = True
    for t in range(k):
        for row in range(n):
            for col in range(n):
                s = And(s, Implies(base[t][row][col], not current.properties[row][col]))
        current = M2.nodes[next(iter((M2.relations[current.node_id])))]

    return s


def alpha_sp(base, n, k):
    """
    Define single path conditions.

    Args:
        base (list): The base grid.
        n (int): Size of the grid.
        k (int): Number of time steps.

    Returns:
        z3.BoolRef: A Boolean formula representing single path conditions.
    """
    formula = True
    for t in range(k):
        # Create a list of all variables in base[t]
        variables_in_base_t = [base[t][r][c] for r in range(n) for c in range(n)]

        # Perform AtMost on all variables in base[t]
        formula = And(AtMost(*variables_in_base_t, 1), formula)

    return formula


def formulise(M2, n, k):
    """
    Formulate the entire system constraints.

    Args:
        M2 (object): Object representing the system.
        n (int): Size of the grid.
        k (int): Number of time steps.

    Returns:
        z3.BoolRef: A Boolean formula representing the entire system constraints.
    """
    base = create_base(n, k)
    a_i = alpha_initial(base)
    a_f = alpha_final(base, n, k)
    a_k = alpha_k(base, n, k)
    a_s = alpha_s(base, M2, n, k)
    a_sp = alpha_sp(base, n, k)

    return And(a_sp, a_i, a_f, a_k, a_s)
