from z3 import Or


class Node:
    def __init__(self, node_id, is_initial, is_final, n):
        self.properties = []
        for rows in range(n):
            self.properties.append([])
            for columns in range(n):
                self.properties[rows].append(False)
        self.node_id = node_id
        self.initial = is_initial
        self.final = is_final

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)

    def add_property(self, present, row, column):
        if present:
            self.properties[row][column] = True

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.node_id == other.node_id
        return False
