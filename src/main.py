import asyncio
import json
from contextlib import suppress
from SX127x.board_config import BOARD

from dtos import UpdateDTO
from httpImpl import HttpImpl
from systemInfoImpl import SystemInfoImpl
from util import DataSplitter
from loraImpl import LoraImpl

import time

# pylora https://pypi.org/project/pyLoRa/
# https://github.com/rpsreal/pySX127x
# https://github.com/rpsreal/pySX127x/blob/master/LORA_SERVER.py

# https://pypi.org/project/async-cron/

# SETUP:
# pip install RPi.GPIO
# pip install spidev
# pip install pyLoRa
# pip install psutil

async def pull_patch(minutes, http_impl: HttpImpl, lora_impl: LoraImpl):
    while True:
        update: UpdateDTO = http_impl.get_update()
        ds: DataSplitter = DataSplitter(update.data, 237)  # chunk size according to spezification

        while ds.has_next_chunk():
            chunk = ds.next_chunk()
            print(chunk)
            # lora_impl.write_payload(chunk)

        await asyncio.sleep(minutes * 60)


async def send_system_info(minutes, system_info_impl: SystemInfoImpl):
    while True:
        system_info_impl.get_data()
        await asyncio.sleep(minutes * 60)


async def lora_listen(lora_impl: LoraImpl):
    await lora_impl.lora_listen()


async def main():
    with open('config.json') as json_file:
        data = json.load(json_file)

    BOARD.setup()

    http_impl = HttpImpl(data['host'])
    system_info_impl = SystemInfoImpl(http_impl)
    lora_impl = LoraImpl(http_impl)

    pull_patch_task = asyncio.Task(pull_patch(0.08, http_impl, lora_impl))
    system_info_task = asyncio.Task(send_system_info(0.016, system_info_impl))
    lora_listen_task = asyncio.Task(lora_listen(lora_impl))

    with suppress(asyncio.CancelledError):
        await pull_patch_task
        await system_info_task
        await lora_listen_task



loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
