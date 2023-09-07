#!/usr/bin/python3
"""
This module deletes out-of-date archives.
"""
from fabric.api import *

env.hosts = ['54.237.43.214', '54.208.103.110']
env.user = 'ubuntu'


def do_clean(number=0):
    """Deletes out-of-date archives"""
    number = int(number)

    if number == 0 or number == 1:
        number = 2
    else:
        number += 1

    local(f'cd versions ; ls -t | tail -n +{number} | xargs rm -rf')
    run(f'cd /data/web_static/releases ;\
         ls -t | tail -n +{number} | xargs rm -rf')
