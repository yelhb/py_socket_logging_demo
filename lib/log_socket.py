#! /home/bae/dataplatform/python-2.7.9/bin python
# -*- coding:utf-8 -*-
"""
Authors: yel_hb
Date:    2016/10/18
"""

import os
import logging
import logging.handlers

def init_log(level=logging.INFO, datefmt="%m-%d %H:%M:%S",
             format="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s"):
    """
    init_log - initialize log module

    Args:
        level         - msg above the level will be displayed
                        DEBUG < INFO < WARNING < ERROR < CRITICAL
                        the default value is logging.INFO
        format        - format of the log
                        default format:
                        %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s
                        INFO: 12-09 18:02:42: log.py:40 * 139814749787872 HELLO WORLD

    Raises:
        OSError: fail to create log directories
        IOError: fail to open log file
    """
    
    formatter = logging.Formatter(format, datefmt)
    logger = logging.getLogger()
    logger.setLevel(level)
    
    HOST = "localhost"
    PORT = logging.handlers.DEFAULT_TCP_LOGGING_PORT

    socket_handler = logging.handlers.SocketHandler(HOST, PORT)

    socket_handler.setLevel(level)
    socket_handler.setFormatter(formatter)
    logger.addHandler(socket_handler)

