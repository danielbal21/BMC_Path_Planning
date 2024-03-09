import z3
from z3 import Bool, Solver, solve, sat, Not, Implies, And, Or, AtMost, PbEq


def create_base(n, k):
    base = [[[Bool(f'p_{t}_{r}_{c}') for c in range(n)] for r in range(n)] for t in range(k)]
    return base


# starting position
def alpha_initial(base):
    return base[0][0][0]


def alpha_final(base, n, k):
    return base[k - 1][n - 1][n - 1]


# valid steps
def alpha_k(base, n, k):
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


# safety
def alpha_s(base, M2, n, k):
    current = M2.get_initial_state()
    s = True
    for t in range(k):
        for row in range(n):
            for col in range(n):
                s = And(s, Implies(base[t][row][col], not current.properties[row][col]))
        current = M2.nodes[next(iter((M2.relations[current.node_id])))]

    return s


# single path
def alpha_sp(base, n, k):
    formula = True
    for t in range(k):
        # Create a list of all variables in base[t]
        variables_in_base_t = [base[t][r][c] for r in range(n) for c in range(n)]

        # Perform AtMost on all variables in base[t]
        formula = And(AtMost(*variables_in_base_t, 1), formula)

    return formula

def formulise(M2, n, k):
    base = create_base(n, k)
    a_i = alpha_initial(base)
    a_f = alpha_final(base, n, k)
    a_k = alpha_k(base, n, k)
    a_s = alpha_s(base, M2, n, k)
    a_sp = alpha_sp(base, n, k)

    return And(a_sp, a_i, a_f, a_k, a_s)
