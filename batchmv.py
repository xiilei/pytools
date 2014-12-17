#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'xilei'

import os
import sys
import hashlib
import shutil

def md5hex(s):
    m = hashlib.md5()
    m.update(s.encode('UTF-8'))
    return m.hexdigest()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("miss args, use like batchmv.py /var/www/pdf")
        sys.exit(0)

    basePath = sys.argv[1]
    print("basePath%s \r\n" % basePath)
    for item in os.listdir(basePath):
        src = os.path.join(basePath, item)
        #只针对文件
        if not os.path.isfile(src):
            continue
        prefix, ext = os.path.splitext(item)
        # pdf
        if ext != '.pdf':
            continue
        # hash重命名
        newname = md5hex("pdf_"+prefix)+".pdf"
        dst = os.path.join(basePath, newname)
        shutil.copyfile(src=src, dst=dst)
        print("mv:%s to %s \r\n" % (item, newname))
    pass
