#!/usr/bin/env python
# coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 06/24/17
"""

from adaptors import email_adaptor
from adaptors import adatporbase

#
# keyword defination
#
EMAIL_ADAPTOR = 'email_adaptor'
WECHAT_ADAPTOR = 'wechat_adaptor'

_dict_adaptor = {
    EMAIL_ADAPTOR: email_adaptor.EmailAdaptor,
    WECHAT_ADAPTOR: None,
}


# ----------------------------------------------------------------------
def get_adaptor_by_name(name):
    """"""
    return _dict_adaptor.get(name)


########################################################################
class NotifyConfig(object):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""

        self._list_adaptor_and_its_config = []

    # ----------------------------------------------------------------------
    def add_adaptor(self, adaptor_name, config):
        """"""
        _adaptor = get_adaptor_by_name(adaptor_name)
        self._list_adaptor_and_its_config.append((_adaptor, config))

    @property
    def adaptors(self):
        """"""
        return [adaptor(params) for adaptor, params in \
                self._list_adaptor_and_its_config]


########################################################################
class Notifier(object):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, config):
        """Constructor"""
        config = config if config else NotifyConfig()
        assert isinstance(config, NotifyConfig)

        self.config = config

    # ----------------------------------------------------------------------
    def notify(self, result):
        """"""
        #
        # process result
        #

        _result = str(result._dict_obj)

        for i in self.config.adaptors:
            assert isinstance(i, adatporbase.AdaptorBase)
            i.send(_result)
