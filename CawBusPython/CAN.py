import can
from typing import Tuple
from .Transmit import TransmitBase

class CAN_Transmit(TransmitBase):
    def __init__(self, can_interface, can_channel, can_bitrate) -> None:
        self._can_interface = can_interface
        self._can_channel = can_channel
        self._can_bitrate = can_bitrate
        self._can = None
        print("init finish...")
    
    def open(self) -> None:
        self._can = can.Bus(
            interface=self._can_interface,
            channel=self._can_channel,
            bitrate=self._can_bitrate
        )
    
    def send(self, arbitration_id, data) -> None:
        msg = can.Message(arbitration_id=arbitration_id,
                  data=data,
                  is_extended_id=False)
        self._can.send(msg, timeout=0.2)
    
    def recv(self)->Tuple[int, bytearray]:
        msg = self._can.recv()
        return (msg.arbitration_id, msg.data)

    def close(self) -> None:
        self._can.shutdown()


