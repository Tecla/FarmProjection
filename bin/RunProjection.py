#!/bin/env python
# This Python file uses the following encoding: utf-8

import argparse
import os
import inspect
import sys


# Find script location, and from there add to the python path so we can use
# common scripts
binDir = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
modulePythonPath = os.path.join(binDir, '..', 'module')
if modulePythonPath not in sys.path:
    sys.path.append(modulePythonPath)

import Farm


if __name__ == "__main__":
    # Set up program arguments
    parser = argparse.ArgumentParser(description="Run farm projection")
    parser.add_argument('scenarios', nargs='*', default='', help="Scenario to run (in <datadir>/scenarios/<scenario>). Use 'all' or leave blank to run all scenarios.")
    parser.add_argument('--datadir', default='', help="Data directory location with common and scenarios subdirectories")
    parser.add_argument('--reportdir', default='', help="Location to write reports to. If not specified, reports are written to <datadir>/reports")
    parser.add_argument('--set', nargs=2, action='append', metavar=("INPUT", "VALUE"), help="Override a value from the scenario. The input is a path through the JSON values, e.g. structures/creamery/cost per sqft; so you may need to put the input path in quotes.")
    args = parser.parse_args()

    if not args.datadir or len(args.datadir) == 0:
        dataDir = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), '..', 'data'))
    else:
        dataDir = os.path.realpath(args.datadir)
    defaultDataDir = os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), '..', 'default-data')
    defaultScenario = Farm.Scenario(os.path.join(defaultDataDir, 'common'), os.path.join(defaultDataDir, 'scenarios', 'default'))

    if not args.reportdir or len(args.reportdir) == 0:
        reportDir = os.path.join(dataDir, 'reports')
        if not os.path.exists(dataDir):
            print("ERROR: data directory doesn't exist, no report subdirectory will be created within it: {}".format(dataDir))
            exit(1)
        if not os.path.exists(reportDir):
            os.mkdir(reportDir, 0o755)
    else:
        reportDir = args.reportdir

    scenariosList = []
    if (args.scenarios is None) or (len(args.scenarios) == 0) or ('all' in args.scenarios):
        dirList = os.listdir(os.path.join(dataDir, 'scenarios'))
        for item in dirList:
            if os.path.isdir(os.path.join(dataDir, 'scenarios', item)):
                scenariosList += [ item ]
    else:
        scenariosList = args.scenarios

    firstScenario = True
    for scenarioName in scenariosList:
        if firstScenario:
            firstScenario = False
        else:
            print('')

        scenario = Farm.Scenario(os.path.join(dataDir, 'common'), os.path.join(dataDir, 'scenarios', scenarioName), defaultScenario, args.set)

        report = Farm.GenerateReport(scenario)
        Farm.GenerateReportJson(report, os.path.join(reportDir, scenarioName + '.json'))
        Farm.GenerateReportHtml(report, os.path.join(reportDir, scenarioName + '.html'), scenarioName)
        print('')
        Farm.ProjectProfit(scenario, scenarioName)
