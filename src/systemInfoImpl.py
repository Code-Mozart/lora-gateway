import platform
from datetime import datetime

import psutil

from httpImpl import HttpImpl


# initiale registrierung des gateways am backend mit infos wie system, machine?
# dann müssen diese daten nicht jedes mal mitgeschickt werden

class SystemInfoImpl:
    def __init__(self, http_impl: HttpImpl):
        # updated by method
        self.cpu_load = None
        self.ram_usage = None
        self.system_time: datetime = None

        # fixed values
        self.started_at: datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.system = f'{platform.system()} {platform.release()}'

        # updated when receiving packages
        self.received_packages = 0
        self.last_package_received: datetime = None

        # updated when sending packages
        self.sent_packages = 0
        self.last_package_sent: datetime = None

    def __str__(self):
        return f'cpu_load: {self.cpu_load}\n' \
               f'ram_usage: {self.ram_usage}\n' \
               f'started_at: {self.started_at}\n' \
               f'system_time: {self.system_time}\n' \
               f'system: {self.system}\n' \
               f'received_packages: {self.received_packages}\n' \
               f'sent_packages: {self.sent_packages}\n' \
               f'last_package_received: {self.last_package_received}\n' \
               f'last_package_sent: {self.last_package_sent}\n' \
               f'------------------'

    def get_data(self):
        self.cpu_load = psutil.cpu_percent()
        self.ram_usage = psutil.virtual_memory().percent
        self.system_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        return self

    def update_on_package_receive(self):
        self.received_packages = self.received_packages + 1
        self.last_package_received = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    def update_on_package_sent(self):
        self.sent_packages = self.sent_packages + 1
        self.last_package_sent = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
