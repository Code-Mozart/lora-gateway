import asyncio
import codecs

from SX127x.LoRa import *
from SX127x.board_config import BOARD

from messageHandler import MessageHandler


class LoraImpl(LoRa):
    def __init__(self, message_handler: MessageHandler):
        super(LoraImpl, self).__init__(False)
        self.lora_setup()
        self.message_handler: MessageHandler = message_handler

    def lora_setup(self):
        print("setup")
        self.set_freq(433.0)
        self.set_spreading_factor(8)
        self.set_bw(BW.BW125)
        self.set_mode(MODE.RXCONT)
        print(self.get_version())

    def on_rx_done(self):
        # payload must be read from lora board!
        payload = self.read_payload(nocheck=True)
        # print("RX:")
        # print(payload)
        # print(codecs.decode(bytes(payload), "utf-8"))

        message = self.message_handler.decode_message(payload)
        block = self.message_handler.handle(message)

        # .handle(message) whatever is returned should be send via LoRa.
        # currently its either a missing update block for the mesh network
        # or
        # a response/ack for the hop network

        # if block is not None:
        print(message)

        # RESET module after receive!
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        BOARD.led_off()
        self.set_mode(MODE.RXCONT)

    def on_tx_done(self):
        # tx?
        print("tx")

    # def lora_write(self):
    #    # self.write_payload()
    #    print("write")

    async def lora_listen(self):
        self.set_mode(MODE.RXCONT)  # receiver mode
        while True:
            # self.read_payload()
            # send http request to backend
            # self.http_impl.send_data()
            # handle request
            # print("read")
            await asyncio.sleep(10)

# TODO: pip install RPi.GPIO & pip install spidev failed
