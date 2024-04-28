def can_move_in_any_direction(movement):
    """
    Check if a movement can occur in any direction.

    Args:
        movement (Movement): The movement information.

    Returns:
        bool: True if the movement can occur in any direction, False otherwise.
    """
    if movement is None:
        return False
    return movement.up or movement.down or movement.left or movement.right or movement.stay


class Robot:
    def __init__(self):
        """
        Initialize a Robot object with an empty movement map and no initial position.
        """
        self.movement_map = {}
        self.initial_pos = None

    def clear(self):
        """
        Clear the movement map and initial position of the robot.
        """
        self.movement_map = {}
        self.initial_pos = None

    def add_movement(self, row, column, can_go_right, can_go_left, can_go_up, can_go_down, can_stay, is_initial):
        """
                Add movement information for a specific position to the robot.

                Args:
                    row (int): Row index of the position.
                    column (int): Column index of the position.
                    can_go_right (bool): Whether the robot can move right from this position.
                    can_go_left (bool): Whether the robot can move left from this position.
                    can_go_up (bool): Whether the robot can move up from this position.
                    can_go_down (bool): Whether the robot can move down from this position.
                    can_stay (bool): Whether the robot can stay in this position.
                    is_initial (bool): Whether this movement corresponds to the initial position of the robot.
                """
        self.movement_map[(row, column)] = Movement(can_go_right, can_go_left, can_go_up, can_go_down, can_stay)

        if not can_go_up and not can_go_down and not can_go_right and not can_go_left and not can_stay:
            if (row, column) in self.movement_map:
                self.movement_map.pop((row, column))

        if is_initial:
            self.initial_pos = (row, column)

        if self.initial_pos == (row, column) and not is_initial:
            is_initial = None

    def movement_get(self, row, col):
        """
        Get the movement information for a specific position.

        Args:
            row (int): Row index of the position.
            col (int): Column index of the position.

        Returns:
            Movement or None: The movement information for the specified position, or None if not available.
        """
        if (row, col) in self.movement_map:
            return self.movement_map[(row, col)]
        else:
            return None

    def is_valid(self):
        """
        Check if the robot configuration is valid.

        Returns:
            bool: True if the robot configuration is valid, False otherwise.
        """
        valid = True

        # check if this robot has an initial position
        if self.initial_pos is None:
            valid = False

        # check if every movement has at least one defined direction
        for pos in self.movement_map:
            if not can_move_in_any_direction(self.movement_map[pos]):
                valid = False

        if self.initial_pos not in self.movement_map:
            valid = False

        return valid and self.is_closed_loop()

    def is_closed_loop(self):
        """
        Check if the robot configuration forms a closed loop.

        Returns:
            bool: True if the robot configuration forms a closed loop, False otherwise.
        """
        valid = True
        for pos in self.movement_map:
            if self.movement_map[pos].up and not (pos[0] - 1, pos[1]) in self.movement_map and \
                    not self.movement_map[pos].stay:
                valid = False
            elif self.movement_map[pos].down and not (pos[0] + 1, pos[1]) in self.movement_map and not \
                    self.movement_map[pos].stay:
                valid = False
            elif self.movement_map[pos].right and not (pos[0], pos[1] + 1) in self.movement_map and not \
                    self.movement_map[pos].stay:
                valid = False
            elif self.movement_map[pos].left and not (pos[0], pos[1] - 1) in self.movement_map and not \
                    self.movement_map[pos].stay:
                valid = False
        return valid


class Movement:
    def __init__(self, can_go_right, can_go_left, can_go_up, can_go_down, can_stay):
        """
        Initialize a Movement object with the specified movement capabilities.

        Args:
            can_go_right (bool): Whether the movement can go right.
            can_go_left (bool): Whether the movement can go left.
            can_go_up (bool): Whether the movement can go up.
            can_go_down (bool): Whether the movement can go down.
            can_stay (bool): Whether the movement can stay.
        """
        self.right = can_go_right
        self.left = can_go_left
        self.up = can_go_up
        self.down = can_go_down
        self.stay = can_stay
