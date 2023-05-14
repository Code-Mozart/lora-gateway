from SX127x.LoRa import *
from http import HTTPStatus

import httpImpl
import time


class LoraImpl(LoRa):
    def __init__(self):
        super(LoraImpl, self).__init__(False)
        self.set_mode(MODE.SLEEP)

    def lora_setup(self):
        print("setup")
        self.set_mode(MODE.STDBY)
        self.set_freq(433.0)

    def on_rx_done(self):
        # rx?
        print("rx")

    def on_tx_done(self):
        # tx?
        print("tx")

    def lora_listen(self):
        self.set_mode(MODE.RXCONT)  # receiver mode
        time.sleep(5)
        while True:
            # self.read_payload()
            # send http request to backend
            httpImpl.send_data()
            # handle request
            print("read")
            time.sleep(10)

    def lora_write(self):
        # self.write_payload()
        print("write")

# TODO: pip install RPi.GPIO & pip install spidev failed
