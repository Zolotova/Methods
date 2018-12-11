import sys
import numpy as np
from math import *


# functions1 = 'δ*cos(β*x/(α*α-x*x))+ε*sin(γ*x)'
def replace(functionSource, gamma):
    return functionSource.replace('γ', str(gamma) or '1')


def delItem(dictionary, key):
    r = dict(dictionary)
    del r[key]
    return r


def calculateFunction(x, y, func):
    print(x, y)
    f = func.replace('x', str(x))
    f = f.replace('y', str(y))

    try:
        result = eval(f)
    except ZeroDivisionError:
        result = inf
    return result


def findPoint(pointX, pointY, func):
    result = calculateFunction(pointX, pointY, func)
    k = 0
    if result == inf:
        result = (calculateFunction(pointX + sys.float_info.epsilon, pointY + sys.float_info.epsilon, func) + calculateFunction(
            pointX - sys.float_info.epsilon, pointY - sys.float_info.epsilon, func)) / 2
    return result