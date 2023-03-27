import pickle
from socket import *

from common.src.common import print_hi
from common.src.packets.Packet import Packet
from common.src.packets.c2s.LoginPacket import LoginPacket

if __name__ == '__main__':
    print_hi('Server')

    # Create a simple udp socket listener
    with socket(AF_INET, SOCK_DGRAM) as s:
        s.bind(('localhost', 5000))
        print("Listening on port 5000")
        while True:
            data, addr = s.recvfrom(1024)
            print(f"Received {data} from {addr}")
            packet = pickle.loads(data)
            if not isinstance(packet, Packet):
                print(f"Received invalid packet: {packet}")
                continue

            print(f"Received packet: {packet}")
            if isinstance(packet, LoginPacket):
                print(f"Received login packet with token {packet.token}")
