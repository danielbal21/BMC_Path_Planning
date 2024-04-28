class Node:
    def __init__(self, node_id, is_initial, is_final, n):
        """
        Initialize a Node object with the specified properties.

        Args:
            node_id (int): The ID of the node.
            is_initial (bool): Whether the node is an initial state.
            is_final (bool): Whether the node is a final state.
            n (int): The size of the grid (n x n).
        """
        self.properties = []
        for rows in range(n):
            self.properties.append([])
            for columns in range(n):
                self.properties[rows].append(False)
        self.node_id = node_id
        self.initial = is_initial
        self.final = is_final

    def __getstate__(self):
        """
        Get the state of the node for pickling.

        Returns:
            dict: The state of the node.
        """
        return self.__dict__

    def __setstate__(self, state):
        """
        Set the state of the node after unpickling.

        Args:
            state (dict): The state of the node.
        """
        self.__dict__.update(state)

    def add_property(self, present, row, column):
        """
        Add a property to the node.

        Args:
            present (bool): Whether the property is present.
            row (int): Row index of the property.
            column (int): Column index of the property.
        """
        if present:
            self.properties[row][column] = True

    def __eq__(self, other):
        """
        Check equality with another Node object.

        Args:
            other (Node): Another Node object.

        Returns:
            bool: True if equal, False otherwise.
        """
        if isinstance(other, Node):
            return self.node_id == other.node_id
        return False
