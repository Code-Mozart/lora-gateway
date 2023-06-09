import asyncio
import json
from systemInfoImpl import SystemInfoImpl
from contextlib import suppress

from loraImpl import LoraImpl
from systemInfoImpl import SystemInfoImpl
from httpImpl import HttpImpl


# pylora https://pypi.org/project/pyLoRa/
# https://github.com/rpsreal/pySX127x
# https://github.com/rpsreal/pySX127x/blob/master/LORA_SERVER.py

# https://pypi.org/project/async-cron/

# SETUP:
# pip install RPi.GPIO
# pip install spidev
# pip install pyLoRa
# pip install psutil

async def pull_patch(minutes):
    while True:
        print('pull patch ...')
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

    system_info_impl = SystemInfoImpl()
    http_impl = HttpImpl(data['host'], data['port'])
    lora_impl = LoraImpl(http_impl)

    pull_patch_task = asyncio.Task(pull_patch(0.08))
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
