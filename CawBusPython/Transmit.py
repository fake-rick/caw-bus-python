from typing import Tuple
from abc import abstractmethod

class TransmitBase(object):
    @abstractmethod
    def open(self):
        """
        open the device
        """

    @abstractmethod
    def send(self, id: int, data: bytearray):
        """
        send data
        """ 

    @abstractmethod
    def recv(self)->Tuple[int, bytearray]:
        """
        send data
        """

    @abstractmethod
    def close(self):
        """
        close the device
        """
