class Kripke:
    def __init__(self):
        self.nodes = []
        self.relations = {}
        pass

    def add_node(self, node):
        self.nodes.append(node)

    def add_relation(self, node1, node2):
        self.relations[node1.node_id] = node2.node_id

    def are_related(self, node1, node2):
        return node1 in self.nodes and node1 in self.relations and self.relations[node1.node_id] == node2.node_id

    def get_initial_state(self):
        for n in self.nodes:
            if n.is_initial:
                return n
        return False

    def get_final_state(self):
        for n in self.nodes:
            if n.is_final:
                return n
        return False
