# This Python file uses the following encoding: utf-8

from .Livestock import *
from .Dairy import *
from .Utilities import *


#
# Cheese
#

def cheeseGallonsUsedByAnimalPerYear(s, animal):
    cheeseMilkProportion = s.get('creamery/{}/cheese milk pct'.format(animal)) * 0.01
    cheeseMilkGallonsPerDay = milkGallonsPerDay(s, animal) * cheeseMilkProportion
    return cheeseMilkGallonsPerDay * 365.0


def cheeseLbsByAnimalPerYear(s, animal):
    cheeseMilkProportion = s.get('creamery/{}/cheese milk pct'.format(animal)) * 0.01
    cheeseMilkLbsYield = s.get('creamery/{}/cheese yield lbs per gallon'.format(animal))
    cheeseMilkLossProportion = s.get('creamery/cheese yield loss pct') * 0.01
    cheeseMilkLbsPerDay = milkGallonsPerDay(s, animal) * cheeseMilkProportion * cheeseMilkLbsYield * (1.0 - cheeseMilkLossProportion)
    return cheeseMilkLbsPerDay * 365.0


def cheeseLbsByAnimalPerWeek(s, animal):
    return cheeseLbsByAnimalPerYear(s, animal) * (7.0 / 365.0)


def cheeseSalesByAnimalPerYear(s, animal):
    pricePerLb = s.get('creamery/{}/cheese price per lb'.format(animal))
    return cheeseLbsByAnimalPerYear(s, animal) * pricePerLb


def cheeseSessionsPerWeek(s, animal):
    vatSize = s.get('creamery/vat size gal')
    gallonsPerYear = cheeseGallonsUsedByAnimalPerYear(s, animal)
    return (gallonsPerYear / float(vatSize)) / (365.0 / 7.0) if vatSize > 0 else 0.0


def cheeseCaveSqft(s):
    # Assumptions: each wheel is no bigger than 12x12 inches, shelves allow us to stack 5 tall,
    # they'll age for average 6 months, and we need 50% extra space to walk
    sellableCheeseWheelsPerYear = 0.0
    animals = livestockList(s)
    for animal in animals:
        sellableCheeseLbsPerYear = cheeseLbsByAnimalPerYear(s, animal)
        lbsPerWheel = s.get('creamery/{}/cheese lbs per wheel'.format(animal))
        sellableCheeseWheelsPerYear += sellableCheeseLbsPerYear / lbsPerWheel if lbsPerWheel > 0 else 0.0
    return sellableCheeseWheelsPerYear * 0.5 * (1.0 / 5.0) * 1.5


def cheeseHoursByAnimalPerYear(s, animal):
    vatSize = s.get('creamery/vat size gal')
    cheeseSessionHours = s.get('creamery/cheese session hours')
    cheeseGallonsPerYear = cheeseGallonsUsedByAnimalPerYear(s, animal)
    cheeseHours = cheeseSessionHours * cheeseGallonsPerYear / float(vatSize) if vatSize > 0 else 0.0
    return cheeseHours


#
# Ice cream
#


def iceCreamMilkGallonsUsedByAnimalPerYear(s, animal):
    iceCreamMilkProportion = s.get('creamery/{}/ice cream milk pct'.format(animal)) * 0.01
    iceCreamMilkGallonsPerDay = milkGallonsPerDay(s, animal) * iceCreamMilkProportion
    return iceCreamMilkGallonsPerDay * 365.0


def iceCreamGallonsByAnimalPerYear(s, animal):
    iceCreamMilkProportion = s.get('creamery/{}/ice cream milk pct'.format(animal)) * 0.01
    iceCreamMilkGallonsYield = s.get('creamery/{}/ice cream yield gallons per gallon'.format(animal))
    iceCreamGallonsPerDay = milkGallonsPerDay(s, animal) * iceCreamMilkProportion * iceCreamMilkGallonsYield
    return iceCreamGallonsPerDay * 365.0


def iceCreamGallonsByAnimalPerWeek(s, animal):
    return iceCreamGallonsByAnimalPerYear(s, animal) * (7.0 / 365.0)


