import unittest
import multiprocessing
from threading import Thread

from batch_processor import BatchProcessor


class TestBatchProcessor(unittest.TestCase):

    def batch_func(self, batch):
        return [v + v for v in batch]

    def setUp(self):
        # multiprocessing.set_start_method('spawn') # spawn doesn't work here https://bugs.python.org/issue33884
        self.processor = BatchProcessor(self.batch_func, worker_num=2)


    def test_process(self):
        self.assertEqual(self.processor.process(5), 10)

    def test_batch(self):
        def create_bulk_request(n, processor):
            self.assertEqual(processor.process(n), n + n)

        threads = []
        for i in range(200):
            t = Thread(target=create_bulk_request, args=(i, self.processor))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()


if __name__ == '__main__':
    unittest.main()