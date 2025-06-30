# This Python file uses the following encoding: utf-8

import os
import json
import functools
import re


def mergeDict(a: dict, b: dict, dictionaryPath = []):
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                mergeDict(a[key], b[key], dictionaryPath + [ str(key) ])
            elif isinstance(a[key], list) and isinstance(b[key], list):
                # Concatenate arrays with the same key
                a[key] += b[key]
            elif a[key] != b[key]:
                print("Scenario overrides {} from {} to {}".format('.'.join(dictionaryPath + [ str(key) ]), a[key], b[key]))
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


def mergeDictionaries(dictionariesList):
    if len(dictionariesList) == 0:
        return {}
    elif len(dictionariesList) == 1:
        return dictionariesList[0]
    dest = dict(dictionariesList[0])
    functools.reduce(mergeDict, [ dest ] + dictionariesList[1:])
    return dest


def prettyPrintDict(d, indent=0):
    print('{}{}'.format(' '*indent, '{'))
    indent += 4
    for key, value in d.items():
        if isinstance(value, dict):
            print('{}"{}":'.format(' '*indent, key))
            prettyPrintDict(value, indent)
        elif isinstance(value, str):
            print('{}"{}": "{}",'.format(' '*indent, key, value))
        else:
            print('{}"{}": {},'.format(' '*indent, key, value))
    print('{}{},'.format(' '*(indent - 4), '}'))


class Scenario:
    # Overrides are a list of lists, like thus: [ [ 'path/to/some input', value ], [ 'path/to another', value ], ... ]
    def __init__(self, commonDir, scenarioDir, maxAcres, defaultScenario=None, overrides=[]):
        self.defaultScenario = defaultScenario
        self.maxAcres = maxAcres
        self.desiredAcres = 0.0
        self.json = {}
        for file in os.listdir(commonDir):
            filename = os.path.join(commonDir, os.fsdecode(file))
            if not filename.endswith('.json'):
                continue
            print("Reading common JSON: {}".format(filename))
            with open(filename, 'r') as jsonFile:
                entryName = os.path.splitext(os.path.basename(filename))[0]
                self.json[entryName] = json.load(jsonFile)
        for file in os.listdir(scenarioDir):
            filename = os.path.join(scenarioDir, os.fsdecode(file))
            if not filename.endswith('.json'):
                continue
            print("Reading scenario JSON: {}".format(filename))
            with open(filename, 'r') as jsonFile:
                entryName = os.path.splitext(os.path.basename(filename))[0]
                if entryName in self.json:
                    mergeDict(self.json[entryName], json.load(jsonFile))
                else:
                    self.json[entryName] = json.load(jsonFile)
        # Apply overrides
        if overrides is not None:
            for override in overrides:
                try:
                    value = float(override[1])
                    self.set(override[0], value)
                except:
                    self.set(override[0], override[1])

    def hasAcreLimit(self):
        return self.maxAcres > 0.0

    def getMaxAcres(self):
        return self.maxAcres

    def getDesiredAcres(self):
        return self.desiredAcres

    def setDesiredAcres(self, acres):
        self.desiredAcres = acres

    def getSub(self, pathArray, d, originalPath):
        if len(pathArray) == 0:
            print("WARNING: Empty path array found when processing path: {}".format(originalPath))
            return None
        pathElem = pathArray[0]
        results = []
        if '*' in pathElem:
            matchStr = '^' + pathElem.replace('*', '.*')
            matcher = re.compile(matchStr)
            for key, value in d.items():
                if not matcher.match(key):
                    continue
                if len(pathArray) == 1:
                    results += [ value ]
                elif isinstance(value, dict):
                    results += self.getSub(pathArray[1:], value, originalPath)
                else:
                    print("WARNING: Non-dict {} found in incomplete path: {}".format(key, originalPath))
        elif len(pathArray) == 1:
            if pathElem in d:
                results += [ d[pathElem] ]
            else:
                print("WARNING: Path element {} not found in {}".format(pathElem, originalPath))
        else:
            if pathElem in d:
                nextElem = d[pathElem]
                if isinstance(nextElem, dict):
                    results += self.getSub(pathArray[1:], nextElem, originalPath)
                else:
                    print("WARNING: Path element {} is not a dictionary in {}".format(pathElement, originalPath))
            else:
                print("WARNING: Path element {} not found in {}".format(pathElem, originalPath))
        return results

    def get(self, path, defaultValue=None):
        pathArray = path.split('/')
        results = self.getSub(pathArray, self.json, path)
        if not results:
            if defaultValue:
                return defaultValue
            elif self.defaultScenario:
                return self.defaultScenario.get(path, defaultValue)
            else:
                return None
        if '*' in path or len(results) > 1:
            return results
        return results[0]

    def setSub(self, pathArray, d, originalPath, newValue):
        if len(pathArray) == 0:
            print("WARNING: When setting a value, empty path array found in path: {}".format(originalPath))
            return False
        valueGotSet = False
        pathElem = pathArray[0]
        if '*' in pathElem:
            matchStr = '^' + pathElem.replace('*', '.*')
            matcher = re.compile(matchStr)
            for key, value in d.items():
                if not matcher.match(key):
                    continue
                if len(pathArray) == 1:
                    print("Override applied: '{}' at key '{}' to value: {}".format(originalPath, key, newValue))
                    d[key] = newValue
                    valueGotSet = True
                elif isinstance(value, dict):
                    if self.setSub(pathArray[1:], value, originalPath, newValue):
                        valueGotSet = True
                else:
                    print("WARNING: When setting a value, non-dict {} found in incomplete path: {}".format(key, originalPath))
        elif len(pathArray) == 1:
            if pathElem in d:
                print("Value applied: '{}' to value: {}".format(originalPath, newValue))
                d[pathElem] = newValue
                valueGotSet = True
            else:
                print("WARNING: When setting a value, path element {} not found in {}".format(pathElem, originalPath))
        else:
            if pathElem in d:
                nextElem = d[pathElem]
                if isinstance(nextElem, dict):
                    if self.setSub(pathArray[1:], nextElem, originalPath, newValue):
                        valueGotSet = True
                else:
                    print("WARNING: When setting a value, path element {} is not a dictionary in {}".format(pathElement, originalPath))
            else:
                print("WARNING: When setting a value, path element {} not found in {}".format(pathElem, originalPath))
        return valueGotSet

    def set(self, path, newValue):
        pathArray = path.split('/')
        return self.setSub(pathArray, self.json, path, newValue)

    def dump(self):
        prettyPrintDict(self.json)
