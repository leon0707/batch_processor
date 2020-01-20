import unittest

from batch_processor import Task

class TestTask(unittest.TestCase):

    def setUp(self):
        self.task = Task(0)

    def test_set_get_result(self):
        with self.assertRaises(TimeoutError):
            self.task.get_result(1)

        self.task.set_result('result')
        self.assertEqual(self.task.get_result(1), 'result')


if __name__ == '__main__':
    unittest.main()

