class System:
    def __init__(self):
        """
        Initialize a System object with an empty list of robots.
        """
        self.robots = []


    def __str__(self):
        """
        Return a string representation of the System object.

        Returns:
            str: String representation of the System object.
        """
        pass

    def add_robot(self, robot):
        """
        Add a robot to the system.

        Args:
            robot (Robot): The robot to add to the system.
        """
        self.robots.append(robot)

    def clear(self):
        """
        Clear the list of robots in the system.
        """
        self.robots.clear()