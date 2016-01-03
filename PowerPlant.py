#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-26 21:59:24
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import CONST
import matplotlib.pyplot as plt


def load_dist(load):
    """[summary]
    
    [description]
    
    Arguments:
        load {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    return


x1 = CONST.SAT_SX
y1 = CONST.SAT_TY
print(len(x1))
print(len(y1))
x = [6.6282, 6.7106, 7.3515, 7.3967, 5.8402,1.9161,6.6158]
y = [550, 359, 544.7, 313.5, 32.8,159.3,552]
plt.plot(x1, y1)
plt.plot(x, y)
plt.show()
