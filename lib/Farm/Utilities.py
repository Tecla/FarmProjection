# This Python file uses the following encoding: utf-8


def dollars(value):
    return "${:.2f}".format(float(value))

def rounded(value, places):
    formatStr = "{}:.{}f{}".format('{', places, '}')
    return formatStr.format(float(value))