def iceCreamSalesByAnimalPerYear(s, animal):
    pricePerGallon = s.get('creamery/{}/ice cream price per gallon'.format(animal))
    return iceCreamGallonsByAnimalPerYear(s, animal) * pricePerGallon


def iceCreamSessionsPerWeek(s, animal):
    iceCreamGallonsPerSession = s.get('creamery/ice cream session gal')
    iceCreamGallonsPerYear = iceCreamMilkGallonsUsedByAnimalPerYear(s, animal)
    return (iceCreamGallonsPerYear / float(iceCreamGallonsPerSession)) / (365.0 / 7.0) if iceCreamGallonsPerSession > 0 else 0.0


def iceCreamHoursByAnimalPerYear(s, animal):
    iceCreamSessionHours = s.get('creamery/ice cream session hours')
    iceCreamGallonsPerSession = s.get('creamery/ice cream session gal')
    iceCreamGallonsPerYear = iceCreamMilkGallonsUsedByAnimalPerYear(s, animal)
    iceCreamHours = iceCreamSessionHours * iceCreamGallonsPerYear / float(iceCreamGallonsPerSession) if iceCreamGallonsPerSession > 0 else 0.0
    return iceCreamHours


#
# Butter
#


def butterGallonsUsedByAnimalPerYear(s, animal):
    butterGallonsProportion = s.get('creamery/{}/butter milk pct'.format(animal)) * 0.01
    butterGallonsPerDay = milkGallonsPerDay(s, animal) * butterGallonsProportion
    return butterGallonsPerDay * 365.0


def butterLbsByAnimalPerYear(s, animal):
    butterGallonsProportion = s.get('creamery/{}/butter milk pct'.format(animal)) * 0.01
    butterGallonsYield = s.get('creamery/{}/butter yield lbs per gallon'.format(animal))
    butterLbsPerDay = milkGallonsPerDay(s, animal) * butterGallonsProportion * butterGallonsYield
    return butterLbsPerDay * 365.0


def butterLbsByAnimalPerWeek(s, animal):
    return butterLbsByAnimalPerYear(s, animal) * (7.0 / 365.0)


def butterSalesByAnimalPerYear(s, animal):
    pricePerLb = s.get('creamery/{}/butter price per lb'.format(animal))
    return butterLbsByAnimalPerYear(s, animal) * pricePerLb


def buttermilkGallonsByAnimalPerYear(s, animal):
    butterGallonsProportion = s.get('creamery/{}/butter milk pct'.format(animal)) * 0.01
    buttermilkGallonsYield = s.get('creamery/{}/buttermilk yield gallons per gallon'.format(animal))
    buttermilkGallonsPerDay = milkGallonsPerDay(s, animal) * butterGallonsProportion * buttermilkGallonsYield
    return buttermilkGallonsPerDay * 365.0


def buttermilkGallonsByAnimalPerWeek(s, animal):
    return buttermilkGallonsByAnimalPerYear(s, animal) * (7.0 / 365.0)


def buttermilkSalesByAnimalPerYear(s, animal):
    pricePerGallon = s.get('creamery/{}/buttermilk price per gallon'.format(animal))
    return buttermilkGallonsByAnimalPerYear(s, animal) * pricePerGallon


def butterSessionsPerWeek(s, animal):
    butterGallonsPerSession = s.get('creamery/butter session gal')
    butterGallonsPerYear = butterGallonsUsedByAnimalPerYear(s, animal)
    return (butterGallonsPerYear / float(butterGallonsPerSession)) / (365.0 / 7.0) if butterGallonsPerSession > 0 else 0.0


def butterHoursByAnimalPerYear(s, animal):
    butterSessionHours = s.get('creamery/butter session hours')
    butterGallonsPerSession = s.get('creamery/butter session gal')
    butterGallonsPerYear = butterGallonsUsedByAnimalPerYear(s, animal)
    butterHours = butterSessionHours * butterGallonsPerYear / float(butterGallonsPerSession) if butterGallonsPerSession > 0 else 0.0
    return butterHours


#
# Cream
#


