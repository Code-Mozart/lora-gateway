from SX127x.LoRa import *
from SX127x.board_config import BOARD

from http import HTTPStatus
from httpImpl import HttpImpl

import httpImpl
import time

import codecs

class LoraImpl(LoRa):
    def __init__(self, http_impl: HttpImpl):
        super(LoraImpl, self).__init__(False)
        self.lora_setup()
        self.http_impl: HttpImpl = httpImpl
        

    def lora_setup(self):
        print("setup")
        self.set_freq(433.0)
        self.set_spreading_factor(8)
        self.set_bw(BW.BW125)
        self.set_mode(MODE.RXCONT)
        print(self.get_version())

        while(True):
            time.sleep(5)

    def on_rx_done(self):
        # payload must be read from lora board!
        payload = self.read_payload(nocheck=True) 
        print("RX:")
        print(payload)
        print(codecs.decode(bytes(payload),"utf-8"))
        #RESET module after receive!
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        BOARD.led_off()
        self.set_mode(MODE.RXCONT)


    def on_tx_done(self):
        # tx?
        print("tx")

    #def lora_write(self):
    #    # self.write_payload()
    #    print("write")

    def lora_listen(self):
        self.set_mode(MODE.RXCONT)  # receiver mode
        time.sleep(5)
        while True:
            # self.read_payload()
            # send http request to backend
            #self.http_impl.send_data()
            # handle request
            #print("read")
            time.sleep(10)


# TODO: pip install RPi.GPIO & pip install spidev failed
