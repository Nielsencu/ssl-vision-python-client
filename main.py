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
                robotCommands = []
                robotCommands.append(RobotCommand(0, -0.1, 0.0, 0.0))
                desiredCommand = GRSimPacket(0.0, True, robotCommands)
                client.send(desiredCommand)
                desiredCommand = GRSimPacket(0.0, False, robotCommands)
                client.send(desiredCommand)
            else:
                packet = client.receive()
                # Packet handler will update strategyInfo on handle
                packetHandler.handle(packet)
                print(f'{strategyInfo}')

                