def creamMilkGallonsUsedByAnimalPerYear(s, animal):
    creamMilkProportion = s.get('creamery/{}/cream milk pct'.format(animal)) * 0.01
    creamMilkGallonsPerDay = milkGallonsPerDay(s, animal) * creamMilkProportion
    return creamMilkGallonsPerDay * 365.0


def creamGallonsByAnimalPerYear(s, animal):
    creamMilkProportion = s.get('creamery/{}/cream milk pct'.format(animal)) * 0.01
    creamMilkGallonsYield = s.get('creamery/{}/cream yield gallons per gallon'.format(animal))
    creamGallonsPerDay = milkGallonsPerDay(s, animal) * creamMilkProportion * creamMilkGallonsYield
    return creamGallonsPerDay * 365.0


def creamGallonsByAnimalPerWeek(s, animal):
    return creamGallonsByAnimalPerYear(s, animal) * (7.0 / 365.0)


def creamSalesByAnimalPerYear(s, animal):
    pricePerGallon = s.get('creamery/{}/cream price per gallon'.format(animal))
    return creamGallonsByAnimalPerYear(s, animal) * pricePerGallon


def creamSessionsPerWeek(s, animal):
    creamGallonsPerSession = s.get('creamery/cream session gal')
    creamGallonsPerYear = creamMilkGallonsUsedByAnimalPerYear(s, animal)
    return (creamGallonsPerYear / float(creamGallonsPerSession)) / (365.0 / 7.0) if creamGallonsPerSession > 0 else 0.0


def creamHoursByAnimalPerYear(s, animal):
    creamSessionHours = s.get('creamery/cream session hours')
    creamGallonsPerSession = s.get('creamery/cream session gal')
    creamGallonsPerYear = creamMilkGallonsUsedByAnimalPerYear(s, animal)
    creamHours = creamSessionHours * creamGallonsPerYear / float(creamGallonsPerSession) if creamGallonsPerSession > 0 else 0.0
    return creamHours


#
# Yogurt
#


def yogurtMilkGallonsUsedByAnimalPerYear(s, animal):
    yogurtMilkProportion = s.get('creamery/{}/yogurt milk pct'.format(animal)) * 0.01
    yogurtMilkGallonsPerDay = milkGallonsPerDay(s, animal) * yogurtMilkProportion
    return yogurtMilkGallonsPerDay * 365.0


def yogurtGallonsByAnimalPerYear(s, animal):
    yogurtMilkProportion = s.get('creamery/{}/yogurt milk pct'.format(animal)) * 0.01
    yogurtMilkGallonsYield = s.get('creamery/{}/yogurt yield gallons per gallon'.format(animal))
    yogurtGallonsPerDay = milkGallonsPerDay(s, animal) * yogurtMilkProportion * yogurtMilkGallonsYield
    return yogurtGallonsPerDay * 365.0


def yogurtGallonsByAnimalPerWeek(s, animal):
    return yogurtGallonsByAnimalPerYear(s, animal) * (7.0 / 365.0)


def yogurtSalesByAnimalPerYear(s, animal):
    pricePerGallon = s.get('creamery/{}/yogurt price per gallon'.format(animal))
    return yogurtGallonsByAnimalPerYear(s, animal) * pricePerGallon


def yogurtSessionsPerWeek(s, animal):
    yogurtGallonsPerSession = s.get('creamery/yogurt session gal')
    yogurtGallonsPerYear = yogurtMilkGallonsUsedByAnimalPerYear(s, animal)
    return (yogurtGallonsPerYear / float(yogurtGallonsPerSession)) / (365.0 / 7.0) if yogurtGallonsPerSession > 0 else 0.0


def yogurtHoursByAnimalPerYear(s, animal):
    yogurtSessionHours = s.get('creamery/yogurt session hours')
    yogurtGallonsPerSession = s.get('creamery/yogurt session gal')
    yogurtGallonsPerYear = yogurtMilkGallonsUsedByAnimalPerYear(s, animal)
    yogurtHours = yogurtSessionHours * yogurtGallonsPerYear / float(yogurtGallonsPerSession) if yogurtGallonsPerSession > 0 else 0.0
    return yogurtHours


