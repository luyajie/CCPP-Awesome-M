#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-25 00:11:18
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import subprocess
opt = int(input("Please Choose your operation:"))
"""
1:从Github文件夹同步到编辑文件夹
2:从编辑文件夹同步到Github文件夹
"""
print("1 or 2")
if opt==1:
    op = subprocess.getoutput("rsync -vr /Users/LiuBing/Documents/CCPP-Awesome-M/ "
                              "/Users/LiuBing/PycharmProjects/CCPP-Awesome-M")
elif opt==2:
    op = subprocess.getoutput("rsync -vr "
                              "/Users/LiuBing/PycharmProjects/CCPP-Awesome-M/ "
                              "/Users/LiuBing/Documents/CCPP-Awesome-M")
else:
    print("reinput!")
print(op)
print("ur choose is %d"%(opt))
