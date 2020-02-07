import os
import csv
from datetime import datetime

performanceLogFileName = 'performance'

def createFileName():
    return datetime.today().strftime('%Y-%m-%d')

def createLogDirectoryPath():
    fileDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(fileDir)
    return os.path.join(parentDir, 'logs')


logDirectory = createLogDirectoryPath()


def logFunction(fn):
    def writeFnInfo(*args, **kwargs):
        logFileName = createFileName()
        with open('{}/{}'.format(logDirectory, logFileName), 'a+') as logFile:
            tsvWriter = csv.writer(logFile, delimiter='\t')
            start = datetime.now()
            fnResult = fn(*args, **kwargs)
            end = datetime.now()
            duration = end - start
            tsvWriter.writerow([start, fn.__name__, duration.total_seconds() * 1000])
            return fnResult
    return writeFnInfo

def formatPath(fileName):
    return '{}/{}'.format(logDirectory, fileName)

def processPerformanceLog(logPath, actionEntries = {}):
    with open(logPath, newline='') as log:
        log = csv.reader(log, delimiter='\t')

        for row in log:
            action = row[1]
            duration = float(row[2])
            print(actionEntries)
            if action not in actionEntries:
                actionEntries[action] = {'totalDuration': duration, 'count': 1}
            else:
                actionEntry = actionEntries.get(action)
                actionEntry['totalDuration'] += duration
                actionEntry['count'] +=1

def analyzePerformance():
    actionEntries = {}
    with os.scandir(logDirectory) as logDir:
        for path in logDir:
            if path.is_file() and performanceLogFileName not in path.name:
                processPerformanceLog(path, actionEntries)

    for action in actionEntries:
        entry = actionEntries.get(action)
        avg = entry['totalDuration']/entry['count']
        print('Function {} was called {} times, and the average execution duration was {}ms'.format(action, entry['count'], avg))

