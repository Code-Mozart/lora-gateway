import platform
import string
from datetime import datetime


class SystemInfoImpl:
    def __init__(self):
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
               f'machine: {self.machine}'

    def get_data(self):
        # print("collecting system info")
        self.current_time = datetime.now()
        self.uptime = self.current_time - self.start_time
        self.system = platform.system()
        self.machine = platform.machine()
        return self
