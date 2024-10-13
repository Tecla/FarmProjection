# This Python file uses the following encoding: utf-8

from .Utilities import *


def neededAcresByAnimal(s, animal):
    existingFemales = s.get('livestock/{}/existing females'.format(animal))
    purchasedFemales = s.get('livestock/{}/purchased females'.format(animal))
    existingMales = s.get('livestock/{}/existing males'.format(animal))
    purchasedMales = s.get('livestock/{}/purchased males'.format(animal))
    acresPerHead = s.get('livestock/{}/acres'.format(animal))
    acresTotal = (existingFemales + purchasedFemales + existingMales + purchasedMales) * float(acresPerHead)
    return acresTotal


def neededAcres(s):
    acresTotal = 0.0
    animals = livestockList(s)
    for animal in animals:
        existingFemales = s.get('livestock/{}/existing females'.format(animal))
        purchasedFemales = s.get('livestock/{}/purchased females'.format(animal))
        existingMales = s.get('livestock/{}/existing males'.format(animal))
        purchasedMales = s.get('livestock/{}/purchased males'.format(animal))
        acresPerHead = s.get('livestock/{}/acres'.format(animal))
        acresTotal += (existingFemales + purchasedFemales + existingMales + purchasedMales) * float(acresPerHead)
    return acresTotal


def livestockBeddingCost(s, animal):
    barnSqft = s.get('livestock/{}/barn sqft'.format(animal))
    beddingDepthInches = s.get('livestock/{}/bedding depth inches'.format(animal))
    beddingRefreshes = s.get('livestock/{}/bedding refreshes'.format(animal))
    cheapBaleCost = s.get('farm/feed/cheap hay cost per small bale')

    cubicInchesOfBedding = barnSqft * 12 * 12 * beddingDepthInches * beddingRefreshes
    cubicInchesOfBale = 14 * 18 * 36
    return float(cheapBaleCost) * float(cubicInchesOfBedding) / float(cubicInchesOfBale)


def livestockHayCost(s, animal):
    hayTons = s.get('livestock/{}/yearly/hay tons'.format(animal))
    monthsOnPasture = s.get('farm/pasture/months')
    hayCostPerTon = s.get('farm/feed/premium hay cost per ton')

    return (hayCostPerTon * hayTons / 2.0) * (1.0 - monthsOnPasture / 12.0)


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


def livestockCommonCostPerYear(s):
    amortizationYears = s.get('farm/amortization years')
    fixedAmortizationActive = True if s.get('farm/years running') <= amortizationYears else False

    cost = 0.0
    if fixedAmortizationActive:
        fixedCosts = s.get('farm/fixed/* cost')
        for c in fixedCosts:
            cost += c / float(amortizationYears) if amortizationYears > 0 else 0.0
        cost += barnCost(s) / float(amortizationYears) if amortizationYears > 0 else 0.0
    yearlyCosts = s.get('farm/yearly/* cost')
    for c in yearlyCosts:
        cost += c
    return cost


def livestockIncomePerYear(s, animal):
    sales = livestockSalesPerYear(s, animal)
    costs = livestockCostPerYear(s, animal)
    costs += livestockCommonCostPerYear(s) * livestockCommonCostProportion(s, animal)
    return sales - costs


def livestockNetIncomePerYear(s, animal):
    income = livestockIncomePerYear(s, animal)
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
    return livestockEmployeeHoursPerYear(s, animal) / 365.0


def livestockEmployeeExpectedPayRatePerHour(s):
    minPayRate = s.get('livestock/employee/min pay per hour')
    maxPayRate = s.get('livestock/employee/max pay per hour')
    totalHoursPerYear = 0
    totalIncomePerYear = 0
    animals = livestockList(s)
    for animal in animals:
        totalHoursPerYear += livestockEmployeeHoursPerYear(s, animal)
        totalIncomePerYear += livestockIncomePerYear(s, animal)
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
