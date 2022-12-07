from client import SSLClient
import time
import sys
from grSimPacket import GRSimPacket, RobotCommand

if __name__ == "__main__":
    with SSLClient(ip="127.0.0.1", port=10006) as client:
        if len(sys.argv) <=1:
            raise RuntimeError("Please add another argument send/receive")
        while True:
            if sys.argv[1] == 'send':
                robotCommands = []
                robotCommands.append(RobotCommand(0, -0.1, 0.0, 0.0))
                desiredCommand = GRSimPacket(0.0, True, robotCommands)
                sent = client.send(desiredCommand)
                desiredCommand = GRSimPacket(0.0, False, robotCommands)
                sent = client.send(desiredCommand)
            else:
                pack = client.receive()
                detection_packet = pack.get('detection', None)
                if detection_packet:
                    print("Detection packet:\n", detection_packet, '\n')
                geometry_packet = pack.get('geometry', None)
                if geometry_packet:
                    print("Geometry packet:\n", geometry_packet, '\n')
