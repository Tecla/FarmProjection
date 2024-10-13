# This Python file uses the following encoding: utf-8

from .Livestock import *


def milkGallonsLostPerYear(s, animal):
    yieldLossProportion = s.get('milk/milk yield loss pct') * 0.01
    adultFemales = livestockAdultFemales(s, animal)
    peakGallons = s.get('livestock/{}/peak gallons'.format(animal))
    dryMonths = s.get('livestock/{}/dry months'.format(animal))
    return adultFemales * peakGallons * (1.0 - dryMonths / 12.0) * 0.5 * yieldLossProportion * 365.0


def milkGallonsPerDay(s, animal):
    yieldLossProportion = s.get('milk/milk yield loss pct') * 0.01
    adultFemales = livestockAdultFemales(s, animal)
    peakGallons = s.get('livestock/{}/peak gallons'.format(animal))
    dryMonths = s.get('livestock/{}/dry months'.format(animal))
    return adultFemales * peakGallons * (1.0 - dryMonths / 12.0) * 0.5 * (1.0 - yieldLossProportion)


def milkGallonsSoldPerWeek(s, animal):
    gallonsPerDay = milkGallonsPerDay(s, animal)
    bottledProportion = s.get('milk/{}/bottled pct'.format(animal)) * 0.01
    return gallonsPerDay * bottledProportion * 7.0


def milkSalesPerYear(s, animal):
    salePricePerGallon = s.get('milk/{}/sale price per gallon'.format(animal))
    return milkGallonsSoldPerWeek(s, animal) * salePricePerGallon * (365.0/7.0)


def dairyFacilitySqft(s):
    milkhouseSqft = s.get('structures/dairy/milkhouse sqft')
    bathroomSqft = s.get('structures/dairy/bathroom sqft')
    overheadSqft = s.get('structures/dairy/overhead sqft')
    parlorSqft = 0
    animals = livestockList(s)
    for animal in animals:
        stands = s.get('milk/{}/stands'.format(animal))
        standSqft = s.get('livestock/{}/milk stand sqft'.format(animal))
        parlorSqft += stands * standSqft
    return milkhouseSqft + bathroomSqft + parlorSqft + overheadSqft


def dairyFacilityCost(s):
    costPerSqft = s.get('structures/dairy/cost per sqft')
    return dairyFacilitySqft(s) * costPerSqft


def milkCostByAnimalPerYear(s, animal):
    milkGallonsPerYear = milkGallonsSoldPerWeek(s, animal) * (365.0/7.0)
    cost = 0.0
    perGallonCosts = s.get('milk/per gallon/* cost')
    for c in perGallonCosts:
        cost += c
    return milkGallonsPerYear * cost


def milkCommonCostPerYear(s):
    amortizationYears = s.get('farm/amortization years')
    fixedAmortizationActive = True if s.get('farm/years running') <= amortizationYears else False

    cost = 0
    if fixedAmortizationActive:
        fixedCosts = s.get('milk/fixed/* cost')
        for c in fixedCosts:
            cost += c / float(amortizationYears)
        cost += dairyFacilityCost(s) / float(amortizationYears)
    yearlyCosts = s.get('milk/yearly/* cost')
    for c in yearlyCosts:
        cost += c
    return cost


def dairyCommonCostProportion(s, animal):
    animalTime = 0
    totalTime = 0
    for a in livestockList(s):
        time = milkHoursPerYear(s, a)
        if a == animal:
            animalTime = time
        totalTime += time
    return animalTime / totalTime if totalTime > 0 else 0


def milkIncomeByAnimalPerYear(s, animal):
    sales = milkSalesPerYear(s, animal)
    costs = milkCostByAnimalPerYear(s, animal)
    costs += milkCommonCostPerYear(s) * dairyCommonCostProportion(s, animal)
    return sales - costs


def milkHoursPerYear(s, animal):
    adultFemales = livestockAdultFemales(s, animal)
    sessionOverheadMin = s.get('milk/{}/milking overhead minutes'.format(animal))
    sessionPerHeadMin = s.get('milk/{}/milking minutes'.format(animal))
    stands = s.get('milk/{}/stands'.format(animal))
    sessionsPerDay = s.get('milk/{}/milkings per day'.format(animal))

    if stands > 0:
        minutesPerDay = (sessionOverheadMin + adultFemales * sessionPerHeadMin / float(stands)) * sessionsPerDay
    else:
        minutesPerDay = 0
    return minutesPerDay * 365.0 / 60.0


def milkHoursPerDay(s, animal):
    return milkHoursPerYear(s, animal) / 365.0


def milkHoursPerSession(s, animal):
    sessionsPerDay = s.get('milk/{}/milkings per day'.format(animal))
    return milkHoursPerDay(s, animal) / sessionsPerDay


