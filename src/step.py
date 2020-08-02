#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import abc
import sys
import time
import shutil
import subprocess

import path
import log

from conf import config
from log import func_log
from log import func_timer

logger = log.get_logger('aaaa')

#==============================================================================
# JobComponent,JobItem,Job
# JobComponent: Component接口
# JobItem: Leaf接口
# Job: Composite节点
#==============================================================================

class JobComponent(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add(self, component):
        pass

    @abc.abstractmethod
    def run(self):
        pass

class JobItem(JobComponent):
    def add(self, component):
        raise NotImplementedError('JobItem.add not implemented!')

    @abc.abstractmethod
    def run(self):
        pass

class Job(JobComponent):
    def __init__(self, job_name='Job'):
        self._job_items = []
        self._name = job_name

    def add(self, component):
        self._job_items.append(component)

    @func_timer(logger)
    def run(self):
        logger.info('%s run enter ...', self._name)

        start_time = time.perf_counter()
        try:
            for item in self._job_items:
                item.run()
        except BaseException:
            logger.error('exception', exc_info=True)
            sys.exit(1)
        end_time = time.perf_counter()
        logger.info('%s used %.3f seconds', self._name, end_time - start_time)

        logger.info('%s run exit ...', self._name)

class PathPrinter(JobItem):
    @func_log(logger)
    def run(self):
        logger.info('PROJECT_ROOT_PATH = %s', path.get_project_root_path())
        logger.info('LOG_PATH          = %s', path.get_build_path())
        logger.info('BUILD_PATH        = %s', path.get_build_path())
        logger.info('RESOURCE_PATH     = %s', path.get_resource_path())

#==============================================================================
# CommandExecuter: Shell命令执行器
#==============================================================================

class CommandExecuter(JobItem):
    def run(self):
        for cmd in self.cmd_list():
            logger.info('%s ', cmd)
            ret = subprocess.call(cmd, shell=True)
            if ret != 0:
                raise RuntimeError('CommandExecuter error. return code %s' % ret)

    @abc.abstractmethod
    def cmd_list(self):
        pass


class DirectoryMaker(JobItem):
    def run(self):
        for item in self.get_dirs():
            if os.path.exists(item):
                logger.info('%s already exist, no need to create.', item)
            else:
                logger.info('%s does not exist, will be created.', item)
                os.makedirs(item)

    @abc.abstractmethod
    def get_dirs(self):
        pass


class GoDirectoryMaker(DirectoryMaker):
    def get_dirs(self):
        dir_list = []
        dir_list.append(path.get_build_path())
        # dir_list.append(config.get_value_by_1key('software_install_path'))
        return dir_list

class GoPathDirectoryMaker(DirectoryMaker):
    def get_dirs(self):
        go_path = os.path.join(config.get_value_by_1key('software_install_path'), 'gopath')

        dir_list = []
        dir_list.append(os.path.join(go_path, 'bin'))
        dir_list.append(os.path.join(go_path, 'pkg'))
        dir_list.append(os.path.join(go_path, 'src'))
        return dir_list

class JavaDirectoryMaker(DirectoryMaker):
    def get_dirs(self):
        dir_list = []
        dir_list.append(path.get_build_path())
        return dir_list

#==============================================================================
# DirectoryCleaner: 删除制定目录
#==============================================================================

class DirectoryCleaner(JobItem):
    def run(self):
        for item in self.get_dirs():
            if not os.path.exists(item):
                logger.info('%s does not exist, no need to clean.', item)
            else:
                logger.info('remove %s', item)
                shutil.rmtree(item)

    @abc.abstractmethod
    def get_dirs(self):
        pass

class AllDirectoryCleaner(DirectoryCleaner):
    def get_dirs(self):
        dir_list = []
        dir_list.append(path.get_build_path())
        return dir_list

class GoDirectoryCleaner(DirectoryCleaner):
    def get_dirs(self):
        dir_list = []
        dir_list.append(os.path.join(path.get_resource_path(), 'install_go'))
        return dir_list

class JavaDirectoryCleaner(DirectoryCleaner):
    def get_dirs(self):
        dir_list = []
        dir_list.append(os.path.join(path.get_resource_path(), 'install_java'))
        return dir_list

#==============================================================================
# ResourceDownloader: 下载依赖的资源
#==============================================================================

class ResourceDownloader(JobItem):
    def run(self):
        for url in self.get_urls():
            ret = subprocess.call('wget -P %s \'%s\' ' % (self.get_dest_path(), url), shell=True)
            if ret != 0:
                raise RuntimeError('ResourceDownloader error. return code %s' % ret)

    @abc.abstractmethod
    def get_urls(self):
        pass

    @abc.abstractmethod
    def get_dest_path(self):
        pass

class GoPackageDownloader(ResourceDownloader):
    def get_urls(self):
        url_list = []
        url_list.append(os.path.join(
            config.get_value_by_2key('install_go', 'url_base'),
            config.get_value_by_2key('install_go', 'package_name')))
        return url_list

    def get_dest_path(self):
        return os.path.join(path.get_resource_path(), 'install_go')

class JavaPackageDownloader(ResourceDownloader):
    def get_urls(self):
        url_list = []
        url_list.append(os.path.join(
            config.get_value_by_2key('install_java', 'url_base'),
            config.get_value_by_2key('install_java', 'package_name')))
        return url_list

    def get_dest_path(self):
        return os.path.join(path.get_resource_path(), 'install_java')

#==============================================================================
# FileDecompressor:
#==============================================================================

class FileDecompressor(CommandExecuter):
    def cmd_list(self):
        cmd_list = []
        cmd_list.append('tar -xzf %s -C %s' % (self.compressed_file_path(), self.dest_path()))
        return cmd_list

    @abc.abstractmethod
    def compressed_file_path(self):
        pass

    @abc.abstractmethod
    def dest_path(self):
        pass

class GoPackageDecompressor(FileDecompressor):
    def compressed_file_path(self):
        return os.path.join(
            path.get_resource_path(),
            'install_go',
            config.get_value_by_2key('install_go', 'package_name'))

    @abc.abstractmethod
    def dest_path(self):
        return config.get_value_by_2key('install_go', 'install_path')
