# encoding: utf-8

from datetime import datetime

DT_FORMAT = '%Y-%m-%d %H:%M:%S'


def nowDatetime():
    return datetime.now()


def nowTimeToString():
    return datetime.now().strftime(DT_FORMAT)


def strToDatetime(tstr):
    return datetime.strptime(tstr, DT_FORMAT)


def hourminToMin(h, m):
    """
    >>> hourminToMin(2, 30)
    150
    """
    h, m = int(h), int(m)
    return 60*h + m


def minToHourMin(m):
    """
    >>> minToHourMin(150)
    (2, 30)
    """
    rh = m // 60
    rm = m - 60*rh
    return rh, rm


def secToMin(s):
    """
    >>> secToMin(150)
    2
    """
    return s // 60


def dictToListSortedByValue(d):
    """
    >>> dictToListSortedByValue({"02_T": "CC", "01_E": "BB", "03_H": "AA"})
    ['BB', 'CC', 'AA']
    """
    return [v for k, v in sorted(d.items())]
