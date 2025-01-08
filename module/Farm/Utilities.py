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

def amortizedLoanPayment(principal, ratePerYear, totalPeriods, periodsPerYear=12):
    ratePerPeriod = ratePerYear / float(periodsPerYear)
    if totalPeriods <= 0:
        return principal
    elif ratePerYear <= 0.0:
        return principal / float(totalPeriods)
    else:
        poweredRate = pow(1.0 + ratePerPeriod, totalPeriods)
        return principal * ratePerPeriod * poweredRate / (poweredRate - 1.0)

def smoothstep(a1, a2, value):
    if a2 <= a1:
        return 0.0
    t = (value - a1) / (a2 - a1)
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    return t * t * (3.0 - 2.0 * t)
