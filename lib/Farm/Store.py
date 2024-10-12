# This Python file uses the following encoding: utf-8

from .Livestock import *
from .Dairy import *
from .Utilities import *


def storeFacilitySqft(s):
    storeArea = s.get('store/store area sqft')
    utilityArea = s.get('structures/store/utility sqft')
    officeArea = s.get('structures/store/office sqft')
    bathroomArea = s.get('structures/store/bathroom sqft')
    overheadArea = s.get('structures/store/overhead sqft')
    return storeArea + utilityArea + officeArea + bathroomArea + overheadArea


def storeFacilityCost(s):
    costPerSqft = s.get('structures/store/cost per sqft')
    return storeFacilitySqft(s) * costPerSqft


def storeCommonCostPerYear(s):
    amortizationYears = s.get('farm/amortization years')
    fixedAmortizationActive = True if s.get('farm/years running') <= amortizationYears else False

    cost = 0
    if fixedAmortizationActive:
        fixedCosts = s.get('store/fixed/* cost')
        for c in fixedCosts:
            cost += c / float(amortizationYears)
        cost += storeFacilityCost(s) / float(amortizationYears)
    yearlyCosts = s.get('store/yearly/* cost')
    for c in yearlyCosts:
        cost += c
    return cost


def storeHoursPerYear(s):
    hoursPerWeek = s.get('store/open hours per week')
    return hoursPerWeek * (365.0 / 7.0)


def storeEmployeeHoursPerWeek(s):
    hoursPerWeek = s.get('store/open hours per week')
    selfHoursPerWeek = s.get('store/self hours per week')
    return max(0, hoursPerWeek - selfHoursPerWeek)


def storeEmployeeHoursPerYear(s):
    return storeEmployeeHoursPerWeek(s) * (365.0 / 7.0)


def storeEmployeeExpectedPayRatePerHour(s):
    minPayRate = s.get('store/employee/min pay per hour')
    maxPayRate = s.get('store/employee/max pay per hour')
    # For now, we just return the max pay rate
    return maxPayRate


# Returns a tuple of (pay, overhead)
def storeEmployeeExpectedPayPerYear(s):
    ssTaxRate = s.get('taxes/SS')
    mcTaxRate = s.get('taxes/Medicare')
    ssLimit = s.get('taxes/SS limit')

    payRatePerHour = storeEmployeeExpectedPayRatePerHour(s)
    hoursPerYear = storeEmployeeHoursPerYear(s)
    incomePerYear = payRatePerHour * hoursPerYear
    overheadPerYear = incomeOverhead(s, incomePerYear)
    return (incomePerYear, overheadPerYear)


def storeIncomePerYear(s):
    # All income is currently attributed to other parts of the farm
    return -storeCommonCostPerYear(s)


def storeNetIncomePerYear(s):
    storeEmployeeYearlyPay, storeEmployeeYearlyOverhead = storeEmployeeExpectedPayPerYear(s)
    return storeIncomePerYear(s) - storeEmployeeYearlyPay - storeEmployeeYearlyOverhead
