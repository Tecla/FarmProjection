# This Python file uses the following encoding: utf-8

from .Dairy import *
from .Livestock import *
from .Creamery import *
from .Store import *
from .Utilities import *


def grossIncomeByAnimalPerYear(s, animal):
    income = 0
    income += livestockGrossIncomePerYear(s, animal)
    income += milkGrossIncomeByAnimalPerYear(s, animal)
    income += creameryGrossIncomeByAnimalPerYear(s, animal)
    return income

def netIncomeByAnimalPerYear(s, animal):
    income = 0
    income += livestockNetIncomePerYear(s, animal)
    income += dairyNetIncome(s, animal)
    income += creameryNetIncomeByAnimalPerYear(s, animal)
    return income

def netSelfPayPerYearEstimate(s, netIncome):
    taxType = s.get('taxes/Tax situation')
    ssTaxRate = s.get('taxes/SS pct') * 0.01
    mcTaxRate = s.get('taxes/Medicare pct') * 0.01
    ssLimit = s.get('taxes/SS limit')
    seTaxBase = s.get('taxes/OASDI tax base pct') * 0.01
    stateTaxRate = s.get('taxes/State tax rate pct') * 0.01

    taxTable = []
    taxDict = s.get('taxes/Tax table/{}'.format(taxType))
    for taxRateStr, threshold in taxDict.items():
        taxTable += [ (int(taxRateStr), threshold) ]
    def applyTaxTable(income, table):
        taxes = 0.0
        incomeRemaining = income
        lastThreshold = 0
        for entry in table:
            taxPct, threshold = entry
            taxRate = taxPct * 0.01
            if income >= lastThreshold:
                incomeAtThisLevel = min(income, threshold) - lastThreshold
                taxes += (min(income, threshold) - lastThreshold) * taxRate
                lastThreshold = threshold
            else:
                break
        return taxes

    taxes = 0
    taxes += applyTaxTable(netIncome, taxTable)
    taxes += netIncome * stateTaxRate
    taxBase = seTaxBase * netIncome
    ficaIncome = min(taxBase, ssLimit)
    taxes += taxBase * mcTaxRate * 2.0    # Both employee and employer portion
    taxes += ficaIncome * ssTaxRate * 2.0 # Both employee and employer portion, stopped out a SS limit
    return max(0.0, netIncome - taxes)


def ProjectProfit(scenario, scenarioName):
    s = scenario
    print("Summary")
    print("=======")
    print('')
    print('Scenario: {}'.format(scenarioName))
    print('')
    print("Total acres needed: {}".format(round(neededAcres(s, True), 2)))
    print("Total acres desired: {}".format(round(neededAcres(s, False), 2)))
    print("Hit acreage limit: {}".format('Yes' if s.hasAcreLimit() and s.getDesiredAcres() >= neededAcres(s, True) else 'No'))
    print('')

    butterLbs = 0
    cheeseLbs = 0
    creamGallons = 0
    iceCreamGallons = 0
    milkGallons = 0
    yogurtGallons = 0
    animals = livestockList(s)
    for animal in animals:
        butterLbs += butterLbsByAnimalPerWeek(s, animal)
        cheeseLbs += cheeseLbsByAnimalPerWeek(s, animal)
        creamGallons += creamGallonsByAnimalPerWeek(s, animal)
        iceCreamGallons += iceCreamGallonsByAnimalPerWeek(s, animal)
        milkGallons += milkGallonsSoldPerWeek(s, animal)
        yogurtGallons += yogurtGallonsByAnimalPerWeek(s, animal)
    print('Butter lbs to sell per week: {}'.format(round(butterLbs, 2)))
    print('Cheese lbs to sell per week: {}'.format(round(cheeseLbs, 2)))
    print('Cream gallons to sell per week: {}'.format(round(creamGallons, 2)))
    print('Ice cream gallons to sell per week: {}'.format(round(iceCreamGallons, 2)))
    print('Milk gallons to sell per week: {}'.format(round(milkGallons, 2)))
    print('Yogurt gallons to sell per week: {}'.format(round(yogurtGallons, 2)))
    print('')

    grossIncome = 0
    netIncome = 0
    for animal in animals:
        incomeByAnimal = grossIncomeByAnimalPerYear(s, animal)
        netIncomeByAnimal = netIncomeByAnimalPerYear(s, animal)
        print("Gross income and net income for {}s: {}, {}".format(animal, dollars(incomeByAnimal), dollars(netIncomeByAnimal)))
        grossIncome += incomeByAnimal
        netIncome += netIncomeByAnimal
    grossIncome += storeGrossIncomePerYear(s)
    print('Total income: {}'.format(dollars(grossIncome)))
    print('')

    totalNetIncome = netIncome
    totalNetIncome += storeNetIncomePerYear(s)
    print('Total profit: {}'.format(dollars(totalNetIncome)))

    netPayEstimate = netSelfPayPerYearEstimate(s, totalNetIncome)
    print('Self net estimate: {} (per month: {})'.format(dollars(netPayEstimate), dollars(netPayEstimate / 12.0)))
