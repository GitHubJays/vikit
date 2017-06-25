#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: LogTest
  Created: 06/26/17
"""

from vikit.core import vikitlogger

print(vikitlogger.fmt)
print(vikitlogger.debug)
vikitlogger.debug = True
print(vikitlogger.debug)
vikitlogger.no_file = False
print(vikitlogger)
#----------------------------------------------------------------------
def test():
    """"""
    clog = vikitlogger.logger.VikitLogger('test', './test_log.test', no_file=False)
    clog.output.info('sfasdfasdfa')
        
    
test()