#
# General creamery
#


def creameryFacilitySqft(s):
    creameryArea = s.get('creamery/creamery sqft')
    overheadArea = s.get('structures/creamery/overhead sqft')
    caveArea = cheeseCaveSqft(s)
    return creameryArea + caveArea + overheadArea


def creameryFacilityCost(s):
    costPerSqft = s.get('structures/creamery/cost per sqft')
    return creameryFacilitySqft(s) * costPerSqft


def creameryCommonCostPerYear(s):
    amortizationYears = s.get('farm/amortization years')
    fixedAmortizationActive = True if s.get('farm/years running') <= amortizationYears else False

    cost = 0.0
    if fixedAmortizationActive:
        totalFixedCosts = 0.0
        fixedCosts = s.get('creamery/fixed/* cost')
        if fixedCosts:
            for c in fixedCosts:
                totalFixedCosts += c
            cost += amortizedLoanPayment(totalFixedCosts, s.get('farm/fixed cost loan rate') * 0.01, amortizationYears * 12) * 12
        cost += amortizedLoanPayment(creameryFacilityCost(s), s.get('farm/facility loan rate') * 0.01, amortizationYears * 12) * 12
    yearlyCosts = s.get('creamery/yearly/* cost')
    if yearlyCosts:
        for c in yearlyCosts:
            cost += c
    return cost


def creameryCommonCostProportion(s, animal):
    totalGallons = 0
    animalGallons = 0
    animals = livestockList(s)
    for a in animals:
        gallons = cheeseGallonsUsedByAnimalPerYear(s, a)
        gallons += butterGallonsUsedByAnimalPerYear(s, a)
        gallons += creamMilkGallonsUsedByAnimalPerYear(s, a)
        gallons += iceCreamMilkGallonsUsedByAnimalPerYear(s, a)
        gallons += yogurtMilkGallonsUsedByAnimalPerYear(s, a)
        if a == animal:
            animalGallons = gallons
        totalGallons += gallons
    return animalGallons / float(totalGallons) if totalGallons > 0 else 0


def creameryGrossIncomeByAnimalPerYear(s, animal):
    sales = cheeseSalesByAnimalPerYear(s, animal)
    sales += creamSalesByAnimalPerYear(s, animal)
    sales += iceCreamSalesByAnimalPerYear(s, animal)
    sales += butterSalesByAnimalPerYear(s, animal)
    sales += buttermilkSalesByAnimalPerYear(s, animal)
    sales += yogurtSalesByAnimalPerYear(s, animal)
    return sales


def creameryNetIncomeByAnimalPerYearNoEmployees(s, animal):
    income = creameryGrossIncomeByAnimalPerYear(s, animal)
    costs = creameryCommonCostPerYear(s) * creameryCommonCostProportion(s, animal)
    return income - costs


def creameryHoursByAnimalPerYear(s, animal):
    return cheeseHoursByAnimalPerYear(s, animal) + iceCreamHoursByAnimalPerYear(s, animal)


def creameryHoursByAnimalPerWeek(s, animal):
    return creameryHoursByAnimalPerYear(s, animal) * (7.0 / 365.0)


