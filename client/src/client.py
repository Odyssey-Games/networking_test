import pickle
from socket import socket, AF_INET, SOCK_DGRAM

from common.src.common import print_hi
from common.src.packets.Packet import Packet
from common.src.packets.c2s.HelloPacket import HelloPacket
from common.src.packets.c2s.RequestInfoPacket import RequestInfoPacket
from common.src.packets.s2c.InfoReplyPacket import InfoReplyPacket


class Client:
    def __init__(self, address: tuple):
        self.address = address
        self.socket = socket(AF_INET, SOCK_DGRAM)

    def send_packet(self, packet: Packet):
        data = pickle.dumps(packet)
        self.socket.sendto(data, self.address)

    def rcv(self, bufsize: int):
        data, addr = self.socket.recvfrom(bufsize)
        packet = pickle.loads(data)
        if not isinstance(packet, Packet):
            print(f"Received invalid packet: {packet}")
            return None
        return packet


if __name__ == '__main__':
    print_hi('Client')
    # Sent a message to the server

    client = Client(('localhost', 5000))

    login_packet = HelloPacket('Cool Client Name')
    client.send_packet(login_packet)

    request_info_packet = RequestInfoPacket()
    client.send_packet(request_info_packet)

    info_reply = client.rcv(1024)
    if isinstance(info_reply, InfoReplyPacket):
        print(f"Received info reply with {info_reply.player_count} players and state {info_reply.state}")
