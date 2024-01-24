from Models.Robot import Robot


class System:
    def __init__(self):
        self.robots = []


    def __str__(self):
        pass

    def add_robot(self, robot):
        self.robots.append(robot)

    def clear(self):
        self.robot.clear()