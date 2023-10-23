from .Transmit import TransmitBase
from typing import Tuple

# |cmd|action(0:set 1:get)|version|accuracy(0:int32)|data(4bytes)|

byteorder = 'big'

VERSION = 0x05 # 0b00000101 (v1.01)

class ControlType:
    TORQUE = 0x00
    VELOCITY = 0x01
    ANGLE = 0x02
    VELOCITY_OPENLOOP = 0x03
    ANGLE_OPENLOOP = 0x04

class CMDEnum:
    STOP = 0x00
    START = 0x01
    CONTROL_TYPE = 0x02
    CURRENT_P = 0x03
    CURRENT_I = 0x04
    CURRENT_D = 0x05
    VELOCITY_P = 0x06
    VELOCITY_I = 0x07
    VELOCITY_D = 0x08
    ANGLE_P = 0x09
    ANGLE_I = 0x0A
    ANGLE_D = 0x0B
    LPF_CURRENT = 0x0C
    LPF_VELOCITY = 0x0D
    LPF_ANGLE = 0x0E
    VELOCITY_SP = 0x0F # shaft_velocity_sp
    TARGET = 0x10
    CURRENT_VALUE = 0x11
    VELOCITY_VALUE = 0x12
    ANGLE_VALUE = 0x13
    REPLY = 0xff

class ActionEnum:
    NONE = 0x00
    SET = 0x01
    GET = 0x02

class CMD:
    def __init__(self, cmd:int, action:int, accuracy:int, data:float) -> None:
        if accuracy > 0:
            data = data * 10 ** accuracy
        self._cmd = cmd
        self._action = action
        self._accuracy = accuracy
        self._version = VERSION
        self._data = int(data)

    def set_cmd(self, cmd:int):
        self._cmd = cmd
    
    def set_action(self, action:int):
        self._action = action
    
    def set_accuracy(self, accuracy:int):
        self._accuracy = accuracy
    
    def set_data(self, data:float):
        if self._accuracy > 0:
            data = data * 10 ** self._accuracy
        self._data = int(data)

class Protocol:
    def __init__(self, id:int, transmit:TransmitBase) -> None:
        self._transmit = transmit
        self._id = id
    
    def request(self, cmd:CMD) -> Tuple[int,float,bool]:
        data = bytearray([cmd._cmd, cmd._action, cmd._version, cmd._accuracy])
        data += bytearray(cmd._data.to_bytes(4, byteorder, signed=True))
        self._transmit.send(self._id, data)
        (id, recv_data) = self._transmit.recv()
        if recv_data[0] != CMDEnum.REPLY or recv_data[2] != VERSION:
            return (0, 0, False)
        data = float(int.from_bytes(recv_data[4:], byteorder))
        if recv_data[3] != 0: data / 10 ** recv_data[3]
        return (id, data, True) 