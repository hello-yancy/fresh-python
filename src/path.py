#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def get_abs_file_path():
    return os.path.abspath(__file__)

def get_project_root_path():
    file_path = get_abs_file_path()
    src_path = os.path.dirname(file_path)
    return os.path.dirname(src_path)

def get_config_path():
    return os.path.join(get_project_root_path(), 'config')

def get_build_path():
    return os.path.join(get_project_root_path(), 'build')

def get_log_path():
    return os.path.join(get_build_path(), 'log')

def get_resource_path():
    return os.path.join(get_build_path(), 'resource')
