import socket
from protobuf.messages_robocup_ssl_wrapper_pb2 import SSL_WrapperPacket
from protobuf.grSim_Packet_pb2 import grSim_Packet
from protobuf_to_dict import protobuf_to_dict
from grSimPacket import GRSimPacket, RobotCommand
from struct import pack


DEFAULT_COMMAND_PORT = 20011
TOTAL_ROBOTS_COUNT = 11

class SSLClient:
    def __init__(self,  ip = '224.5.23.2', port=10006):
        """
        Init SSLClient object.
        Extended description of function.
        Parameters
        ----------
        ip : str
            Multicast IP in format '255.255.255.255'. 
        port : int
            Port up to 1024. 
        """
        if not isinstance(ip, str):
            raise ValueError('IP type should be string type')
        if not isinstance(port, int):
            raise ValueError('Port type should be int type')
        self.ip = ip
        self.port = port

    def __enter__(self):
        """Binds the client with ip and port and configure to UDP multicast."""
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 128)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        self.sock.bind((self.ip, self.port))

        host = socket.gethostbyname(socket.gethostname())
        self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
        # TODO: Currently multicast is disabled as main.py uses 127.0.0.1 address instead of 224.0.0.0 and above
        # Not sure about the difference, but multicast sounds more fancy
        # self.sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, 
        #        socket.inet_aton(self.ip) + socket.inet_aton(host))
        return self

    def __exit__(self,  exc_type, exc_value, exc_tb):
        stopCommands = [RobotCommand(i, 0.0, 0.0, 0.0) for i in range(TOTAL_ROBOTS_COUNT)]
        desiredCommand = GRSimPacket(0.0, False, stopCommands)
        self.send(desiredCommand)
        desiredCommand = GRSimPacket(0.0, True, stopCommands)
        self.send(desiredCommand)
        
    def receive(self):
        """Receive package and decode."""
        wrapper_packet = SSL_WrapperPacket()
        data, len = self.sock.recvfrom(1024)
        try:
            wrapper_packet.ParseFromString(data)
        except Exception as e:
            # TODO: Debug error message : Error parsing message with type 'SSL_WrapperPacket'
            # Only minor concern as we can still get geometry packet, but its annoying
            ...
            #print(e)
        wrapper_packet = protobuf_to_dict(wrapper_packet)
        return wrapper_packet

    def send(self, desiredCommand : GRSimPacket):
        grsimPacket = grSim_Packet()

        grsimPacket.commands.timestamp = desiredCommand.timeStamp
        grsimPacket.commands.isteamyellow = desiredCommand.isYellowTeam

        for robotCommand in desiredCommand.robotCommands:
            command = grsimPacket.commands.robot_commands.add()
            command.id = robotCommand.id
            command.veltangent = robotCommand.velX
            command.velnormal = robotCommand.velY
            command.velangular = robotCommand.yaw
            command.kickspeedx = robotCommand.kickSpeedX
            command.kickspeedz = robotCommand.kickSpeedZ
            command.spinner = robotCommand.spinner
            command.wheelsspeed = robotCommand.wheelsSpeed
            command.wheel1 = robotCommand.wheel1
            command.wheel2 = robotCommand.wheel2
            command.wheel3 = robotCommand.wheel3
            command.wheel4 = robotCommand.wheel4
        return self.sock.sendto(grsimPacket.SerializeToString(), (self.ip, DEFAULT_COMMAND_PORT))