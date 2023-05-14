import asyncio

from httpImpl import HttpImpl
from async_cron.job import CronJob
from async_cron.schedule import Scheduler

from loraImpl import LoraImpl

# pylora https://pypi.org/project/pyLoRa/
# https://github.com/rpsreal/pySX127x
# https://github.com/rpsreal/pySX127x/blob/master/LORA_SERVER.py

# https://pypi.org/project/async-cron/

if __name__ == '__main__':
    loraImpl = LoraImpl()
    loraImpl.lora_setup()
    loraImpl.lora_listen()

    scheduler = Scheduler()
    job = CronJob(name='backendPull').every(5).second.go(loraImpl.lora_write)
    scheduler.add_job(job)
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(scheduler.start())
    except KeyboardInterrupt:
        print("exit")



