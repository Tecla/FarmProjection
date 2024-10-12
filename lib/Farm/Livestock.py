# This Python file uses the following encoding: utf-8

def neededAcresByAnimal(s, animal):
    existingFemales = s.get('livestock/{}/existing females'.format(animal))
    purchasedFemales = s.get('livestock/{}/purchased females'.format(animal))
    existingMales = s.get('livestock/{}/existing males'.format(animal))
    purchasedMales = s.get('livestock/{}/purchased males'.format(animal))
    acresPerHead = s.get('livestock/{}/acres'.format(animal))
    acresTotal = (existingFemales + purchasedFemales + existingMales + purchasedMales) * float(acresPerHead)
    return acresTotal


def neededAcres(s):
    existingFemales = s.get('livestock/*/existing females')
    purchasedFemales = s.get('livestock/*/purchased females')
    existingMales = s.get('livestock/*/existing males')
    purchasedMales = s.get('livestock/*/purchased males')
    acresPerHead = s.get('livestock/*/acres')
    acresTotal = 0.0
    for existingF, purchasedF, existingM, purchasedM, acres in zip(existingFemales, purchasedFemales, existingMales, purchasedMales, acresPerHead):
        acresTotal += (existingF + purchasedF + existingM + purchasedM) * float(acres)
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
    animals = livestockList(s)
    totalSqft = 0
    for animal in animals:
        # TODO: include calves/lambs/etc somehow
        count = livestockTotal(s, animal)
        barnSqft = s.get('livestock/{}/barn sqft'.format(animal))
        totalSqft += count * barnSqft
    # 20% extra space for alleys, etc
    return totalSqft * 1.2


def barnCost(s):
    costPerSqft = s.get('structures/barn/cost per sqft')
    return barnSqft(s) * costPerSqft


def livestockCommonCostPerYear(s):
    amortizationYears = s.get('farm/amortization years')
    fixedAmortizationActive = True if s.get('farm/years running') <= amortizationYears else False

    cost = 0
    if fixedAmortizationActive:
        fixedCosts = s.get('farm/fixed/* cost')
        for c in fixedCosts:
            cost += c / float(amortizationYears)
        cost += barnCost(s) / float(amortizationYears)
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
    # TODO: account for livestock employees?
    return livestockIncomePerYear(s, animal)


def livestockCommonCostProportion(s, animal):
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
    else:
        print("Unkown livestock common cost method: {}".format(method))
        return 0.0


def livestockList(s):
    animals = s.get('farm/animals')
    return animals
