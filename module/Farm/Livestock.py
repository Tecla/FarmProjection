# This Python file uses the following encoding: utf-8

from .Utilities import *

import math


def perAcreAUMs(s):
    # "Enough" water for a productive pasture is defined as equivalent of 20 inches of precipitation
    # This can be achieved by rain, snow, or irrigation
    precipitationInches = s.get('farm/pasture/precipitation inches per year')
    irrigationInches = s.get('farm/pasture/irrigation inches per year')
    totalInches = precipitationInches + irrigationInches
    fertilityProportion = s.get('farm/pasture/soil fertility')

    # Forage production AUMs per year based on: https://extension.usu.edu/smallfarms/research/forage-needs

    # Up to 10 AUMs per acre on very fertile soil, up to about 5 on poor soil (fertility proportion 0.5)
    perAcreAUMs = 10.0 * fertilityProportion
    # Water AUMs multiplier ranges from about 0.1 at 12 inches of water per year to 1.0 at 20 inches of water
    # Equation is (clamped between 0.0 and 1.0): modifier = 9*inches/80 - 1.25
    waterAUMMod = totalInches * (9.0 / 80.0) - 1.25
    if waterAUMMod < 0.0:
        waterAUMMod = 0.0
    elif waterAUMMod > 1.0:
        waterAUMMode = 1.0
    perAcreAUMs *= waterAUMMod
    return perAcreAUMs

def soilProductivityProportion(s):
    return perAcreAUMs(s) / 10.0

def perAnimalAUs(s, animal):
    existingFemales = s.get('livestock/{}/existing females'.format(animal))
    purchasedFemales = s.get('livestock/{}/purchased females'.format(animal))
    existingMales = s.get('livestock/{}/existing males'.format(animal))
    purchasedMales = s.get('livestock/{}/purchased males'.format(animal))
    offspringPerFemale = s.get('livestock/{}/yearly/offspring'.format(animal))
    maleAUs = s.get('livestock/{}/male AUs'.format(animal))
    femaleAUs = s.get('livestock/{}/female AUs'.format(animal))
    offspringAUs = s.get('livestock/{}/weaned offspring AUs'.format(animal))
    totalAUs = maleAUs * (existingMales + purchasedMales) + femaleAUs * (existingFemales + purchasedFemales) + offspringAUs * ((existingFemales + purchasedFemales) * offspringPerFemale)
    return totalAUs

def totalAUs(s):
    total = 0.0
    animals = livestockList(s)
    for animal in animals:
        total += perAnimalAUs(s, animal)
    return total

def neededAcresByAnimal(s, animal):
    totalAUs = perAnimalAUs(s, animal)
    acresPerAUM = perAcreAUMs(s)
    monthsOnPasture = s.get('farm/pasture/months')
    # Total acres needed is AUs * months-on-pasture / AUMs-per-acre
    acresTotal = totalAUs * monthsOnPasture / acresPerAUM if acresPerAUM > 0.0 else 0.0
    return acresTotal

def neededAcres(s):
    acresTotal = 0.0
    animals = livestockList(s)
    for animal in animals:
        acresTotal += neededAcresByAnimal(s, animal)
    return acresTotal

def livestockPaddocks(s):
    # Based on https://attra.ncat.org/publication/irrigated-pastures-setting-up-an-intensive-grazing-system-that-works/
    rotationDays = s.get('farm/pasture/paddock rotation in days')
    recoveryDays = s.get('farm/pasture/paddock recovery in days')
    if rotationDays <= 0.0:
        return 0.0
    paddocks = math.ceil(recoveryDays / rotationDays) + 1
    return paddocks

def livestockPaddockSize(s, animal):
    acres = neededAcresByAnimal(s, animal)
    paddocks = livestockPaddocks(s)
    return acres / paddocks if paddocks > 0.0 else 0.0


