import unittest
import time
import multiprocessing as mp

from batch_processor import Worker
from util_queue import Queue

class TestWorker(unittest.TestCase):

    def batch_func(self, batch):
        # do nothing
        return batch

    def clean_queues(self):
        while not self.input_queue.empty():
            self.input_queue.get()

        while not self.output_queue.empty():
            self.output_queue.get()

    def setUp(self):
        self.input_queue = Queue() # queue can be full and raise exception
        self.output_queue = Queue()

        self.worker = Worker(self.input_queue, self.output_queue, 32, self.batch_func)

        # generate one process
        self.process = mp.Process(target=self.worker.loop_run, name='batch_worker')
        self.process.start()

    def test_pause_restart(self):
        self.worker.pause()
        # add one item in the input queue
        self.input_queue.put((0, 'test'))
        # pause 1 sec
        time.sleep(1)
        self.assertEqual(self.input_queue.qsize(), 1)
        self.assertEqual(self.output_queue.qsize(), 0)

        self.worker.restart()
        time.sleep(1)
        self.assertEqual(self.input_queue.qsize(), 0)
        self.assertEqual(self.output_queue.qsize(), 1)

        self.clean_queues()

    def test_loop_run(self):
        self.assertEqual(self.input_queue.qsize(), 0)
        self.assertEqual(self.output_queue.qsize(), 0)
        for i in range(35):
            self.input_queue.put((i, 'test'))
        time.sleep(1)
        self.assertEqual(self.input_queue.qsize(), 0)
        self.assertEqual(self.output_queue.qsize(), 35)


    def tearDown(self):
        self.process.terminate()

if __name__ == '__main__':
    unittest.main()