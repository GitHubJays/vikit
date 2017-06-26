#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Logger For Vikit
  Created: 06/11/17
"""

import os
import logging
import sys
from logging import handlers

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_LOG_DIR = os.path.join(_CURRENT_DIR, '../../datas/logs/')

NETIO_LOGFILE_NAME = 'netio.log.vikitdata'

_DEFAULT_LOGGING_FMT = "[%(levelname)s] %(asctime)s [%(filename)s:%(funcName)s line:%(lineno)s]: %(message)s"
_LITE_LOGGING_FMT = "[%(levelname)s] %(asctime)s: %(message)s"
_DEFAULT_TIME_FMT = '[%d %b %Y %H:%M:%S]'

########################################################################
class VikitLogger(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, name, logfile, fmt=None, log_trigger=True,
                 max_bytes=10*1024*1024, backup_count=5,
                 debug=True, no_file=True):
        """Constructor"""
        #
        # main trigger
        #
        self.name = name
        self.log_trigger = log_trigger
        self.no_file = no_file
        self.fmt = fmt if fmt else _DEFAULT_LOGGING_FMT
        self.logfile = logfile
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self._debug = debug
        
        self.__init_logger()
        
        assert hasattr(self, 'logger')
    
    #----------------------------------------------------------------------
    def __init_logger(self):
        """"""
        
        ls = [logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR]
        
        self.logger = logging.getLogger(self.name)
        
        #
        # set handler and fmt
        #
        def set_levels(levelname):
            if not self.no_file:
                self._file_hdlr.setLevel(levelname)
            
        if not self.no_file:
            self._file_hdlr = handlers.RotatingFileHandler(self.logfile, maxBytes=self.max_bytes,
                                                                 backupCount=self.backup_count)
            
            self._file_hdlr.setFormatter(logging.Formatter(self.fmt,
                                                _DEFAULT_TIME_FMT))
            self.logger.addHandler(self._file_hdlr)  
            
        if self._debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
            
        _streamhdler = logging.StreamHandler(sys.stdout)
        _streamhdler.setFormatter(logging.Formatter(_LITE_LOGGING_FMT))
        self.logger.addHandler(_streamhdler)        

        map(set_levels, ls)
        
        if self.log_trigger:
            pass
        else:
            map(logging.disable, ls)
    
    @property
    def output(self):
        """"""
        return self.logger