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


def storeThirdPartyCostPerYear(s):
    costs = 0.0
    thirdPartyItems = s.get('store/third party')
    for name, item in thirdPartyItems.items():
        if name == "__comments__":
            continue
        if 'cost' not in item or 'price' not in item or 'items sold per month' not in item:
            print('Invalid third party item found in store: {} {}'.format(name, item))
            continue
        costs += item['cost'] * item['items sold per month'] * 12
    return costs


def storeThirdPartyIncomePerYear(s):
    income = 0.0
    thirdPartyItems = s.get('store/third party')
    for name, item in thirdPartyItems.items():
        if name == "__comments__":
            continue
        if 'cost' not in item or 'price' not in item or 'items sold per month' not in item:
            print('Invalid third party item found in store: {}'.format(name))
            continue
        income += item['price'] * item['items sold per month'] * 12
    return income


def storeCommonCostPerYear(s):
    amortizationYears = s.get('farm/amortization years')
    fixedAmortizationActive = True if s.get('farm/years running') <= amortizationYears else False

    cost = 0.0
    if fixedAmortizationActive:
        totalFixedCosts = 0.0
        fixedCosts = s.get('store/fixed/* cost')
        if fixedCosts:
            for c in fixedCosts:
                totalFixedCosts += c / float(amortizationYears) if amortizationYears > 0 else 0.0
        cost += amortizedLoanPayment(totalFixedCosts, s.get('farm/fixed cost loan rate') * 0.01, amortizationYears * 12) * 12
        cost += amortizedLoanPayment(storeFacilityCost(s), s.get('farm/facility loan rate') * 0.01, amortizationYears * 12) * 12
    yearlyCosts = s.get('store/yearly/* cost')
    if yearlyCosts:
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


def storeEmployeeHoursPerDay(s):
    return storeEmployeeHoursPerWeek(s) / 7.0


def storeEmployeeExpectedPayRatePerHour(s):
    minPayRate = s.get('store/employee/min pay per hour')
    maxPayRate = s.get('store/employee/max pay per hour')
    # For now, we just return the max pay rate
    return maxPayRate


# Returns a tuple of (pay, overhead)
def storeEmployeeExpectedPayPerYear(s):
    ssTaxRate = s.get('taxes/SS pct') * 0.01
    mcTaxRate = s.get('taxes/Medicare pct') * 0.01
    ssLimit = s.get('taxes/SS limit')

    payRatePerHour = storeEmployeeExpectedPayRatePerHour(s)
    hoursPerYear = storeEmployeeHoursPerYear(s)
    incomePerYear = payRatePerHour * hoursPerYear
    overheadPerYear = incomeOverhead(s, incomePerYear)
    return (incomePerYear, overheadPerYear)


def storeGrossIncomePerYear(s):
    # All the rest of the income is currently attributed to other parts of the farm
    return storeThirdPartyIncomePerYear(s)


def storeNetIncomePerYear(s):
    storeEmployeeYearlyPay, storeEmployeeYearlyOverhead = storeEmployeeExpectedPayPerYear(s)
    return storeGrossIncomePerYear(s) - storeThirdPartyCostPerYear(s) - storeCommonCostPerYear(s) - storeEmployeeYearlyPay - storeEmployeeYearlyOverhead
