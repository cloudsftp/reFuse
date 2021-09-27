#!/usr/bin/env python

"""
remarkable.py of reFuse
Copyright (C) 2021 Fabian Weik

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see https://www.gnu.org/licenses/.
"""



from paramiko import SSHClient, AutoAddPolicy


REMARKABLE_DATA_DIR = '/mnt/reMarkable/.local/share/remarkable/xochitl'

def restart_xochitl(hostname: str):
    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    ssh_client.connect(hostname, username='root')

    ssh_client.exec_command('systemctl restart xochitl')

    ssh_client.close()
