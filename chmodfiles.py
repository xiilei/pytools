#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'xilei'

import os
from os.path import join
import stat


def chmod(targetdir):
    """
     chmod 644 for files
    """
    for root, dirs, files in os.walk(targetdir):
        for file in files:
            os.chmod(join(root, file), stat.S_IWRITE+stat.S_IREAD+stat.S_IROTH+stat.S_IRGRP)


if __name__ == '__main__':
    ##print(os.mkdir('/home/xilei/work/test/dirs'), 755)
    chmod('/home/xilei/work/test')