def totalIrrigationWaterAcreFeet(s):
    totalAcres = neededAcres(s)
    irrigationInches = s.get('farm/pasture/irrigation inches per year')
    return totalAcres * irrigationInches / 12.0


def livestockBeddingCost(s, animal):
    barnSqft = s.get('livestock/{}/barn sqft'.format(animal))
    beddingDepthInches = s.get('livestock/{}/bedding depth inches'.format(animal))
    beddingRefreshes = s.get('livestock/{}/bedding refreshes'.format(animal))
    cheapBaleCost = s.get('farm/feed/cheap hay cost per small bale')

    cubicInchesOfBedding = barnSqft * 12 * 12 * beddingDepthInches * beddingRefreshes
    cubicInchesOfBale = 14 * 18 * 36
    return float(cheapBaleCost) * float(cubicInchesOfBedding) / float(cubicInchesOfBale)

def livestockHayTons(s, animal, perHead=True):
    hayPercentOfBodyweight = s.get('livestock/{}/hay pct of bodyweight daily'.format(animal))
    monthsOnPasture = s.get('farm/pasture/months')
    hayWastePct = s.get('farm/feed/premium hay waste pct')
    animalAUs = perAnimalAUs(s, animal)
    totalAnimals = livestockTotal(s, animal) + offspringPerYear(s, animal)
    # Rough estimate of hay requirements per lb of body weight for the whole year
    hayLbs = animalAUs * 1000.0 * hayPercentOfBodyweight * 365.0
    if totalAnimals > 0.0:
        hayLbs /= totalAnimals
    else:
        hayLbs = 0.0
    hayTons = hayLbs / 2000.0
    hayTons /= 1.0 + hayWastePct
    hayTons *= 1.0 - monthsOnPasture / 12.0
    if perHead:
        return hayTons
    else:
        return hayTons * totalAnimals

def livestockHayCost(s, animal):
    hayCostPerTon = s.get('farm/feed/premium hay cost per ton')
    return hayCostPerTon * livestockHayTons(s, animal)

def livestockTotalHayTons(s):
    total = 0.0
    animals = livestockList(s)
    for animal in animals:
        total += livestockHayTons(s, animal, False)
    return total

def livestockCostPerYear(s, animal):
    maleCount = livestockAdultMales(s, animal)
    malePurchased = s.get('livestock/{}/purchased males'.format(animal))
    femaleCount = livestockAdultFemales(s, animal)
    femalePurchased = s.get('livestock/{}/purchased females'.format(animal))
    offspring = s.get('livestock/{}/yearly/offspring'.format(animal))
    femalePurchasePrice = s.get('livestock/{}/female purchase price'.format(animal))
    malePurchasePrice = s.get('livestock/{}/male purchase price'.format(animal))
    amortizationYears = s.get('livestock/{}/amortization years'.format(animal))

    fixedCosts = s.get('livestock/{}/fixed/* cost'.format(animal))
    yearlyCosts = s.get('livestock/{}/yearly/* cost'.format(animal))
    cost = 0
    # Offspring are assumed to need only half of the costs of the adults
    headAmount = maleCount
    headAmount += femaleCount * (1.0 + offspring * 0.5)
    if fixedCosts is not None:
        for fixedCost in fixedCosts:
            cost += fixedCost * headAmount
    if yearlyCosts is not None:
        for yearlyCost in yearlyCosts:
            cost += yearlyCost * headAmount
    if amortizationYears > 0:
        cost += femalePurchased * femalePurchasePrice / amortizationYears
        cost += malePurchased * malePurchasePrice / amortizationYears
    cost += (livestockBeddingCost(s, animal) + livestockHayCost(s, animal)) * headAmount

    return cost


def livestockTotal(s, animal):
    existingHead = s.get('livestock/{}/existing females'.format(animal))
    existingHead += s.get('livestock/{}/existing males'.format(animal))
    purchasedHead = s.get('livestock/{}/purchased females'.format(animal))
    purchasedHead += s.get('livestock/{}/purchased males'.format(animal))
    return existingHead + purchasedHead


