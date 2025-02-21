import serial
import sys
import time
import struct
from openc3.interfaces.tcpip_server_interface import TcpipServerInterface
from openc3.packets.packet import Packet

port = 2945
if len(sys.argv) > 2:
    port = sys.argv[2]

a = TcpipServerInterface(port, port, 10, None, "BURST")
a.connect()

id = 1 # This is for testing with COSMOS. Every pkt needs and ID and PROVESKit does not have IDs.


with serial.Serial(sys.argv[1], 115200) as ser:
    while True:
        data = ser.read_until(b"\n")
        pkt_len = len(data)
        pkt = struct.pack(f"bb{pkt_len}s", id, pkt_len, data)
        packet = Packet()
        packet.buffer = pkt
        a.write(packet)
