import unittest
from aspect.logging import logFunction, logDirectory, createFileName, analyzePerformance

class Test_Logging_Works(unittest.TestCase):

    def test_log_appended(self):
        def testFn():
            print('test function was called')
        fn = logFunction(testFn)
        with open('{}/{}'.format(logDirectory, createFileName()), 'r+') as logFile:
            firstCount = sum(1 for line in logFile)

        fn()
        with open('{}/{}'.format(logDirectory, createFileName()), 'r+') as logFile:
            secondCount = sum(1 for line in logFile)

        self.assertEqual(secondCount, (firstCount+1))

    def test_performance_analysis_works(self):
        try:
            analyzePerformance()
        except Exception:
            self.fail('analyzePerformance() raised an error unexpectedly!')


if __name__ == '__main__':
    unittest.main()
