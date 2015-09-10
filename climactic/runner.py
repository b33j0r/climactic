#! /usr/bin/env python
"""
``climactic.runner``
--------------------

.. autoclass:: ClimacticTestResult

.. autoclass:: ClimacticTestRunner
"""
import unittest
import logging

from climactic.suite import ClimacticTestSuite


logger = logging.getLogger(__name__)


class ClimacticTestResult(unittest.TextTestResult):
    """

    """

    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)

    def startTest(self, test):
        super(ClimacticTestResult, self).startTest(test)
        if logger.parent.level < logging.INFO:
            # the superclass writes "
            self.stream.write("\n")
            self.stream.flush()


class ClimacticTestRunner(unittest.TextTestRunner):
    """

    """

    resultclass = ClimacticTestResult

    @classmethod
    def run_for_targets(cls, *targets, recursive=True, **kwargs):
        runner = cls(**kwargs)
        suite = ClimacticTestSuite.from_targets(
            *targets, recursive=recursive
        )
        result = runner.run(suite)
        return result

    @classmethod
    def run_in_dir(cls, dir_path, recursive=True, **kwargs):
        runner = cls(**kwargs)
        suite = ClimacticTestSuite.from_dir(
            dir_path, recursive=recursive
        )
        result = runner.run(suite)
        return result

    def run(self, test):
        """
        Run the given test case or test suite.
        """
        import warnings
        import time
        from unittest.signals import registerResult

        result = self._makeResult()
        registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        with warnings.catch_warnings():
            if self.warnings:
                # if self.warnings is set, use it to filter all the warnings
                warnings.simplefilter(self.warnings)
                # if the filter is 'default' or 'always', special-case the
                # warnings from the deprecated unittest methods to show them
                # no more than once per module, because they can be fairly
                # noisy.  The -Wd and -Wa flags can be used to bypass this
                # only when self.warnings is None.
                if self.warnings in ['default', 'always']:
                    warnings.filterwarnings(
                        'module',
                        category=DeprecationWarning,
                        message='Please use assert\w+ instead.'
                    )
            startTime = time.time()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()
            try:
                test(result)
            finally:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()
            stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printErrors()
        if hasattr(result, 'separator2'):
            logger.info(result.separator2)
        run = result.testsRun
        logger.info(
            "Ran %d test%s in %.3fs" %
            (run, run != 1 and "s" or "", timeTaken)
        )

        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped))
        except AttributeError:
            pass
        else:
            expectedFails, unexpectedSuccesses, skipped = results

        infos = []
        if not result.wasSuccessful():
            logger.info("FAILED")
            failed, errored = len(result.failures), len(result.errors)
            if failed:
                infos.append("failures=%d" % failed)
            if errored:
                infos.append("errors=%d" % errored)
        else:
            logger.info("OK")
        if skipped:
            infos.append("skipped=%d" % skipped)
        if expectedFails:
            infos.append("expected failures=%d" % expectedFails)
        if unexpectedSuccesses:
            infos.append("unexpected successes=%d" % unexpectedSuccesses)
        if infos:
            logger.info(" (%s)" % (", ".join(infos),))
        else:
            logger.info("\n")
        return result
