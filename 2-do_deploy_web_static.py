#!/usr/bin/python3
"""A Fabric 3.1.14 script to manage my servers deployment"""

from fabric.api import local, env, put, run
from os.path import exists, getsize, basename, join
from os import mkdir
from datetime import datetime

env.user = 'ubuntu'  # servers username
env.hosts = ['54.162.238.187', '54.175.189.248']  # servers ip addresses


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


def do_deploy(archive_path):
    """Deploys the packed web_static directory state to my servers"""

    try:
        # check if archive exists otherwise return False
        if not exists(archive_path):
            return False

        archive_name = basename(archive_path)
        tmp_path = join('/tmp', archive_name)
        root_path = '/data/web_static/releases'

        # remove the last 4 chars from the archive_name '.tgz'
        release_path = join(root_path, archive_name[:-4] + '/')

        # upload the archive to the server
        put(archive_path, tmp_path)

        # decompress the archive
        sudo(f"mkdir -p {release_path}")
        sudo(f"tar -xzf {tmp_path} -C {release_path}")
        sudo(f"rm {tmp_path}")
        sudo(f"mv {release_path}web_static/* {release_path}")
        sudo(f"rm -rf {release_path}web_static")
        sudo("rm -rf /data/web_static/current")
        sudo(f"ln -s {release_path} /data/web_static/current")
        print('New version deployed!')

    except Exception:
        return False

    return True
