#!/usr/bin/python3
"""
This module deploys the web_static archive to the servers.
"""

from os.path import exists
from fabric.api import *
import shlex
from fabric import task

env.hosts = ['54.237.43.214', '54.208.103.110']
env.user = 'ubuntu'


@task
def do_deploy(archive_path):
    """Deploy web_static."""
    if not exists(archive_path):
        return False

    try:
        ar_name = archive_path.replace('/', ' ')
        ar_name = shlex.split(ar_name)
        ar_name = ar_name[-1]

        bare_ar_name = ar_name.replace('.', ' ')
        bare_ar_name = shlex.split(bare_ar_name)
        bare_ar_name = bare_ar_name[0]

        releases_path = "/data/web_static/releases/{}/".format(bare_ar_name)
        tmp_path = "/tmp/{}".format(ar_name)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(releases_path))
        run("tar -xzf {} -C {}".format(tmp_path, releases_path))
        run("rm {}".format(tmp_path))
        run("mv {}web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}web_static".format(releases_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(releases_path))
        print("New version deployed!")
        return True
    except Exception:
        return False

# do_deploy('/home/vagrant/AirBnB_clone_v2/versions/web_static_20230907130838.tgz')
