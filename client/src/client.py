import pickle
from socket import socket, AF_INET, SOCK_DGRAM

from common.src.common import print_hi
from common.src.packets.Packet import Packet
from common.src.packets.c2s.LoginPacket import LoginPacket


class Client:
    def __init__(self, address: tuple):
        self.address = address
        self.socket = socket(AF_INET, SOCK_DGRAM)

    def send_packet(self, packet: Packet):
        data = pickle.dumps(packet)
        self.socket.sendto(data, self.address)


if __name__ == '__main__':
    print_hi('Client')
    # Sent a message to the server

    client = Client(('localhost', 5000))
    login_packet = LoginPacket('my_token')
    client.send_packet(login_packet)