def milkHoursPerSession(s, animal):
    adultFemales = livestockAdultFemales(s, animal)
    sessionOverheadMin = s.get('milk/{}/milking overhead minutes'.format(animal))
    sessionPerHeadMin = s.get('milk/{}/milking minutes'.format(animal))
    stands = s.get('milk/{}/stands'.format(animal))

    return (sessionOverheadMin + adultFemales * sessionPerHeadMin / float(stands)) / 60.0 if stands > 0 else 0.0


def dairyEmployeeHoursPerYear(s, animal):
    animalHoursPerYear = milkHoursPerYear(s, animal)
    selfTimeProportion = s.get('milk/{}/self time pct'.format(animal)) * 0.01
    return animalHoursPerYear * (1.0 - selfTimeProportion)


def dairyEmployeeHoursPerDay(s, animal):
    return dairyEmployeeHoursPerYear(s, animal) / 365.0


def dairyEmployeeHoursPerWeek(s, animal):
    return dairyEmployeeHoursPerYear(s, animal) * (7.0 / 365.0)


def dairyEmployeeExpectedPayRatePerHour(s):
    minPayRate = s.get('milk/employee/min pay per hour')
    maxPayRate = s.get('milk/employee/max pay per hour')
    totalHoursPerYear = 0
    totalMilkIncomePerYear = 0
    animals = livestockList(s)
    for animal in animals:
        totalHoursPerYear += dairyEmployeeHoursPerYear(s, animal)
        totalMilkIncomePerYear += milkIncomeByAnimalPerYear(s, animal)
    if totalHoursPerYear <= 0:
        return minPayRate
    return min(maxPayRate, max(minPayRate, totalMilkIncomePerYear / totalHoursPerYear))


# Returns a tuple of (pay, overhead)
def dairyEmployeeExpectedPayPerYear(s):
    payRatePerHour = dairyEmployeeExpectedPayRatePerHour(s)
    totalHoursPerYear = 0
    animals = livestockList(s)
    for animal in animals:
        totalHoursPerYear += dairyEmployeeHoursPerYear(s, animal)
    incomePerYear = payRatePerHour * totalHoursPerYear
    overheadPerYear = incomePerYear * (0.062 + 0.0145)
    return (incomePerYear, overheadPerYear)


gallonWeightLbs = 8.6


def milkCostPerCWT(s, animal):
    '''
    livestockCost = livestockCostPerYear(s, animal)
    livestockCommonCost = livestockCommonCostPerYear(s)
    milkCost = milkCostByAnimalPerYear(s, animal)
    milkCommonCost = milkCommonCostPerYear(s)
    employeeCost, employeeOverhead = dairyEmployeeExpectedPayPerYear(s)
    gallonsSoldPerYear = milkGallonsSoldPerWeek(s, animal) * (365.0 / 7.0)
    bottledProportion = s.get('milk/{}/bottled pct'.format(animal)) * 0.01

    totalAnimalCost = (livestockCost + livestockCommonCost * livestockCommonCostProportion(s, animal)) * bottledProportion
    totalAnimalCost += milkCost + (milkCommonCost + employeeCost + employeeOverhead) * dairyCommonCostProportion(s, animal) * bottledProportion
    return totalAnimalCost * 100.0 / (gallonsSoldPerYear * gallonWeightLbs) if gallonsSoldPerYear > 0 else 0.0
    '''
    # This is essentially what's leftover from sales per 100 lbs minus profit per 100 lbs
    salePricePerGallon = s.get('milk/{}/sale price per gallon'.format(animal))
    salePricePerCWT = salePricePerGallon * 100.0 / gallonWeightLbs
    return salePricePerCWT - milkProfitPerCWT(s, animal)


def milkCostPerGallon(s, animal):
    return milkCostPerCWT(s, animal) * gallonWeightLbs / 100.0


def milkProfitPerCWT(s, animal):
    gallonsSoldPerYear = milkGallonsSoldPerWeek(s, animal) * (365.0 / 7.0)
    netIncome = dairyNetIncome(s, animal)
    return netIncome * 100 / (gallonsSoldPerYear * gallonWeightLbs) if gallonsSoldPerYear > 0 else 0.0


def milkProfitPerGallon(s, animal):
    return milkProfitPerCWT(s, animal) * gallonWeightLbs / 100.0


def dairyNetIncome(s, animal):
    income = milkIncomeByAnimalPerYear(s, animal)
    employeeCost, employeeOverhead = dairyEmployeeExpectedPayPerYear(s)
    # Only attribute portion of dairy employee cost to (time milking this animal)/(total milking time)
    bottledProportion = s.get('milk/{}/bottled pct'.format(animal)) * 0.01
    employeePartCost = (employeeCost + employeeOverhead) * dairyCommonCostProportion(s, animal) * bottledProportion
    return income - employeePartCost

