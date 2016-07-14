#encoding: utf-8

from datetime import datetime

DT_FORMAT = '%Y-%m-%d %H:%M:%S'

def nowDatetime():
    return datetime.now()

def nowTimeToString():
    return datetime.now().strftime(DT_FORMAT)

def strToDatetime(tstr):
    return datetime.strptime(tstr, DT_FORMAT)

def hourminToMin(h, m):
    h, m  = int(h), int(m)
    return 60*h + m

def minTohourMin(m):
    rh = m // 60
    rm = m - 60*rh
    return rh, rm

def secToMin(s):
    return s // 60
