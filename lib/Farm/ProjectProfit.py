# This Python file uses the following encoding: utf-8

from .Dairy import *
from .Livestock import *
from .Creamery import *
from .Store import *
from .Utilities import *


def incomeByAnimalPerYear(s, animal):
    income = 0
    income += livestockIncomePerYear(s, animal)
    income += milkIncomeByAnimalPerYear(s, animal)
    income += creameryIncomeByAnimalPerYear(s, animal)
    return income

def netIncomeByAnimalPerYear(s, animal):
    income = 0
    income += livestockNetIncomePerYear(s, animal)
    income += dairyNetIncome(s, animal)
    income += creameryNetIncomeByAnimalPerYear(s, animal)
    return income

def netSelfPayPerYearEstimate(netIncome):
    return netIncome * (1.0 - 0.05 - 0.0145 * 1.5 - 0.1 - 0.22) - min(netIncome, 168600) * 0.062 * 1.5


def ProjectProfit(scenario):
    s = scenario
    print("Summary")
    print("=======")
    print('')
    print("Total acres needed: {}".format(neededAcres(s)))
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

    income = 0
    netIncome = 0
    for animal in animals:
        incomeByAnimal = incomeByAnimalPerYear(s, animal)
        netIncomeByAnimal = netIncomeByAnimalPerYear(s, animal)
        print("Income and net income for {}s: {}, {}".format(animal, dollars(incomeByAnimal), dollars(netIncomeByAnimal)))
        income += incomeByAnimal
        netIncome += netIncomeByAnimal
    income += storeIncomePerYear(s)
    print('Total income: {}'.format(dollars(income)))
    print('')

    totalNetIncome = netIncome
    totalNetIncome += storeNetIncomePerYear(s)
    print('Total profit: {}'.format(dollars(totalNetIncome)))

    netPayEstimate = netSelfPayPerYearEstimate(totalNetIncome)
    print('Self net estimate: {} (per month: {})'.format(dollars(netPayEstimate), dollars(netPayEstimate / 12.0)))
