import unittest
import multiprocessing
from threading import Thread

from batch_processor import BatchProcessor


class TestBatchProcessor(unittest.TestCase):

    def batch_func(self, batch):
        return [v + v for v in batch]

    def setUp(self):
        # multiprocessing.set_start_method('spawn') # spawn doesn't work here https://bugs.python.org/issue33884
        self.processor_1 = BatchProcessor(self.batch_func, worker_num=2)
        self.processor_2 = BatchProcessor(self.batch_func, worker_num=2, task_wait_time=0.001)

    def test_process(self):
        self.assertEqual(self.processor_1.process(5), 10)
        # processor 2 has the min waiting time, should generate an exception and return None
        self.assertEqual(self.processor_2.process(5), None)

    def test_batch(self):
        def create_bulk_request(n, processor):
            self.assertEqual(processor.process(n), n + n)

        threads = []
        for i in range(200):
            t = Thread(target=create_bulk_request, args=(i, self.processor_1))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    def tearDown(self):
        self.processor_1.terminate()
        self.processor_2.terminate()

if __name__ == '__main__':
    unittest.main()