#!/usr/bin/env python

from paramiko import SSHClient, AutoAddPolicy


REMARKABLE_DATA_DIR = '/mnt/reMarkable/.local/share/remarkable/xochitl'

def restart_xochitl(hostname: str):
    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    ssh_client.connect(hostname, username='root')

    ssh_client.exec_command('systemctl restart xochitl')

    ssh_client.close()
