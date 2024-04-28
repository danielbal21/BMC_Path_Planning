import random as rand

from z3 import *

from Models.Kripke import Kripke
from Models.Node import Node
from Models.Robot import Robot
from Models.System import System


def generate_from_system(system, n):
    """
    Generate a Kripke structure from the given system.

    Args:
        system (System): The system object.
        n (int): Size of the grid.

    Returns:
        Kripke: The generated Kripke structure.
    """
    node_id = 0
    M2 = Kripke(n)
    robot_pos = {}
    history = []
    initial_node = Node(node_id, True, False, n)

    # Initial Node Setup

    for i in range(len(system.robots)):
        initial_node.add_property(True, system.robots[i].initial_pos[0], system.robots[i].initial_pos[1])
        robot_pos[i] = set()
        robot_pos[i].add((system.robots[i].initial_pos[0], system.robots[i].initial_pos[1]))

    M2.add_node(initial_node)
    hasClosedLoop = False
    nextNode = initial_node

    while not hasClosedLoop:
        node_id += 1
        history.append(copy.copy(robot_pos))
        # Calculate possible whereabouts of each robot in the next step
        prevNode = nextNode
        nextNode = Node(node_id, False, False, n)
        for i in range(len(system.robots)):
            future = set()
            for possible_pos in robot_pos[i]:
                move = system.robots[i].movement_get(possible_pos[0], possible_pos[1])
                if move is None:
                    raise Exception("The given system has a path with no closed loop")
                if move.right:
                    future.add((possible_pos[0], possible_pos[1] + 1))
                if move.left:
                    future.add((possible_pos[0], possible_pos[1] - 1))
                if move.up:
                    future.add((possible_pos[0] - 1, possible_pos[1]))
                if move.down:
                    future.add((possible_pos[0] + 1, possible_pos[1]))
                if move.stay:
                    future.add((possible_pos[0], possible_pos[1]))
            robot_pos[i] = future

        for i in range(len(history)):
            # closed loop - finish
            if history[i] == robot_pos:
                hasClosedLoop = True
                M2.add_relation(prevNode, M2.nodes[i])
                break

        if not hasClosedLoop:
            for robot_positions in robot_pos:
                for possible_pos in robot_pos[robot_positions]:
                    nextNode.add_property(True, possible_pos[0], possible_pos[1])

            M2.add_node(nextNode)
            M2.add_relation(prevNode, nextNode)

    return M2


def create_M1(n):
    """
    Create the M1 Kripke structure.

    Args:
        n (int): Size of the grid.

    Returns:
        Kripke: M1 Kripke structure.
    """
    M1 = Kripke(n)
    grid = []

    for i in range(n):
        grid.append([])
        for j in range(n):
            node_id = (i * n) + j
            node = (Node(node_id, (node_id == 0), node_id == ((n * n) - 1), n))
            node.add_property(True, i, j)
            M1.add_node(node)

    for row in range(n):
        for col in range(n):
            right = True
            left = True
            up = True
            down = True
            stay = True

            if col == 0:
                left = False
            elif col == n - 1:
                right = False
            if row == 0:
                up = False
            elif row == n - 1:
                down = False

            if up:
                M1.add_relation_by_id((row * n) + col, ((row - 1) * n) + col)
            if down:
                M1.add_relation_by_id((row * n) + col, ((row + 1) * n) + col)
            if right:
                M1.add_relation_by_id((row * n) + col, (row * n) + col + 1)
            if left:
                M1.add_relation_by_id((row * n) + col, (row * n) + col - 1)

            M1.add_relation_by_id((row * n) + col, (row * n) + col)

    return M1


def auto_generate_system(n, num_counter_agents, stay_chance, stray_radius):
    """
    Automatically generate a system and its corresponding Kripke structure.

    Args:
        n (int): Size of the grid.
        num_counter_agents (int): Number of counter agents.
        stay_chance (float): Probability of staying in the same position.
        stray_radius (int): Maximum radius for straying from the initial position.

    Returns:
        Tuple[System, Kripke]: A tuple containing the generated system and its corresponding Kripke structure.
    """
    generated_system = System()

    for rnum in range(num_counter_agents):
        generated_system.add_robot(auto_gen_robot(n, stay_chance, stray_radius))

    return generated_system, generate_from_system(generated_system, n)


