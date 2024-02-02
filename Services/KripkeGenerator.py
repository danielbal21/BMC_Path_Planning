from z3 import *

from Models.Kripke import Kripke
from Models.Node import Node


class KripkeGenerator:
    def __init__(self):
        pass

    def generate_from_system(self, system, n):
        node_id = 0
        robot_id = 0
        M2 = Kripke()
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
