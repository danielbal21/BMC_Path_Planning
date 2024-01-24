class Robot:
    def __init__(self):
        self.movement_map = {}
        self.initial_pos = None

    def clear(self):
        self.movement_map = {}
        self.initial_pos = None

    def add_movement(self, row, column, can_go_right, can_go_left, can_go_up, can_go_down, can_stay, is_initial):
        self.movement_map[(row, column)] = Movement(can_go_right, can_go_left, can_go_up, can_go_down, can_stay)

        if not can_go_up and not can_go_down and not can_go_right and not can_go_left and not can_stay:
            if (row, column) in self.movement_map:
                self.movement_map.pop((row, column))

        if is_initial:
            self.initial_pos = (row, column)

        if self.initial_pos == (row, column) and not is_initial:
            is_initial = None

    def movement_get(self, row, col):
        if (row, col) in self.movement_map:
            return self.movement_map[(row, col)]
        else:
            return None

    def is_valid(self):
        valid = True

        # check if this robot has an initial position
        if self.initial_pos == None:
            valid = False

        # check if every movement has at least one defined direction
        for pos in self.movement_map:
            if self.can_move_in_any_direction(self.movement_map[pos]) == False:
                valid = False

        if self.initial_pos not in self.movement_map:
            valid = False

        return valid and self.is_closed_loop()

    def can_move_in_any_direction(self,movement):
        if movement is None: return False
        return movement.up == True or movement.down == True or movement.left == True or movement.right == True or movement.stay == True

    def is_closed_loop(self):
        valid = True
        for pos in self.movement_map:
            if self.movement_map[pos].up and not (pos[0] - 1, pos[1]) in self.movement_map and not self.movement_map[pos].stay:
                valid = False
            elif self.movement_map[pos].down and not (pos[0] + 1, pos[1]) in self.movement_map and not self.movement_map[pos].stay:
                valid = False
            elif self.movement_map[pos].right and not (pos[0], pos[1] + 1) in self.movement_map and not self.movement_map[pos].stay:
                valid = False
            elif self.movement_map[pos].left and not (pos[0], pos[1] - 1) in self.movement_map and not self.movement_map[pos].stay:
                valid = False
        return valid
class Movement:
    def __init__(self, can_go_right, can_go_left, can_go_up, can_go_down, can_stay):
        self.right = can_go_right
        self.left = can_go_left
        self.up = can_go_up
        self.down = can_go_down
        self.stay = can_stay
