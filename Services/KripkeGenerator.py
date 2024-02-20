from math import sqrt
import random as rand
from z3 import *

from Models.Kripke import Kripke
from Models.Node import Node
from Models.Robot import Robot
from Models.System import System


def generate_from_system(system, n):
    node_id = 0
    robot_id = 0
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
    generated_system = System()

    for rnum in range(num_counter_agents):
        generated_system.add_robot(auto_gen_robot(n, stay_chance, stray_radius))

    return generated_system, generate_from_system(generated_system,n)


def auto_gen_robot(n, stay_chance, stray_radius):
    robot = Robot()
    initial_pos = (random_number(0, n - 1), random_number(0, n - 1))
    print(f"initial: {initial_pos}")
    can_initially_stay = has_happend(stay_chance)
    minimal_stray_radius = 0
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
    cur_distance = (travel_distance, travel_distance)

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
    return rand.random() < chance


def random_number(min, max):
    return rand.randint(min, max)


def distance(r, c, ri, ci):
    return (ri - r), (ci - c)


def step(current_pos, n, robot, initial_pos, stay_chance, travel_distance):
    print(current_pos)
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
