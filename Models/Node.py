class Node:
    def __init__(self, node_id, is_initial, is_final):
        self.properties = []
        self.node_id = node_id
        self.initial = is_initial
        self.final = is_final

    def add_property(self, atomic_property):
        if atomic_property not in self.properties:
            self.properties.append(atomic_property)
        else:
            raise ValueError

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.node_id == other.node_id
        return False
