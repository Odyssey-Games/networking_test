from common.src.packets.Packet import Packet


class LoginPacket(Packet):
    def __init__(self, token: str):
        self.token = token
