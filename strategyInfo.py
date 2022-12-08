from dataclasses import dataclass, field
from typing import List

class FieldInfo:
    # TODO: Process raw field info data
    ...

@dataclass
class BallInfo:
    x: float
    y: float
    confidence: float

@dataclass
class RobotState:
    x : float
    y : float 
    yaw : float # [-pi,pi]
    confidence : float  # [0,1]

class StrategyInfo:
    def __init__(self):
        self. fieldInfo = FieldInfo()
        self.ballInfo = BallInfo(0.0, 0.0, 0.0)
        self.yellowRobotStates = [RobotState(0.0, 0.0, 0.0, 0.0) for i in range(11)]
        self.blueRobotStates = [RobotState(0.0, 0.0, 0.0, 0.0) for i in range(11)]

    def __str__(self):
        str_rep = f"""Ball location (Conf. {self.ballInfo.confidence}): {self.ballInfo.x}, {self.ballInfo.y}\n"""
        for idx, robot in enumerate(self.yellowRobotStates):
            str_rep += f'Robot {idx} (Conf. {robot.confidence}): \nX:{robot.x}\nY:{robot.y}\nYaw:{robot.yaw}\n'
        for idx, robot in enumerate(self.blueRobotStates):
            str_rep += f'Robot {idx} (Conf. {robot.confidence}): \nX:{robot.x}\nY:{robot.y}\nYaw:{robot.yaw}\n'
        return str_rep