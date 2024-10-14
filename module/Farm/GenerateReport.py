# This Python file uses the following encoding: utf-8

import json
from xml.etree import ElementTree as ET
import xml.dom.minidom

from .Dairy import *
from .Livestock import *
from .Creamery import *
from .Store import *
from .ProjectProfit import *
from .Utilities import *


def GenerateReport(scenario):
    s = scenario
    root = {}
    root['Farm'] = {}
    root['Livestock'] = {}
    root['Dairy'] = {}
    root['Creamery'] = {}
    root['Store'] = {}
    root['Employees'] = {}
    root['Income'] = {}

    # Farm report
    amortizationYears = s.get('farm/amortization years')
    currentYear = s.get('farm/years running')
    fixedAmortizationActive = True if currentYear <= amortizationYears else False
    root['Farm']['Acres needed'] = neededAcres(s)
    root['Farm']['Months on pasture'] = s.get('farm/pasture/months')
    root['Farm']['Fixed costs paid off'] = 'No' if fixedAmortizationActive else 'Yes'
    root['Farm']['Fixed costs year'] = '{} of {}'.format(currentYear, amortizationYears)

    # Livestock report
    animals = livestockList(s)
    root['Livestock']['Animals'] = animals
    root['Livestock']['Barn cost'] = dollars(barnCost(s))
    root['Livestock']['Barn sqft'] = round(barnSqft(s), 0)
    root['Livestock']['Fence cost'] = dollars(livestockFenceCost(s))
    root['Livestock']['Common cost per year'] = dollars(livestockCommonCostPerYear(s))
    for a in animals:
        root['Livestock'][a] = {}
        root['Livestock'][a]['Head'] = livestockTotal(s, a)
        offspringName = s.get('livestock/{}/offspring name'.format(a))
        root['Livestock'][a]['{} born'.format(offspringName)] = offspringPerYear(s, a)
        root['Livestock'][a]['Cost per year'] = dollars(livestockCostPerYear(s, a))
        root['Livestock'][a]['Pct of common cost'] = '{}%'.format(round(livestockCommonCostProportion(s, a) * 100, 1))
        root['Livestock'][a]['Bedding cost per head'] = dollars(livestockBeddingCost(s, a))
        root['Livestock'][a]['Hay cost per head'] = dollars(livestockHayCost(s, a))
        root['Livestock'][a]['Sales of {}s'.format(a)] = dollars(livestockSalesPerYear(s, a))
        root['Livestock'][a]['Income per year'] = dollars(livestockIncomePerYear(s, a))
        root['Livestock'][a]['Net income per year'] = dollars(livestockNetIncomePerYear(s, a))
        root['Livestock'][a]['Work hours per year'] = rounded(livestockHoursPerYear(s, a), 2)
        root['Livestock'][a]['Work hours per week'] = rounded(livestockHoursPerWeek(s, a), 2)
        root['Livestock'][a]['Work hours per day'] = rounded(livestockHoursPerDay(s, a), 2)
        root['Livestock'][a]['Employee hours per year'] = rounded(livestockEmployeeHoursPerYear(s, a), 0)
        root['Livestock'][a]['Employee hours per week'] = rounded(livestockEmployeeHoursPerWeek(s, a), 2)
        root['Livestock'][a]['Employee hours per day'] = rounded(livestockEmployeeHoursPerDay(s, a), 2)

    # Dairy report
    root['Dairy']['Building cost'] = dollars(dairyFacilityCost(s))
    root['Dairy']['Building sqft'] = round(dairyFacilitySqft(s), 0)
    root['Dairy']['Common cost per year'] = dollars(milkCommonCostPerYear(s))
    for a in animals:
        root['Dairy'][a] = {}
        root['Dairy'][a]['Gallons per day'] = rounded(milkGallonsPerDay(s, a), 4)
        root['Dairy'][a]['Gallons sold per week'] = rounded(milkGallonsSoldPerWeek(s, a), 2)
        root['Dairy'][a]['Milk sales per year'] = dollars(milkSalesPerYear(s, a))
        root['Dairy'][a]['Gallons lost per year'] = rounded(milkGallonsLostPerYear(s, a), 2)
        root['Dairy'][a]['Cost per year'] = dollars(milkCostByAnimalPerYear(s, a))
        root['Dairy'][a]['Cost per CWT'] = dollars(milkCostPerCWT(s, a))
        root['Dairy'][a]['Cost per gallon'] = dollars(milkCostPerGallon(s, a))
        root['Dairy'][a]['Pct of common cost'] = '{}%'.format(round(dairyCommonCostProportion(s, a) * 100, 1))
        root['Dairy'][a]['Income per year'] = dollars(milkIncomeByAnimalPerYear(s, a))
        root['Dairy'][a]['Net income per year'] = dollars(dairyNetIncome(s, a))
        root['Dairy'][a]['Profit per CWT'] = dollars(milkProfitPerCWT(s, a))
        root['Dairy'][a]['Profit per gallon'] = dollars(milkProfitPerGallon(s, a))
        root['Dairy'][a]['Milking hours per year'] = rounded(milkHoursPerYear(s, a), 2)
        root['Dairy'][a]['Milking hours per day'] = rounded(milkHoursPerDay(s, a), 2)
        root['Dairy'][a]['Milking hours per session'] = rounded(milkHoursPerSession(s, a), 4)
        root['Dairy'][a]['Employee hours per year'] = rounded(dairyEmployeeHoursPerYear(s, a), 0)
        root['Dairy'][a]['Employee hours per week'] = rounded(dairyEmployeeHoursPerWeek(s, a), 2)
        root['Dairy'][a]['Employee hours per day'] = rounded(dairyEmployeeHoursPerDay(s, a), 2)

    # Creamery report
    root['Creamery']['Building cost'] = dollars(creameryFacilityCost(s))
    root['Creamery']['Building sqft'] = round(creameryFacilitySqft(s), 0)
    root['Creamery']['Cheese cave sqft'] = rounded(cheeseCaveSqft(s), 0)
    root['Creamery']['Common cost per year'] = dollars(creameryCommonCostPerYear(s))
    for a in animals:
        root['Creamery'][a] = {}
        root['Creamery'][a]['Butter gallons used per year'] = rounded(butterGallonsUsedByAnimalPerYear(s, a), 2)
        root['Creamery'][a]['Butter lbs sold per year'] = rounded(butterLbsByAnimalPerYear(s, a), 0)
        root['Creamery'][a]['Butter lbs sold per week'] = rounded(butterLbsByAnimalPerWeek(s, a), 2)
        root['Creamery'][a]['Butter sales per year'] = dollars(butterSalesByAnimalPerYear(s, a))
        root['Creamery'][a]['Butter sessions per week'] = rounded(butterSessionsPerWeek(s, a), 4)
        root['Creamery'][a]['Cheese gallons used per year'] = rounded(cheeseGallonsUsedByAnimalPerYear(s, a), 2)
        root['Creamery'][a]['Cheese lbs sold per year'] = rounded(cheeseLbsByAnimalPerYear(s, a), 0)
        root['Creamery'][a]['Cheese lbs sold per week'] = rounded(cheeseLbsByAnimalPerWeek(s, a), 2)
        root['Creamery'][a]['Cheese sales per year'] = dollars(cheeseSalesByAnimalPerYear(s, a))
        root['Creamery'][a]['Cheese cost per CWT'] = dollars(cheeseCostPerCWT(s, a))
        root['Creamery'][a]['Cheese cost per lb'] = dollars(cheeseCostPerLb(s, a))
        root['Creamery'][a]['Cheese profit per CWT'] = dollars(cheeseProfitPerCWT(s, a))
        root['Creamery'][a]['Cheese profit per lb'] = dollars(cheeseProfitPerLb(s, a))
        root['Creamery'][a]['Cheese sessions per week'] = rounded(cheeseSessionsPerWeek(s, a), 4)
        root['Creamery'][a]['Cream gallons used per year'] = rounded(creamMilkGallonsUsedByAnimalPerYear(s, a), 2)
        root['Creamery'][a]['Cream gallons sold per year'] = rounded(creamGallonsByAnimalPerYear(s, a), 0)
        root['Creamery'][a]['Cream gallons sold per week'] = rounded(creamGallonsByAnimalPerWeek(s, a), 2)
        root['Creamery'][a]['Cream sales per year'] = dollars(creamSalesByAnimalPerYear(s, a))
        root['Creamery'][a]['Cream sessions per week'] = rounded(creamSessionsPerWeek(s, a), 4)
        root['Creamery'][a]['Ice cream gallons used per year'] = rounded(iceCreamMilkGallonsUsedByAnimalPerYear(s, a), 2)
        root['Creamery'][a]['Ice cream gallons sold per year'] = rounded(iceCreamGallonsByAnimalPerYear(s, a), 0)
        root['Creamery'][a]['Ice cream gallons sold per week'] = rounded(iceCreamGallonsByAnimalPerWeek(s, a), 2)
        root['Creamery'][a]['Ice cream sales per year'] = dollars(iceCreamSalesByAnimalPerYear(s, a))
        root['Creamery'][a]['Ice cream sessions per week'] = rounded(iceCreamSessionsPerWeek(s, a), 4)
        root['Creamery'][a]['Yogurt gallons used per year'] = rounded(yogurtMilkGallonsUsedByAnimalPerYear(s, a), 2)
        root['Creamery'][a]['Yogurt gallons sold per year'] = rounded(yogurtGallonsByAnimalPerYear(s, a), 0)
        root['Creamery'][a]['Yogurt gallons sold per week'] = rounded(yogurtGallonsByAnimalPerWeek(s, a), 2)
        root['Creamery'][a]['Yogurt sales per year'] = dollars(yogurtSalesByAnimalPerYear(s, a))
        root['Creamery'][a]['Yogurt sessions per week'] = rounded(yogurtSessionsPerWeek(s, a), 4)
        root['Creamery'][a]['Income per year'] = dollars(creameryIncomeByAnimalPerYear(s, a))
        root['Creamery'][a]['Net income per year'] = dollars(creameryNetIncomeByAnimalPerYear(s, a))
        root['Creamery'][a]['Pct of common cost'] = '{}%'.format(round(creameryCommonCostProportion(s, a) * 100, 1))
        root['Creamery'][a]['Creamery hours per year'] = rounded(creameryHoursByAnimalPerYear(s, a), 0)
        root['Creamery'][a]['Creamery hours per week'] = rounded(creameryHoursByAnimalPerWeek(s, a), 2)
        root['Creamery'][a]['Employee hours per year'] = rounded(creameryEmployeeHoursByAnimalPerYear(s, a), 0)
        root['Creamery'][a]['Employee hours per week'] = rounded(creameryEmployeeHoursByAnimalPerWeek(s, a), 2)
        root['Creamery'][a]['Employee hours per day'] = rounded(creameryEmployeeHoursByAnimalPerDay(s, a), 4)

    # Store report
    root['Store']['Building cost'] = dollars(storeFacilityCost(s))
    root['Store']['Building sqft'] = round(storeFacilitySqft(s), 0)
    root['Store']['Common cost per year'] = dollars(storeCommonCostPerYear(s))
    root['Store']['Hours per year'] = rounded(storeHoursPerYear(s), 0)
    root['Store']['Employee hours per year'] = rounded(storeEmployeeHoursPerYear(s), 0)
    root['Store']['Employee hours per week'] = rounded(storeEmployeeHoursPerWeek(s), 2)

    # Employees report
    livestockEmployeeYearlyPay, livestockEmployeeYearlyOverhead = livestockEmployeeExpectedPayPerYear(s)
    dairyEmployeeYearlyPay, dairyEmployeeYearlyOverhead = dairyEmployeeExpectedPayPerYear(s)
    creameryEmployeeYearlyPay, creameryEmployeeYearlyOverhead = creameryEmployeeExpectedPayPerYear(s)
    storeEmployeeYearlyPay, storeEmployeeYearlyOverhead = storeEmployeeExpectedPayPerYear(s)
    livestockEmployeeHourlyPay = livestockEmployeeExpectedPayRatePerHour(s)
    dairyEmployeeHourlyPay = dairyEmployeeExpectedPayRatePerHour(s)
    creameryEmployeeHourlyPay = creameryEmployeeExpectedPayRatePerHour(s)
    storeEmployeeHourlyPay = storeEmployeeExpectedPayRatePerHour(s)
    root['Employees']['Livestock'] = {}
    root['Employees']['Dairy'] = {}
    root['Employees']['Creamery'] = {}
    root['Employees']['Store'] = {}
    root['Employees']['Livestock']['Yearly pay'] = dollars(livestockEmployeeYearlyPay)
    root['Employees']['Livestock']['Yearly overhead'] = dollars(livestockEmployeeYearlyOverhead)
    root['Employees']['Livestock']['Hourly pay'] = dollars(livestockEmployeeHourlyPay)
    totalHoursPerYear = 0.0
    totalHoursPerWeek = 0.0
    totalHoursPerDay = 0.0
    for a in animals:
        totalHoursPerYear += livestockEmployeeHoursPerYear(s, a)
        totalHoursPerWeek += livestockEmployeeHoursPerWeek(s, a)
        totalHoursPerDay += livestockEmployeeHoursPerDay(s, a)
    root['Employees']['Livestock']['Hours per year'] = rounded(totalHoursPerYear, 0)
    root['Employees']['Livestock']['Hours per week'] = rounded(totalHoursPerWeek, 2)
    root['Employees']['Livestock']['Hours per day'] = rounded(totalHoursPerDay, 4)
    root['Employees']['Dairy']['Yearly pay'] = dollars(dairyEmployeeYearlyPay)
    root['Employees']['Dairy']['Yearly overhead'] = dollars(dairyEmployeeYearlyOverhead)
    root['Employees']['Dairy']['Hourly pay'] = dollars(dairyEmployeeHourlyPay)
    totalHoursPerYear = 0.0
    totalHoursPerWeek = 0.0
    totalHoursPerDay = 0.0
    for a in animals:
        totalHoursPerYear += dairyEmployeeHoursPerYear(s, a)
        totalHoursPerWeek += dairyEmployeeHoursPerWeek(s, a)
        totalHoursPerDay += dairyEmployeeHoursPerDay(s, a)
    root['Employees']['Dairy']['Hours per year'] = rounded(totalHoursPerYear, 0)
    root['Employees']['Dairy']['Hours per week'] = rounded(totalHoursPerWeek, 2)
    root['Employees']['Dairy']['Hours per day'] = rounded(totalHoursPerDay, 4)
    root['Employees']['Creamery']['Yearly pay'] = dollars(creameryEmployeeYearlyPay)
    root['Employees']['Creamery']['Yearly overhead'] = dollars(creameryEmployeeYearlyOverhead)
    root['Employees']['Creamery']['Hourly pay'] = dollars(creameryEmployeeHourlyPay)
    totalHoursPerYear = 0.0
    totalHoursPerWeek = 0.0
    totalHoursPerDay = 0.0
    for a in animals:
        totalHoursPerYear += creameryEmployeeHoursByAnimalPerYear(s, a)
        totalHoursPerWeek += creameryEmployeeHoursByAnimalPerWeek(s, a)
        totalHoursPerDay += creameryEmployeeHoursByAnimalPerDay(s, a)
    root['Employees']['Creamery']['Hours per year'] = rounded(totalHoursPerYear, 0)
    root['Employees']['Creamery']['Hours per week'] = rounded(totalHoursPerWeek, 2)
    root['Employees']['Creamery']['Hours per day'] = rounded(totalHoursPerDay, 4)
    root['Employees']['Store']['Yearly pay'] = dollars(storeEmployeeYearlyPay)
    root['Employees']['Store']['Yearly overhead'] = dollars(storeEmployeeYearlyOverhead)
    root['Employees']['Store']['Hourly pay'] = dollars(storeEmployeeHourlyPay)
    root['Employees']['Store']['Hours per year'] = rounded(storeEmployeeHoursPerYear(s), 0)
    root['Employees']['Store']['Hours per week'] = rounded(storeEmployeeHoursPerWeek(s), 2)

    # Income report
    income = 0
    netIncome = 0
    animals = livestockList(s)
    for animal in animals:
        incomeByAnimal = incomeByAnimalPerYear(s, animal)
        netIncomeByAnimal = netIncomeByAnimalPerYear(s, animal)
        root['Income'][animal] = {}
        root['Income'][animal]['Income'] = dollars(incomeByAnimal)
        root['Income'][animal]['Net income'] = dollars(netIncomeByAnimal)
        income += incomeByAnimal
        netIncome += netIncomeByAnimal
    income += storeIncomePerYear(s)
    root['Income']['Total income'] = dollars(income)

    totalNetIncome = netIncome
    totalNetIncome += storeNetIncomePerYear(s)
    root['Income']['Total profit'] = dollars(totalNetIncome)

    netPayEstimate = netSelfPayPerYearEstimate(s, totalNetIncome)
    root['Income']['Self net yearly estimate'] = dollars(netPayEstimate)
    root['Income']['Self net monthly estimate'] = dollars(netPayEstimate / 12.0)

    return root


