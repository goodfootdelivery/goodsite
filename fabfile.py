#   GoodFoot Delivery Fabric
#       Fri  1 Apr 11:15:39 2016

from __future__ import with_statement
from fabric.api import settings, local, run, cd, env
from fabric.context_managers import prefix

# Path Configuration
REPO = 'https://github.com/connorsullivan/goodfoot.git'
SERVER = '/home2/goodfop0/gamma/goodfoot'

# Environment Variables
env.hosts = ['goodfootdelivery.com']
env.user = 'goodfop0'
env.password = 'Redmond2013!'


# Local Tasks TBE Before Deployment
def prepare():
    local('./manage.py check')
    local('pip freeze > requirements.txt')


# Deploy Project Using Git
def deploy():
    prepare()
    with cd(SERVER), prefix('workon goodfoot'):
        run('git checkout .')
        run('git pull')
        # Install Python Packages
        with settings(warn_only=True):
            run('pip install -r requirements.txt')
        # run('./manage.py makemigrations --merge')
        run('./manage.py migrate')
        run('./manage.py loaddata fixtures/*')
        run('./manage.py collectstatic')
