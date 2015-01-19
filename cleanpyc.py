#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'xilei'

import os
from os.path import join
import stat


def chmod(targetdir):
    """
     remove *.pyc files
    """
    for root, dirs, files in os.walk(targetdir):
        for file in files:
            prefix,ext = os.path.splitext(file)
            if ext == '.pyc':
                filename = join(root,file)
                os.remove(filename)
                print("remove:%s" % filename)


if __name__ == '__main__':
    chmod('./')