def GenerateReportJson(reportRoot, outputJsonFile):
    with open(outputJsonFile, 'w') as outputFile:
        print("Writing report: {}".format(outputJsonFile))
        json.dump(reportRoot, outputFile, indent=4)


def GenerateReportHtml(reportRoot, outputHtmlFile, scenarioName):
    with open(outputHtmlFile, 'w') as outputFile:
        print("Writing report: {}".format(outputHtmlFile))

        html = ET.Element('html')
        head = ET.SubElement(html, 'head')
        style = ET.SubElement(head, 'style')
        style.text = """
table, th, td {
    border-collapse: collapse;
    border: 0px;
}
th, td {
    padding: 3px;
}
th {
    text-align: right;
}
"""
        body = ET.SubElement(html, 'body')
        title = ET.SubElement(body, 'h1')
        title.text = "Projection Report: {}".format(scenarioName)
        rootTable = ET.SubElement(body, 'table')

        for groupName, group in reportRoot.items():
            if not isinstance(group, dict):
                continue
            groupRow = ET.SubElement(rootTable, 'tr')
            groupTitleHeader = ET.SubElement(groupRow, 'th')
            groupTitle = ET.SubElement(groupTitleHeader, 'h2')
            groupTitle.text = groupName
            groupData = ET.SubElement(groupRow, 'td')
            groupTable = ET.SubElement(groupData, 'table')
            groupTable.set('style', 'border:1px solid;')
            groupSubgroupsRow = None
            for groupElementName, groupElement in group.items():
                if not isinstance(groupElement, dict):
                    groupElementRow = ET.SubElement(groupTable, 'tr')
                    groupElementTitle = ET.SubElement(groupElementRow, 'th')
                    groupElementTitle.text = groupElementName
                    groupElementData = ET.SubElement(groupElementRow, 'td')
                    if isinstance(groupElement, list):
                        listElement = ET.SubElement(groupElementData, 'ul')
                        for item in groupElement:
                            listItem = ET.SubElement(listElement, 'li')
                            listItem.text = item
                    else:
                        groupElementData.text = str(groupElement)
                else:
                    if not groupSubgroupsRow:
                        groupSubgroupsRow = ET.SubElement(groupTable, 'tr')
                    groupElementData = ET.SubElement(groupSubgroupsRow, 'td')
                    groupElementTitleHeader = ET.SubElement(groupElementData, 'th')
                    groupElementTitle = ET.SubElement(groupElementTitleHeader, 'h3')
                    groupElementTitle.text = groupElementName
                    subgroupElementData = ET.SubElement(groupElementData, 'td')
                    subgroupElementTable = ET.SubElement(subgroupElementData, 'table')
                    subgroupElementTable.set('style', 'border:1px dotted;')
                    for subgroupElementName, subgroupElement in groupElement.items():
                        subgroupElementRow = ET.SubElement(subgroupElementTable, 'tr')
                        subgroupElementTitle = ET.SubElement(subgroupElementRow, 'th')
                        subgroupElementTitle.text = subgroupElementName
                        subgroupElementData = ET.SubElement(subgroupElementRow, 'td')
                        subgroupElementData.text = str(subgroupElement)

        xmlDom = xml.dom.minidom.parseString(ET.tostring(html, method='html').decode('utf-8'))
        outputFile.write("<!DOCTYPE html>\n");
        outputFile.write(xmlDom.toprettyxml(indent=" "))