def auto_gen_robot(n, stay_chance, stray_radius):
    """
    Automatically generate a robot with random movements.

    Args:
        n (int): Size of the grid.
        stay_chance (float): Probability of staying in the same position.
        stray_radius (int): Maximum radius for straying from the initial position.

    Returns:
        Robot: The generated robot.
    """
    robot = Robot()
    initial_pos = (random_number(0, n - 1), random_number(0, n - 1))
    print(f"initial: {initial_pos}")
    can_initially_stay = has_happend(stay_chance)
    if can_initially_stay:
        minimal_stray_radius = 0
    else:
        minimal_stray_radius = 1

    travel_distance = random_number(minimal_stray_radius, stray_radius)
    robot.initial_pos = initial_pos
    can_move_up = has_happend(0.5) and ((initial_pos[0] - 1) >= 0) and (travel_distance > 0)
    can_move_down = has_happend(0.5) and ((initial_pos[0] + 1) < n) and (travel_distance > 0)
    can_move_right = has_happend(0.5) and ((initial_pos[1] + 1) < n) and (travel_distance > 0)
    can_move_left = has_happend(0.5) and ((initial_pos[1] - 1) >= 0) and (travel_distance > 0)
    robot.add_movement(initial_pos[0], initial_pos[1], can_move_right, can_move_left, can_move_up, can_move_down,
                       can_initially_stay, True)
    current_pos = initial_pos

    if (not can_move_up) and (not can_move_down) and (not can_move_left) and (not can_move_right):
        can_initially_stay = True

    robot.add_movement(initial_pos[0], initial_pos[1], can_move_right, can_move_left, can_move_up, can_move_down,
                       can_initially_stay, True)

    if can_move_right:
        step((current_pos[0], current_pos[1] + 1), n, robot, initial_pos, stay_chance,
             travel_distance)

    if can_move_left:
        step((current_pos[0], current_pos[1] - 1), n, robot, initial_pos, stay_chance,
             travel_distance)

    if can_move_up:
        step((current_pos[0] - 1, current_pos[1]), n, robot, initial_pos, stay_chance,
             travel_distance)

    if can_move_down:
        step((current_pos[0] + 1, current_pos[1]), n, robot, initial_pos, stay_chance,
             travel_distance)

    return robot


def has_happend(chance):
    """
    Determine if an event has occurred based on a given probability.

    Args:
        chance (float): The probability of the event occurring.

    Returns:
        bool: True if the event has occurred, False otherwise.
    """
    return rand.random() < chance


def random_number(min_num, max_num):
    """
    Generate a random integer within the specified range.

    Args:
        min (int): The minimum value of the range.
        max (int): The maximum value of the range.

    Returns:
        int: A random integer within the specified range.
    """
    return rand.randint(min_num, max_num)


def distance(r, c, ri, ci):
    """
    Calculate the distance between two points.

    Args:
        r (int): Row of the first point.
        c (int): Column of the first point.
        ri (int): Row of the second point.
        ci (int): Column of the second point.

    Returns:
        tuple: A tuple representing the distance between the two points along the rows and columns.
    """
    return (ri - r), (ci - c)


def step(current_pos, n, robot, initial_pos, stay_chance, travel_distance):
    """
    Take a step in the robot's movement and update its properties accordingly.

    Args:
        current_pos (tuple): The current position of the robot.
        n (int): Size of the grid.
        robot (Robot): The robot object.
        initial_pos (tuple): The initial position of the robot.
        stay_chance (float): Probability of staying in the same position.
        travel_distance (int): Maximum distance the robot can travel from its initial position.

    Returns:
        None
    """
    if robot.movement_get(current_pos[0], current_pos[1]) is not None:
        return

    cur_distance = distance(current_pos[0], current_pos[1], initial_pos[0], initial_pos[1])
    can_move_up = has_happend(0.5) and ((current_pos[0] - 1) >= 0) and (abs(cur_distance[0]) < travel_distance)
    can_move_down = has_happend(0.5) and ((current_pos[0] + 1) < n) and (abs(cur_distance[0]) < travel_distance)
    can_move_right = has_happend(0.5) and ((current_pos[1] + 1) < n) and (abs(cur_distance[1]) < travel_distance)
    can_move_left = has_happend(0.5) and ((current_pos[1] - 1) >= 0) and (abs(cur_distance[1]) < travel_distance)
    can_stay = has_happend(stay_chance)

    if (not can_move_up) and (not can_move_down) and (not can_move_left) and (not can_move_right):
        can_stay = True

    robot.add_movement(current_pos[0], current_pos[1], can_move_right, can_move_left, can_move_up, can_move_down,
                       can_stay, False)

    if can_move_right:
        step((current_pos[0], current_pos[1] + 1), n, robot, initial_pos, stay_chance,
             travel_distance)

    if can_move_left:
        step((current_pos[0], current_pos[1] - 1), n, robot, initial_pos, stay_chance,
             travel_distance)

    if can_move_up:
        step((current_pos[0] - 1, current_pos[1]), n, robot, initial_pos, stay_chance,
             travel_distance)

    if can_move_down:
        step((current_pos[0] + 1, current_pos[1]), n, robot, initial_pos, stay_chance,
             travel_distance)
