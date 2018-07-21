# -*- coding: utf-8 -*-
'''
通过羊城通ID匹配，在早晚高峰都一次以上出行的为换乘

'''
from collections import deque #提高list删除插入速度
import operator
import time
import os