#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import logging
import functools
from datetime import datetime

import path


def func_log(in_logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            in_logger.info('{}.{} enter >...'.format(args[0].__class__.__name__, func.__name__))
            result = func(*args, **kwargs)
            in_logger.info('{}.{} exit ...<'.format(args[0].__class__.__name__, func.__name__))
            return result
        return wrapper
    return decorator

def func_timer(in_logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            in_logger.info('%s.%s used %.3f seconds ......', args[0].__class__.__name__, \
                func.__name__, end_time - start_time)
            return result
        return wrapper
    return decorator


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)

    if not logger.hasHandlers():
        create_log_dir()

        formatter = logging.Formatter(
            '[%(levelname)1.1s%(asctime)s][%(process)d|%(thread)d]' \
            '[%(filename)s:%(lineno)d] %(message)s')

        file_handler = logging.FileHandler(get_log_file_name(logger_name))
        # file_handler = ConcurentRotatingFileHandler(
        #     get_log_file_name(logger_name), 'a', 50*1024*1024, 10)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

def create_log_dir():
    log_dir = path.get_log_path()
    if os.path.exists(log_dir):
        print('%s already exist, no need to create.' % log_dir)
    else:
        print('%s does not exist, will be created' % log_dir)
        os.makedirs(log_dir)

def get_log_file_name(logger_name):
    file_name = '{}.{}'.format(
        os.path.join(path.get_log_path(), logger_name),
        datetime.now().strftime('%Y%m%dT%H%M%S'))
    return file_name
