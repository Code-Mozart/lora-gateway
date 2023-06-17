import asyncio
import json
import sys
from contextlib import suppress
from SX127x.board_config import BOARD

from uuid import uuid4
from dtos import UpdateDTO, BulkDataDTO
from httpImpl import HttpImpl
from systemInfoImpl import SystemInfoImpl
from util import DataSplitter
from loraImpl import LoraImpl
from messageHandler import MessageHandler, MessageHandlerMesh, MessageHandlerHop

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

async def pull_patch(minutes, data_splitter: DataSplitter, http_impl: HttpImpl, lora_impl: LoraImpl):
    # Disable because the backend is not yet ready
    return

    while True:
        update: UpdateDTO = http_impl.get_update()
        # TODO: compare version number to previous pulled patch
        data_splitter.set_new_data(update.data)

        while data_splitter.has_next_block():
            total_blocks, block_index, block = data_splitter.next_block()
            # TODO: write to LoRa here
            # print(total_blocks)
            # print(block_index)
            # print(block)

        await asyncio.sleep(minutes * 60)


async def send_system_info(minutes, system_info_impl: SystemInfoImpl, http_impl: HttpImpl, gateway_uuid: str):
    while True:
        data: BulkDataDTO = system_info_impl.get_data()
        http_impl.post_node_data_bulk(gateway_uuid, data)

        await asyncio.sleep(minutes * 60)


async def lora_listen(lora_impl: LoraImpl):
    await lora_impl.lora_listen()


async def main(mode: str = 'mesh'):
    valid_modes = {'mesh', 'hop'}

    if mode not in valid_modes:
        raise ValueError('mode must be one of %r' % valid_modes)

    with open('config.json') as json_file:
        data: dict = json.load(json_file)

    # generate uuid for gateway
    if 'uuid' not in data:
        uuid = str(uuid4())
        data['uuid'] = uuid

        with open('config.json', 'w') as json_file_write:
            json.dump(data, json_file_write)

    BOARD.setup()

    data_splitter: DataSplitter = DataSplitter(237)
    http_impl: HttpImpl = HttpImpl(data['host'])
    system_info_impl: SystemInfoImpl = SystemInfoImpl(http_impl)
    message_handler: MessageHandler = \
        MessageHandlerMesh(http_impl, data_splitter) if mode == 'mesh' else MessageHandlerHop(http_impl, data_splitter)
    lora_impl: LoraImpl = LoraImpl(message_handler)

    # TODO: adjust interval times (e.g. patch every 24 hours, system info every 10 minutes)
    pull_patch_task = asyncio.Task(pull_patch(0.08, data_splitter, http_impl, lora_impl))
    system_info_task = asyncio.Task(send_system_info(0.016, system_info_impl, http_impl, data['uuid']))
    lora_listen_task = asyncio.Task(lora_listen(lora_impl))

    with suppress(asyncio.CancelledError):
        await pull_patch_task
        await system_info_task
        await lora_listen_task


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    # should take 'mesh' as default if not specified via command line
    # start via cmd line in mesh mode: python main.py mesh
    # start via cmd line in hop mode: python main.py hop
    if len(sys.argv) == 1:
        loop.run_until_complete(main())
    else:
        loop.run_until_complete(main(sys.argv[1]))
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
