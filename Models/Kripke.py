class Kripke:
    def __init__(self, n):
        """
        Initialize a Kripke structure with the specified parameters.

        Args:
            n (int): The size of the grid (n x n).
        """
        self.nodes = []
        self.relations = {}
        self.count = 0
        self.n = n
        pass

    def __getstate__(self):
        """
        Get the state of the Kripke structure for pickling.

        Returns:
            dict: The state of the Kripke structure.
        """
        return self.__dict__

    def __setstate__(self, state):
        """
        Set the state of the Kripke structure after unpickling.

        Args:
            state (dict): The state of the Kripke structure.
        """
        self.__dict__.update(state)

    def add_node(self, node):
        """
        Add a node to the Kripke structure.

        Args:
            node (Node): The node to add.
        """
        self.nodes.append(node)
        self.count += 1

    def add_relation(self, node1, node2):
        """
        Add a relation between two nodes in the Kripke structure.

        Args:
            node1 (Node): The first node.
            node2 (Node): The second node.
        """
        if not (node1.node_id in self.relations):
            self.relations[node1.node_id] = set()
        self.relations[node1.node_id].add(node2.node_id)

    def add_relation_by_id(self, node1_id, node2_id):
        """
        Add a relation between two nodes specified by their IDs.

        Args:
            node1_id (int): The ID of the first node.
            node2_id (int): The ID of the second node.
        """
        if not (node1_id in self.relations):
            self.relations[node1_id] = set()
        self.relations[node1_id].add(node2_id)

    def are_related(self, node1, node2):
        """
        Check if two nodes are related in the Kripke structure.

        Args:
            node1 (Node): The first node.
            node2 (Node): The second node.

        Returns:
            bool: True if there is a relation, False otherwise.
        """
        return node1 in self.nodes and node1 in self.relations and node2.node_id in self.relations[node1.node_id]

    def get_initial_state(self):
        """
        Get the initial state node in the Kripke structure.

        Returns:
            Node: The initial state node, or None if not found.
        """
        for n in self.nodes:
            if n.initial:
                return n
        return None

    def get_final_state(self):
        """
        Get the final state node in the Kripke structure.

        Returns:
            Node: The final state node, or None if not found.
        """
        for n in self.nodes:
            if n.final:
                return n
        return None
