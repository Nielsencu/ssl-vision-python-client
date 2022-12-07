from dataclasses import dataclass
from typing import List

@dataclass
class RobotCommand:
    id : int
    velX : float
    velY : float
    yaw : float
    kickSpeedX : float = 0.0
    kickSpeedZ : float = 0.0
    spinner : bool = False
    wheelsSpeed : bool = False
    wheel1 : float = 0.0
    wheel2 : float = 0.0
    wheel3: float = 0.0
    wheel4: float = 0.0

@dataclass
class GRSimPacket:
    timeStamp: float
    isYellowTeam : bool
    robotCommands : List[RobotCommand]
