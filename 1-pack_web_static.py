#!/usr/bin/python3
"""A Fabric 3.1.14 script that generates a .tgz archive from the web_static dir
"""

from fabric.api import local
from os.path import exists, getsize
from os import mkdir
from datetime import datetime


def do_pack():
    """Pack the web_static dir into web_static_<datetime>.tgz"""

    try:
        # create the versions dir if not exist and store the archive inside
        if not exists('versions'):
            mkdir('versions')

        # get the current datetime to generate the archive name
        datetime_str = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_path = f"versions/web_static_{datetime_str}.tgz"

        # create the archive inside versions/ directory
        print(f'Packing web_static to {archive_path}')
        result = local(f'tar -czvf {archive_path} web_static')
        if result.failed:
            raise Exception

        size = getsize(archive_path)
        print(f'webstatic packed: {archive_path} -> {size}Bytes')

        return archive_path
    except Exception:
        return None
