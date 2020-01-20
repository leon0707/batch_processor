import unittest

# import test modules
import test_task
import test_worker
import test_batch_processor

def suite():
        # initialize the test suite
    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()

        # add tests to the test suite
    suite.addTests(loader.loadTestsFromModule(test_task))
    suite.addTests(loader.loadTestsFromModule(test_worker))
    suite.addTests(loader.loadTestsFromModule(test_batch_processor))
    return suite

if __name__ == '__main__':
        # initialize a runner
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite())