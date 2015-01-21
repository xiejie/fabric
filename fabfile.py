#!/usr/bin/env python
#coding=utf-8
from fabric.api import *
from contextlib import *
from fabric.contrib.files import exists
from fabric.colors import *

"""
File: fabfile.py
Author: Xiejie <xiejie2104@gmail.com>
TODO: 
    rsync_project
    fabric.contrib.project.upload_project
"""
env.password='123456'

@hosts('root@test')
def test_deploy():
    # campaign_deploy(web_code,svn_path,conf,web_path)
    campaign_deploy('admin','web_code/专题页面/admin','uat','/www')

@hosts('root@product')
def prepare_deploy():
    # web_deploy(web_code,svn_path,conf,web_path):
    web_deploy('blinq','web_code/blinq_mobile','product','/php')
    # campaign_deploy('ThinkPHP','web_code/ThinkPHP','product','/php')

@hosts('root@product')
def online_deploy():
    # campaign_deploy('admin','web_code/专题页面/admin','product','/online')
    web_deploy('blinq','web_code/blinq_mobile','product','/online')

@hosts('root@wechat')
def wechat_deploy():
    # campaign_deploy(web_code,svn_path,conf,web_path)
    campaign_deploy('gz_guaguaka','web_code/专题页面/gz_guaguaka','product','/php/campaign')

def campaign_deploy(web_code,svn_path,conf,web_path):
    # get web_code
    with lcd("/tmp"):
        if local_exists(web_code).succeeded:
            with lcd('/tmp/%s' % web_code):
                update()
        else:
            local('git svn clone svn://10.1.0.241/%s %s' % (svn_path,web_code))
    
    if web_code != 'ThinkPHP':
        with lcd('/tmp/%s' % web_code):
            chconfig(conf)

    with lcd("/tmp"):
        local("tar -czf %s.tar.gz %s/ --exclude *.html.bak --exclude *.sql --exclude .git --exclude Runtime" % (web_code,web_code))
        put("%s.tar.gz" % web_code,"/tmp/%s.tar.gz" % web_code)
        # local("rm -f %s.tar.gz" % web_code)
    with cd('/tmp'):
        run("tar zxf %s.tar.gz -C %s" % (web_code,web_path))
        run("rm -f %s.tar.gz" % web_code)

    if web_code != 'ThinkPHP':
            clearRuntime(web_path,web_code)

def web_deploy(web_code,svn_path,conf,web_path):
    # get web_code
    with lcd("/tmp/"):
        if local_exists(web_code).succeeded:
            with lcd('/tmp/%s' % web_code):
                update()
        else:
            local('git svn clone svn://10.1.0.241/%s %s' % (svn_path,web_code))

    with lcd('/tmp/%s' % web_code):
        chconfig(conf)
        local("tar czf %s.tar.gz * --exclude *.html.bak --exclude *.sql --exclude .git --exclude Runtime" % web_code)
        put("%s.tar.gz" % web_code,"/tmp/%s.tar.gz" % web_code)
        local("rm -f %s.tar.gz" % web_code)
    with cd('/tmp'):
        run("tar zxf %s.tar.gz -C %s" % (web_code,web_path))
        run("rm -f %s.tar.gz" % web_code)

    with cd("%s" % web_path):
        if not exists("%s/Runtime" % web_path):
            run('mkdir Runtime')
            run('chmod o+w ./Runtime -R')
        else:
            sudo('rm -rf ./Runtime/Cache/* ./Runtime/*.php')

def update():
    # remove changed files, but keep unversioned files.
    local("git checkout master -f") 
    # svn update
    local("git svn rebase") 

def backup(web_code):
    run('rm -rf %s-*.tar.gz' % web_code)
    DATE_FORMAT='$(date +%m%d%H%M)'
    run("tar -czf %s-%s.tar.gz %s" % (web_code,DATE_FORMAT,web_code))

def chconfig(conf='uat'):
    if conf != 'uat':
        local("sed -i \"s/^.*APP_DEBUG.*/define('APP_DEBUG',false);/\" index.php")
    local("sed -i \"s/^.*APP_STATUS.*/define('APP_STATUS','%s');/\" index.php" % conf)
    # .html css js clear cache
    local("$HOME/fabric/html.sh")

def clearRuntime(web_path,web_code):
    with cd("%s/%s" % (web_path,web_code)):
        if not exists("%s/%s/Runtime" % (web_path,web_code)):
            run('mkdir Runtime')
            run('chmod o+w ./Runtime -R')
        else:
            sudo('rm -rf ./Runtime/Cache/* ./Runtime/*.php')

def local_exists(path):
    with settings(hide('everything'),warn_only=True):
        return local('test -e %s' % path)
