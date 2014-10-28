#!/usr/bin/env python
#coding=utf-8
from fabric.api import *
from contextlib import *
from fabric.contrib.files import exists
from fabric.colors import *

"""
File: fabfile.py
Author: Xiejie <xiejie2104@gmail.com>
Description: 
    10.1.0.207  test           /www
    10.0.0.183  wechat         /php/campaign
    10.0.0.186  prepare_deploy /php
    10.0.0.186  deploy         /online
TODO: 
    rsync_project
    fabric.contrib.project.upload_project
    git commit & update
    add ssh-keygen
    tar --exclude

"""

env.hosts=['localhost']
env.password='123456'

def test():
    local('echo hello')

def debug(web_code='SilverAge'):
    with lcd('/tmp'):
        if local_exists(web_code).succeeded:
            print 'exists'
        else:
            print 'not exists'

def sample_deploy(web_code,svn_path,conf,web_path):
    # get web_code
    with lcd("/tmp/"):
        if local_exists(web_code).succeeded:
            with lcd('/tmp/%s' % web_code):
                update()
        else:
            local('git svn clone svn://10.1.0.241/%s %s' % (svn_path,web_code))

    with lcd('/tmp/%s' % web_code):
        chconfig(conf)
    with lcd("/tmp"):
        local("tar -czf %s.tar.gz %s/" % (web_code,web_code))
        put("%s.tar.gz" % web_code,"/tmp/%s.tar.gz" % web_code)
        local("rm -f %s.tar.gz" % web_code)
    with cd(web_path):
        if exists(web_code):
            backup(web_code)
    with cd('/tmp'):
        run("tar -zxf %s.tar.gz -C %s" % (web_code,web_path))
        run("rm -f %s.tar.gz" % web_code)
    with cd("%s/%s" % (web_path,web_code)):
        clearRuntime()

@hosts('root@10.0.0.186')
def deploy():
    # sample_deploy(web_code,svn_path,conf,web_path)
    sample_deploy('admin','web_code/专题页面/admin','product','/online')


@hosts('root@10.0.0.183')
def wechat_deploy():
    # sample_deploy(web_code,svn_path,conf,web_path)
    sample_deploy('SilverAge','web_code/专题页面/SilverAge','product','/php/campaign')

@hosts('root@10.0.0.186')
def prepare_deploy():
    # sample_deploy(web_code,svn_path,conf,web_path)
    pass

@hosts('root@10.1.0.207')
def test_deploy():
    # sample_deploy(web_code,svn_path,conf,web_path)
    sample_deploy('shining','web_code/专题页面/shining','uat','/www')
    # with cd('/www/SilverAge/Public/js'):
    #     run("sed -i \"s|\(.*\)/cp/\(.*\)|\\1/cptest/\\2|\" share.js")


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
	local("sed -i \"s/^.*APP_DEBUG.*/define('APP_DEBUG',false);/\" index.php")
	local("sed -i \"s/^.*APP_STATUS.*/define('APP_STATUS','%s');/\" index.php" % conf)

def clearRuntime():
	run('rm -rf ./Runtime/*')
	run('chmod o+w ./Runtime -R')

def local_exists(path):
    with settings(hide('everything'),warn_only=True):
        return local('test -e %s' % path)

def init():
    pass

def clone(svn_path):
    local('git svn clone svn://10.1.0.241/%s' % svn_path)

def commit():
	local("git add -p && git commit")

def push():
	local("git push")

def redis_clear():
    # remove picture cache
    local("redis-cli -h 10.0.0.199 del jc_list top_data index_pic jc_data")