#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-25 00:11:18
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import subprocess
op = subprocess.getoutput("rsync -vr /Users/LiuBing/Documents/CCPP-Awesome-M/ \
/Users/LiuBing/PycharmProjects/CCPP-Awesome-M")
print(op)