def livestockAdultMales(s, animal):
    existingHead = s.get('livestock/{}/existing males'.format(animal))
    purchasedHead = s.get('livestock/{}/purchased males'.format(animal))
    return existingHead + purchasedHead


def livestockAdultFemales(s, animal):
    existingHead = s.get('livestock/{}/existing females'.format(animal))
    purchasedHead = s.get('livestock/{}/purchased females'.format(animal))
    return existingHead + purchasedHead


def offspringPerYear(s, animal):
    existingHead = s.get('livestock/{}/existing females'.format(animal))
    purchasedHead = s.get('livestock/{}/purchased females'.format(animal))
    offspring = s.get('livestock/{}/yearly/offspring'.format(animal))

    return (existingHead + purchasedHead) * offspring


def livestockSalesPerYear(s, animal):
    offspring = offspringPerYear(s, animal)
    sellPrice = s.get('livestock/{}/offspring price'.format(animal))

    return offspring * sellPrice


def barnSqft(s):
    overheadProportion = s.get('structures/barn/overhead sqft pct') * 0.01 # Extra space for alleys, etc
    animals = livestockList(s)
    totalSqft = 0
    for animal in animals:
        # TODO: include calves/lambs/etc somehow
        count = livestockTotal(s, animal)
        barnSqft = s.get('livestock/{}/barn sqft'.format(animal))
        totalSqft += count * barnSqft
    return totalSqft * (1.0 + overheadProportion)


def barnCost(s):
    costPerSqft = s.get('structures/barn/cost per sqft')
    return barnSqft(s) * costPerSqft


def livestockFenceCost(s):
    permFenceCostPerFt = s.get('farm/fence/permanent fence cost per ft')
    tempFenceCostPerFt = s.get('farm/fence/temporary fence cost per ft')
    corralFenceCostPerFt = s.get('farm/fence/corral fence cost per ft')
    permFenceLength = s.get('farm/fence/permanent fence ft')
    tempFenceLength = s.get('farm/fence/temporary fence ft')
    corralFenceLength = s.get('farm/fence/corral fence ft')
    return permFenceCostPerFt * permFenceLength + tempFenceCostPerFt * tempFenceLength + corralFenceCostPerFt * corralFenceLength

def livestockCommonCostPerYear(s):
    amortizationYears = s.get('farm/amortization years')
    fixedAmortizationActive = True if s.get('farm/years running') <= amortizationYears else False

    cost = 0.0
    if fixedAmortizationActive:
        totalFixedCosts = 0.0
        fixedCosts = s.get('farm/fixed/* cost')
        if fixedCosts:
            for c in fixedCosts:
                totalFixedCosts += c
        totalFixedCosts += livestockFenceCost(s)
        cost += amortizedLoanPayment(totalFixedCosts, s.get('farm/fixed cost loan rate') * 0.01, amortizationYears * 12) * 12
        cost += amortizedLoanPayment(barnCost(s), s.get('farm/facility loan rate') * 0.01, amortizationYears * 12) * 12
    yearlyCosts = s.get('farm/yearly/* cost')
    for c in yearlyCosts:
        cost += c
    return cost


def livestockGrossIncomePerYear(s, animal):
    sales = livestockSalesPerYear(s, animal)
    return sales


def livestockNetIncomePerYearNoEmployees(s, animal):
    income = livestockSalesPerYear(s, animal)
    costs = livestockCostPerYear(s, animal)
    costs += livestockCommonCostPerYear(s) * livestockCommonCostProportion(s, animal)
    return income - costs


def livestockNetIncomePerYear(s, animal):
    income = livestockNetIncomePerYearNoEmployees(s, animal)
    employeeCost, employeeOverhead = livestockEmployeeExpectedPayPerYear(s)
    # Only attribute portion of employee cost to (time dealing with this animal)/(total time for all animals)
    employeePartCost = (employeeCost + employeeOverhead) * livestockCommonCostProportion(s, animal, 'animal time')
    return income - employeePartCost


