import pickle
import secrets
from socket import *

from common.src.common import print_hi
from common.src.packets.Packet import Packet
from common.src.packets.c2s.HelloPacket import HelloPacket
from common.src.packets.c2s.RequestInfoPacket import RequestInfoPacket
from common.src.packets.s2c.HelloReplyPacket import HelloReplyPacket
from common.src.packets.s2c.InfoReplyPacket import InfoReplyPacket
from User import User


class Server:
    clients: list[User]

    def __init__(self, address: tuple):
        self.clients = []
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(address)

    def send_packet(self, packet, addr: tuple):
        data = pickle.dumps(packet)
        self.socket.sendto(data, addr)

    def rcvfrom(self, bufsize: int):
        data, addr = self.socket.recvfrom(bufsize)
        packet = pickle.loads(data)
        if not isinstance(packet, Packet):
            print(f"Received invalid packet: {packet}")
            return None, None
        return packet, addr


if __name__ == '__main__':
    """The main server entry point.
    
    Currently one server instance means one "game".
    """
    print_hi('Server')

    server = Server(('localhost', 5000))
    while True:
        client_packet, client_addr = server.rcvfrom(1024)
        print(f"Received {client_packet} from {client_addr}")
        if isinstance(client_packet, HelloPacket):
            if client_packet.name in [client.name for client in server.clients]:
                print(f"Client with name {client_packet.name} already exists.")
                continue
            print(f"Client with name {client_packet.name} connected.")
            token = secrets.token_hex(16)
            user = User(client_packet.name, client_addr, token)
            server.clients.append(user)
            reply_packet = HelloReplyPacket(token)
            server.send_packet(reply_packet, client_addr)

        elif isinstance(client_packet, RequestInfoPacket):
            print(f"Received info request from {client_addr}")
            player_count = len(server.clients)
            reply_packet = InfoReplyPacket('Hello World!', player_count, 'lobby')
            server.send_packet(reply_packet, client_addr)
