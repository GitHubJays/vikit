#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/25 20:21
# @Author  : Conan
# @Function: load exp pyc from github and import it to memory as a module


import os
import sys
import gittle
import shutil
import importlib
import stat
import gc

temp_exp_repo_path = 'https://github.com/Conanjun/pyctest.git'

_CURRENT_PATH_ = os.path.dirname(__file__)


class EXPLOADER(object):
    def __init__(self, exp_git_url):
        """"""
        self.exp_repo_git_url = exp_git_url
        self.exp_repo_temp_dir = _CURRENT_PATH_ + "/temp/"
        self.exp_repo_name = self.exp_repo_git_url[
                             self.exp_repo_git_url.rindex("/") + 1:self.exp_repo_git_url.rindex(".")]
        self.exp_mods = None

    def clone_exp_repo(self):
        if not os.path.exists(self.exp_repo_temp_dir + self.exp_repo_name):
            gittle.Gittle.clone(self.exp_repo_git_url, self.exp_repo_temp_dir + self.exp_repo_name)

    def get_pyc_files_path(self):
        """import exp from exp_repo according the pyc files （import all .pyc in the repo temporarily）"""
        pyc_files_path = []
        cur_exp_repo_path = self.exp_repo_temp_dir + self.exp_repo_name  # + "/" + "*.pyc"
        for root, dirs, files in os.walk(cur_exp_repo_path):
            for f in files:
                if (os.path.splitext(f)[1] == '.pyc'):
                    pyc_files_path.append(os.path.join(root, f))
        return pyc_files_path

    def set_exp_mods(self):
        """set only if the pyc_files_path is not None"""
        _exp_mods = {}
        for i in self.get_pyc_files_path():
            sys.path.append(os.path.split(i)[0])
            exp_mod_name = i[i.rindex("\\") + 1:i.rindex('.')]
            print exp_mod_name
            _exp_mod = importlib.import_module(exp_mod_name)
            _exp_mods[exp_mod_name]=_exp_mod

        self.exp_mods = _exp_mods

    def remove_exp_repo(self):
        gc.collect()  # 释放gittle对象对.git文件夹的占用，然后可以删除
        shutil.rmtree(self.exp_repo_temp_dir + self.exp_repo_name)


if __name__ == "__main__":
    exp_repo_loader = EXPLOADER(temp_exp_repo_path)
    exp_repo_loader.clone_exp_repo()

    # set exp mods
    exp_repo_loader.set_exp_mods()
    print("set successfully")
    print()
    print()
    #use module name to call exp mod
    exp_repo_loader.exp_mods['exp_export'].exploit()
    # try delete files and use again
    exp_repo_loader.remove_exp_repo()
    print()
    print()
    print('use after remove:')
    exp_repo_loader.exp_mods['exp'].exploit()
