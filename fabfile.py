####    GoodFoot Delivery Fabric    ###
####    Wed 30 Mar 16:36:19 2016    ###

from fabric.api import local

def hello():
    print('Hello World')

def prepare():
    local('./manage.py check')
    local('./config.sh')