def creameryEmployeeHoursByAnimalPerYear(s, animal):
    cheeseHoursPerYear = cheeseHoursByAnimalPerYear(s, animal)
    cheeseSessionHours = s.get('creamery/cheese session hours')
    selfTimeCheeseHoursPerSession = s.get('creamery/cheese self hours'.format(animal))
    employeeCheeseHoursPerSession = max(0, cheeseSessionHours - selfTimeCheeseHoursPerSession)
    employeeCheeseHoursProportion = (employeeCheeseHoursPerSession / cheeseSessionHours) if cheeseSessionHours > 0 else 0

    butterHoursPerYear = butterHoursByAnimalPerYear(s, animal)
    butterSessionHours = s.get('creamery/butter session hours')
    selfTimeButterHoursPerSession = s.get('creamery/butter self hours'.format(animal))
    employeeButterHoursPerSession = max(0, butterSessionHours - selfTimeButterHoursPerSession)
    employeeButterHoursProportion = (employeeButterHoursPerSession / butterSessionHours) if butterSessionHours > 0 else 0

    creamHoursPerYear = creamHoursByAnimalPerYear(s, animal)
    creamSessionHours = s.get('creamery/cream session hours')
    selfTimeCreamHoursPerSession = s.get('creamery/cream self hours'.format(animal))
    employeeCreamHoursPerSession = max(0, creamSessionHours - selfTimeCreamHoursPerSession)
    employeeCreamHoursProportion = (employeeCreamHoursPerSession / creamSessionHours) if creamSessionHours > 0 else 0

    iceCreamHoursPerYear = iceCreamHoursByAnimalPerYear(s, animal)
    iceCreamSessionHours = s.get('creamery/ice cream session hours')
    selfTimeIceCreamHoursPerSession = s.get('creamery/ice cream self hours'.format(animal))
    employeeIceCreamHoursPerSession = max(0, iceCreamSessionHours - selfTimeIceCreamHoursPerSession)
    employeeIceCreamHoursProportion = (employeeIceCreamHoursPerSession / iceCreamSessionHours) if iceCreamSessionHours > 0 else 0

    yogurtHoursPerYear = yogurtHoursByAnimalPerYear(s, animal)
    yogurtSessionHours = s.get('creamery/yogurt session hours')
    selfTimeYogurtHoursPerSession = s.get('creamery/yogurt self hours'.format(animal))
    employeeYogurtHoursPerSession = max(0, yogurtSessionHours - selfTimeYogurtHoursPerSession)
    employeeYogurtHoursProportion = (employeeYogurtHoursPerSession / yogurtSessionHours) if yogurtSessionHours > 0 else 0

    totalHours = 0
    totalHours += cheeseHoursPerYear * employeeCheeseHoursProportion
    totalHours += butterHoursPerYear * employeeButterHoursProportion
    totalHours += creamHoursPerYear * employeeCreamHoursProportion
    totalHours += iceCreamHoursPerYear * employeeIceCreamHoursProportion
    totalHours += yogurtHoursPerYear * employeeYogurtHoursProportion
    return totalHours


def creameryEmployeeHoursByAnimalPerDay(s, animal):
    return creameryEmployeeHoursByAnimalPerYear(s, animal) / 365.0


def creameryEmployeeHoursByAnimalPerWeek(s, animal):
    return creameryEmployeeHoursByAnimalPerYear(s, animal) * (7.0 / 365.0)


def creameryEmployeeExpectedPayRatePerHour(s):
    minPayRate = s.get('creamery/employee/min pay per hour')
    maxPayRate = s.get('creamery/employee/max pay per hour')
    totalHoursPerYear = 0
    totalCreameryIncomePerYear = 0
    animals = livestockList(s)
    for animal in animals:
        totalHoursPerYear += creameryEmployeeHoursByAnimalPerYear(s, animal)
        totalCreameryIncomePerYear += creameryNetIncomeByAnimalPerYearNoEmployees(s, animal)
    if totalHoursPerYear <= 0:
        return minPayRate
    return min(maxPayRate, max(minPayRate, totalCreameryIncomePerYear / totalHoursPerYear))


# Returns a tuple of (pay, overhead)
def creameryEmployeeExpectedPayPerYear(s):
    payRatePerHour = creameryEmployeeExpectedPayRatePerHour(s)
    totalHoursPerYear = 0
    animals = livestockList(s)
    for animal in animals:
        totalHoursPerYear += creameryEmployeeHoursByAnimalPerYear(s, animal)
    incomePerYear = payRatePerHour * totalHoursPerYear
    overheadPerYear = incomeOverhead(s, incomePerYear)
    return (incomePerYear, overheadPerYear)


