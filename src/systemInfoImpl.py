import platform
import psutil
import string
from datetime import datetime
from httpImpl import HttpImpl


# initiale registrierung des gateways am backend mit infos wie system, machine?
# dann müssen diese daten nicht jedes mal mitgeschickt werden

class SystemInfoImpl:
    def __init__(self, http_impl: HttpImpl):
        self.received_packages = 0
        self.send_packages = 0
        self.current_cpu_usage = None
        self.current_ram_usage = None
        self.start_time: datetime = datetime.now()
        self.current_time = None
        self.uptime = None
        self.system: string = None
        self.machine: string = None

    def __str__(self):
        return f'start_time: {self.start_time}\n' \
               f'current_time: {self.current_time}\n' \
               f'uptime: {self.uptime}\n' \
               f'system: {self.system}\n' \
               f'machine: {self.machine}\n' \
               f'current cpu usage: {self.current_cpu_usage}\n' \
               f'current ram usage: {self.current_ram_usage}\n' \
               f'received packages {self.received_packages}\n' \
               f'send packages {self.send_packages}\n' \
               f'------------------'

    def get_data(self):
        self.current_cpu_usage = psutil.cpu_percent()
        self.current_ram_usage = psutil.virtual_memory().percent
        self.current_time = datetime.now()
        self.uptime = self.current_time - self.start_time
        self.system = platform.system()
        self.machine = platform.machine()
        # TODO: core temp kann hier anscheinend geholt werden, klappt aber nicht unter windows
        # print(psutil.sensors_temperatures())
        return self
