#!/usr/bin/python3
"""
This module deploys the web_static archive to the servers.
"""

from os.path import exists
from fabric.api import *
import shlex

env.hosts = ['54.237.43.214', '54.208.103.110']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Deploy web_static."""
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1].split('.')[0]
        release_path = f"/data/web_static/releases/{archive_name}/"
        tmp_path = f'/tmp/{archive_name}.tgz'

        put(archive_path, '/tmp/')
        run(f'mkdir -p {release_path}')
        run(f'tar -xzf {tmp_path} -C {release_path}')
        run(f'rm -f {tmp_path}')
        # move uncompressed content out of its uncompressed directory
        run(f'mv {release_path}web_static/* {release_path}')
        # rm the empty uncompressed directory web_static
        run(f'rm -rf {release_path}web_static')
        run(f'rm -rf /data/web_static/current')
        run(f'ln -s {release_path} /data/web_static/current')
        print("New version deployed!")
        return True
    except Exception:
        return False

# do_deploy('/home/vagrant/AirBnB_clone_v2/versions/web_static_20230907130838.tgz')
