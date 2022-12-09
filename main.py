from client import SSLClient
import time
import sys
from grSimPacket import GRSimPacket, RobotCommand
from strategyInfo import StrategyInfo
from packetHandler import PacketHandler

if __name__ == "__main__":
    with SSLClient(ip="127.0.0.1", port=10006) as client:
        if len(sys.argv) <=1:
            raise RuntimeError("Please add another argument send/receive")
        strategyInfo = StrategyInfo()
        packetHandler = PacketHandler(strategyInfo)
        while True:
            if sys.argv[1] == 'send':
                client.moveBlueRobot(3, 0.1, 0.0, 0.0)
                client.moveYellowRobot(3, 0.1, 0.0, 0.0)
            else:
                # This will run on a separate thread on the real application
                packet = client.receive()
                packetHandler.handle(packet)
                print(f'{strategyInfo}')

                

