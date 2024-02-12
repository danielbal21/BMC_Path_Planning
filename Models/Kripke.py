class Kripke:
    def __init__(self):
        self.nodes = []
        self.relations = {}
        self.count = 0
        pass

    def add_node(self, node):
        self.nodes.append(node)
        self.count += 1

    def add_relation(self, node1, node2):
        if not (node1.node_id in self.relations):
            self.relations[node1.node_id] = set()
        self.relations[node1.node_id].add(node2.node_id)

    def add_relation_by_id(self, node1_id, node2_id):
        if not (node1_id in self.relations):
            self.relations[node1_id] = set()
        self.relations[node1_id].add(node2_id)
    def are_related(self, node1, node2):
        return node1 in self.nodes and node1 in self.relations and node2.node_id in self.relations[node1.node_id]

    def get_initial_state(self):
        for n in self.nodes:
            if n.initial:
                return n
        return None

    def get_final_state(self):
        for n in self.nodes:
            if n.final:
                return n
        return None
