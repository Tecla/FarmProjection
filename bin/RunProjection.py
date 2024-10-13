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
    parser.add_argument('scenario', help="Scenario to run (in data/scenarios/<scenario>)")
    parser.add_argument('--datadir', default='', help="Data directory location with common and scenarios subdirectories")
    parser.add_argument('--report', default='', help="Location to write reports to (will add report extension automatically)")
    parser.add_argument('--report_json', action='store_true', help='Write JSON report')
    parser.add_argument('--report_html', action='store_true', help='Write HTML report')
    args = parser.parse_args()

    if not args.datadir or len(args.datadir) == 0:
        dataDir = os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), '..', 'data')
    else:
        dataDir = args.datadir
    defaultDataDir = os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), '..', 'default-data')
    defaultScenario = Farm.Scenario(os.path.join(defaultDataDir, 'common'), os.path.join(defaultDataDir, 'scenarios', 'default'))
    scenario = Farm.Scenario(os.path.join(dataDir, 'common'), os.path.join(dataDir, 'scenarios', args.scenario), defaultScenario)

    if args.report and len(args.report) > 0 and (args.report_json or args.report_html):
        report = Farm.GenerateReport(scenario)
        if args.report_json:
            Farm.GenerateReportJson(report, args.report + '.json')
        if args.report_html:
            Farm.GenerateReportHtml(report, args.report + '.html', args.scenario)

    Farm.ProjectProfit(scenario)
