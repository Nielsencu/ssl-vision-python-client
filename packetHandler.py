from strategyInfo import StrategyInfo

class PacketHandler:
    def __init__(self, strategyInfo : StrategyInfo):
        self.strategyInfo = strategyInfo

    def handle(self, packet):
        geometry_packet = packet.get('geometry')
        if geometry_packet:
            return self._handleGeometryPacket(geometry_packet)
        detection_packet = packet.get('detection')
        if detection_packet:
            return self._handleDetectionPacket(detection_packet)

    def _handleGeometryPacket(self, packet):
        # TODO: Update strategyInfo field 
        # print("Geometry packet:\n", packet, '\n')
        ...

    def _handleDetectionPacket(self, packet):
        def copyRobotState(robotStates, destRobotStates):
            for robotState in robotStates:
                id = robotState['robot_id']
                destRobotState = destRobotStates[id]
                destRobotState.confidence = robotState['confidence']
                destRobotState.x = robotState['x']
                destRobotState.y = robotState['y']
                destRobotState.yaw = robotState['orientation']
        # TODO: Shoiuld take into account the possibility of having multiple balls
        balls = packet.get("balls")[0]
        if balls:
            self.strategyInfo.ballInfo.x = balls['x']
            self.strategyInfo.ballInfo.y = balls['y']
            self.strategyInfo.ballInfo.confidence = balls['confidence']
        yellowRobotStates = packet.get("robots_yellow")
        if yellowRobotStates:
            copyRobotState(yellowRobotStates, self.strategyInfo.yellowRobotStates)
        blueRobotStates = packet.get("robots_blue")
        if blueRobotStates:
            copyRobotState(blueRobotStates, self.strategyInfo.blueRobotStates)