def cheeseCostPerCWT(s, animal):
    '''
    livestockCost = livestockCostPerYear(s, animal)
    livestockCommonCost = livestockCommonCostPerYear(s)
    milkCommonCost = milkCommonCostPerYear(s)
    dairyEmployeeCost, dairyEmployeeOverhead = dairyEmployeeExpectedPayPerYear(s)
    creameryCommonCost = creameryCommonCostPerYear(s)
    creameryEmployeeCost, creameryEmployeeOverhead = creameryEmployeeExpectedPayPerYear(s)
    lbsSoldPerYear = cheeseLbsByAnimalPerYear(s, animal)
    cheesedProportion = s.get('creamery/{}/cheese milk pct'.format(animal)) * 0.01

    gallons = cheeseGallonsUsedByAnimalPerYear(s, animal)
    gallons += butterGallonsUsedByAnimalPerYear(s, animal)
    gallons += creamMilkGallonsUsedByAnimalPerYear(s, animal)
    gallons += iceCreamMilkGallonsUsedByAnimalPerYear(s, animal)
    gallons += yogurtMilkGallonsUsedByAnimalPerYear(s, animal)
    cheeseOnlyProportion = cheeseGallonsUsedByAnimalPerYear(s, animal) / gallons if gallons > 0 else 0.0

    totalAnimalCost = (livestockCost + livestockCommonCost * livestockCommonCostProportion(s, animal)) * cheesedProportion
    totalAnimalCost += (milkCommonCost + dairyEmployeeCost + dairyEmployeeOverhead) * dairyCommonCostProportion(s, animal) * cheesedProportion
    totalAnimalCost += (creameryCommonCost + creameryEmployeeCost + creameryEmployeeOverhead) * creameryCommonCostProportion(s, animal) * cheeseOnlyProportion
    return totalAnimalCost * 100.0 / lbsSoldPerYear if lbsSoldPerYear > 0 else 0.0
    '''
    # This is essentially what's leftover from sales per 100 lbs minus profit per 100 lbs
    salePricePerLb = s.get('creamery/{}/cheese price per lb'.format(animal))
    salePricePerCWT = salePricePerLb * 100.0
    return salePricePerCWT - cheeseProfitPerCWT(s, animal)


def cheeseCostPerLb(s, animal):
    return cheeseCostPerCWT(s, animal) / 100.0


def cheeseProfitPerCWT(s, animal):
    lbsSoldPerYear = cheeseLbsByAnimalPerYear(s, animal)
    netIncome = creameryNetIncomeByAnimalPerYear(s, animal)

    # This is an estimate of the creamery costs attributed to cheese
    gallons = cheeseGallonsUsedByAnimalPerYear(s, animal)
    gallons += butterGallonsUsedByAnimalPerYear(s, animal)
    gallons += creamMilkGallonsUsedByAnimalPerYear(s, animal)
    gallons += iceCreamMilkGallonsUsedByAnimalPerYear(s, animal)
    gallons += yogurtMilkGallonsUsedByAnimalPerYear(s, animal)
    cheeseOnlyProportion = cheeseGallonsUsedByAnimalPerYear(s, animal) / gallons if gallons > 0 else 0.0

    return netIncome * cheeseOnlyProportion * 100 / lbsSoldPerYear if lbsSoldPerYear > 0 else 0.0


def cheeseProfitPerLb(s, animal):
    return cheeseProfitPerCWT(s, animal) / 100.0


def creameryNetIncomeByAnimalPerYear(s, animal):
    income = creameryNetIncomeByAnimalPerYearNoEmployees(s, animal)
    dairyEmployeeCost, dairyEmployeeOverhead = dairyEmployeeExpectedPayPerYear(s)
    employeeCost, employeeOverhead = creameryEmployeeExpectedPayPerYear(s)
    # Only attribute portion of dairy employee cost to (milk to creamery gallons)/(total milk)
    creameryProportion = 0
    creameryProportions = s.get('creamery/{}/* pct'.format(animal))
    for p in creameryProportions:
        creameryProportion += p * 0.01
    employeePartCost1 = (dairyEmployeeCost + dairyEmployeeOverhead) * dairyCommonCostProportion(s, animal) * creameryProportion
    employeePartCost2 = (employeeCost + employeeOverhead) * creameryCommonCostProportion(s, animal)
    return income - employeePartCost1 - employeePartCost2
