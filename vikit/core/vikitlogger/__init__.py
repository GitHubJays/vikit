#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4>
  Purpose: Logging entry for logging
  Created: 06/26/17
"""

import os

from . import logger

LOGDIR = logger._LOG_DIR

#
# default logfile name
#
PLATFORM_LOGNAME = 'platform'
PLATFORM_LOGFILE_NAME = 'platform.log'

SERVICENODE_LOGNAME = 'servicenode'
SERVICENODE_LOGFILE_NAME = 'servicenode.log'

SERVICE_LOGNAME = 'service'
SERVICE_LOGFILE_NAME_fmt_id = 'service-{}.log'

CLIENT_LOGNAME = 'client'
CLIENT_LOGFILE_NAME = 'client.log'

NETIO_LOGNAME = 'netio'
NETIO_LOGFILE_NAME = 'notio.log'



fmt = None
log_trigger = True
debug = True
no_file = True
max_bytes = 10 * 1024 * 1024
backup_count = 5

#----------------------------------------------------------------------
def _build_logger(name, filename):
    """"""
    global fmt, log_trigger, no_file, debug, max_bytes, backup_count
    
    filename = os.path.join(LOGDIR, filename)
    log = logger.VikitLogger(name, filename, fmt, log_trigger,
                             max_bytes, backup_count, debug, no_file)
    
    return log
    

#
# platform logger
#
PLATFORM_LOGGER = None
#----------------------------------------------------------------------
def get_platform_logger():
    """"""
    global PLATFORM_LOGGER, PLATFORM_LOGFILE_NAME, PLATFORM_LOGNAME
    if PLATFORM_LOGGER:
        pass
    else:
        PLATFORM_LOGGER = _build_logger(PLATFORM_LOGNAME, PLATFORM_LOGFILE_NAME)
    
    return PLATFORM_LOGGER.output

#
# servicenode logger
#
SERVICENODE_LOGGER = None
#----------------------------------------------------------------------
def get_servicenode_logger():
    """"""
    global SERVICENODE_LOGFILE_NAME, SERVICENODE_LOGGER, SERVICENODE_LOGNAME
    if SERVICENODE_LOGGER:
        pass
    else:
        SERVICENODE_LOGGER = _build_logger(SERVICENODE_LOGNAME, SERVICENODE_LOGFILE_NAME)
        
    return SERVICENODE_LOGGER.output

#
# client logger
#
CLIENT_LOGGER = None
#----------------------------------------------------------------------
def get_client_logger():
    """"""
    global CLIENT_LOGFILE_NAME, CLIENT_LOGGER, CLIENT_LOGNAME
    if CLIENT_LOGGER:
        pass
    else:
        CLIENT_LOGGER = _build_logger(CLIENT_LOGNAME, CLIENT_LOGFILE_NAME)
    
    return CLIENT_LOGGER.output