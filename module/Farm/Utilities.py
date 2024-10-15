# This Python file uses the following encoding: utf-8


def dollars(value):
    return "${:.2f}".format(float(value))

def rounded(value, places):
    formatStr = "{}:.{}f{}".format('{', places, '}')
    return formatStr.format(float(value))

def incomeOverhead(s, incomePerYear):
    ssTaxRate = s.get('taxes/SS pct') * 0.01
    mcTaxRate = s.get('taxes/Medicare pct') * 0.01
    ssLimit = s.get('taxes/SS limit')
    ficaIncome = min(incomePerYear, ssLimit)
    taxes = incomePerYear * mcTaxRate # Employer portion, unlimited
    taxes += ficaIncome * ssTaxRate   # Employer portion, stopped out at SS limit
    return taxes