def livestockCommonCostProportion(s, animal, method=None):
    if not method:
        method = s.get('farm/facility cost split method')
    if method == 'animal cost':
        animalCost = 0
        totalCost = 0
        for a in livestockList(s):
            cost = livestockCostPerYear(s, a)
            if a == animal:
                animalCost = cost
            totalCost += cost
        return animalCost / totalCost if totalCost > 0 else 0.0
    elif method == 'animal space':
        animalSpace = neededAcresByAnimal(s, animal)
        totalSpace = neededAcres(s)
        return animalSpace / totalSpace if totalSpace > 0 else 0.0
    elif method == 'animal time':
        animalTime = s.get('livestock/{}/hours per week'.format(animal))
        totalTime = 0.0
        for a in livestockList(s):
            totalTime += s.get('livestock/{}/hours per week'.format(a))
        return animalTime / totalTime if totalTime > 0 else 0.0
    elif method == 'blended':
        costProp = livestockCommonCostProportion(s, animal, 'animal cost')
        spaceProp = livestockCommonCostProportion(s, animal, 'animal space')
        timeProp = livestockCommonCostProportion(s, animal, 'animal time')
        return (costProp + spaceProp + timeProp) / 3.0
    else:
        print("Unkown livestock common cost method: {}".format(method))
        return 0.0


def livestockList(s):
    animals = s.get('farm/animals')
    return animals


def livestockHoursPerYear(s, animal):
    animalHoursPerYear = s.get('livestock/{}/hours per week'.format(animal)) * (365.0 / 7.0)
    return animalHoursPerYear


def livestockHoursPerWeek(s, animal):
    return s.get('livestock/{}/hours per week'.format(animal))


def livestockHoursPerDay(s, animal):
    return livestockHoursPerYear(s, animal) / 365.0


def livestockEmployeeHoursPerYear(s, animal):
    animalHoursPerYear = s.get('livestock/{}/hours per week'.format(animal)) * (365.0 / 7.0)
    selfHoursPerYear = s.get('livestock/{}/self hours per week'.format(animal)) * (365.0 / 7.0)
    return max(0.0, animalHoursPerYear - selfHoursPerYear)


def livestockEmployeeHoursPerWeek(s, animal):
    animalHoursPerWeek = s.get('livestock/{}/hours per week'.format(animal))
    selfHoursPerWeek = s.get('livestock/{}/self hours per week'.format(animal))
    return max(0.0, animalHoursPerWeek - selfHoursPerWeek)


def livestockEmployeeHoursPerDay(s, animal):
    return livestockEmployeeHoursPerWeek(s, animal) / 7.0


def livestockEmployeeExpectedPayRatePerHour(s):
    minPayRate = s.get('livestock/employee/min pay per hour')
    maxPayRate = s.get('livestock/employee/max pay per hour')
    totalHoursPerYear = 0
    totalIncomePerYear = 0
    animals = livestockList(s)
    for animal in animals:
        totalHoursPerYear += livestockEmployeeHoursPerYear(s, animal)
        totalIncomePerYear += livestockNetIncomePerYearNoEmployees(s, animal)
    if totalHoursPerYear <= 0:
        return minPayRate
    return min(maxPayRate, max(minPayRate, totalIncomePerYear / totalHoursPerYear))


# Returns a tuple of (pay, overhead)
def livestockEmployeeExpectedPayPerYear(s):
    payRatePerHour = livestockEmployeeExpectedPayRatePerHour(s)
    totalHoursPerYear = 0
    animals = livestockList(s)
    for animal in animals:
        totalHoursPerYear += livestockEmployeeHoursPerYear(s, animal)
    incomePerYear = payRatePerHour * totalHoursPerYear
    overheadPerYear = incomeOverhead(s, incomePerYear)
    return (incomePerYear, overheadPerYear)
