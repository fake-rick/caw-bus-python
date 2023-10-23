from CawBusPython import *
import time
import signal

state = True

def signal_handler(signum, frame):
    global state
    state = False

signal.signal(signal.SIGINT, signal_handler)

tran = CAN.CAN_Transmit(
    can_interface='slcan', 
    can_channel='COM16', 
    can_bitrate=500000)

tran.open()

m0 = Protocol.Protocol(0, tran)
cmd_start = Protocol.CMD(Protocol.CMDEnum.START, Protocol.ActionEnum.SET, 0, 0)
cmd_stop = Protocol.CMD(Protocol.CMDEnum.STOP, Protocol.ActionEnum.SET, 0, 0)
target = Protocol.CMD(Protocol.CMDEnum.TARGET, Protocol.ActionEnum.SET, 2, 0.00)

m0.request(cmd_start)
m0.request(Protocol.CMD(Protocol.CMDEnum.CONTROL_TYPE, Protocol.ActionEnum.SET, 0, Protocol.ControlType.VELOCITY))
m0.request(Protocol.CMD(Protocol.CMDEnum.VELOCITY_SP, Protocol.ActionEnum.SET, 2, 0.00))
while state:
    data = input("=> ")
    cmd_list = data.split(' ')
    if len(cmd_list) != 2: continue
    if cmd_list[0] == 'v':
        m0.request(Protocol.CMD(Protocol.CMDEnum.CONTROL_TYPE, Protocol.ActionEnum.SET, 0, Protocol.ControlType.VELOCITY))
        m0.request(Protocol.CMD(Protocol.CMDEnum.VELOCITY_SP, Protocol.ActionEnum.SET, 2, 0.00))
        target.set_data(float(cmd_list[1]))
        m0.request(target)
    elif cmd_list[0] == 'a':
        m0.request(Protocol.CMD(Protocol.CMDEnum.CONTROL_TYPE, Protocol.ActionEnum.SET, 0, Protocol.ControlType.ANGLE))
        m0.request(Protocol.CMD(Protocol.CMDEnum.VELOCITY_SP, Protocol.ActionEnum.SET, 2, 1000.00))
        target.set_data(float(cmd_list[1]))
        m0.request(target)
    elif cmd_list[0] == 't':
        m0.request(Protocol.CMD(Protocol.CMDEnum.CONTROL_TYPE, Protocol.ActionEnum.SET, 0, Protocol.ControlType.TORQUE))
        m0.request(Protocol.CMD(Protocol.CMDEnum.VELOCITY_SP, Protocol.ActionEnum.SET, 2, 0.00))
        target.set_data(float(cmd_list[1]))
        m0.request(target)
    elif cmd_list[0] == 'g' and cmd_list[1] == 'c':
        (id, value, state) = m0.request(Protocol.CMD(Protocol.CMDEnum.CURRENT_VALUE, Protocol.ActionEnum.GET, 0, 0))
        if state: print(f"id: {id} @ current: {value}")
    
tran.close()