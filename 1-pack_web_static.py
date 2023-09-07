#!/usr/bin/python3
"""
This module generates a .tgz archive
from the contents of the web_static folder.
"""

from fabric.api import local
from os.path import exists
from datetime import datetime


def do_pack():
    """Pack web_static."""
    try:
        if not exists('versions'):
            local('mkdir versions')
        now = datetime.now()
        arc_path = f"versions/web_static_{now.strftime('%Y%m%d%H%M%S')}.tgz"
        local(f'tar -czvf {arc_path} web_static')
        return arc_path
    except Exception:
        return None
