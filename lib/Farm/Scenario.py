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
            elif a[key] != b[key]:
                raise Exception('Dictionary merge conflict at ' + '.'.join(dictionaryPath + [ str(key) ]))
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
    def __init__(self, commonDir, scenarioDir):
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

    def getSub(self, pathArray, d, originalPath):
        if len(pathArray) == 0:
            print("Empty path array found when processing path: {}".format(originalPath))
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
                    print("non-dict {} found in incomplete path: {}".format(key, originalPath))
        elif len(pathArray) == 1:
            if pathElem in d:
                results += [ d[pathElem] ]
            else:
                print("Path element {} not found in {}".format(pathElem, originalPath))
        else:
            if pathElem in d:
                nextElem = d[pathElem]
                if isinstance(nextElem, dict):
                    results += self.getSub(pathArray[1:], nextElem, originalPath)
                else:
                    print("Path element {} is not a dictionary in {}".format(pathElement, originalPath))
            else:
                print("Path element {} not found in {}".format(pathElem, originalPath))
        return results

    def get(self, path, d=None):
        pathArray = path.split('/')
        results = self.getSub(pathArray, self.json, path)
        if not results:
            return None
        if '*' in path or len(results) > 1:
            return results
        return results[0]

    def dump(self):
        prettyPrintDict(self.json)
