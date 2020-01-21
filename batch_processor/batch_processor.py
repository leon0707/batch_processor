#
# Module implementing batch process
#
# Author Leon Feng

__all__ = ['Task', 'Worker', 'BatchProcessor']


import multiprocessing as mp
from os import getpid
from queue import Empty
from threading import Event, Thread
from time import sleep

class Task(object):
    def __init__(self, id):
        self._id = id
        self._finish_event = Event()
        self.__result = None

    def set_result(self, res):
        self.__result = res
        self._finish_event.set()

    def get_result(self, timeout=None):
        finished = self._finish_event.wait(timeout)
        if not finished:
            # if task is not finished within time period
            raise TimeoutError("Task: %d Timeout" % self._id)
        # return result
        return self.__result


class _TaskCache(dict):
    'Dict for weakref only'
    pass


class Worker(object):
    def __init__(self, input_queue, output_queue, batch_size, batch_func, sleep_time=0.01):
        self._input_queue = input_queue
        self._output_queue = output_queue
        self._batch_size = batch_size
        self.batch_func = batch_func
        self._sleep_time = sleep_time
        self.__pause = mp.Value('i', False, lock=True)
        self.__stop_evt = Event()

    def loop_run(self):
        self._worker_id = getpid()
        print('worker {} starts working'.format(self._worker_id))
        counter = 0
        batch = []
        while True:
            if self.__stop_evt.is_set():
                break
            if self.is_paused():
                continue    
            batch = self.__fill_batch()
            if batch:
                inputs = [req for task_id, req in batch] # batch func doesn't need task_id
                results = self.batch_func(inputs)
                for i in range(len(batch)):
                    # match result with task_id
                    self.__process_result(batch[i][0], results[i])
                print('worker {} processes {}'.format(self._worker_id, len(results)))
            else:
                sleep(self._sleep_time)

    def __fill_batch(self):
        batch = []
        for i in range(self._batch_size):
            try:
                task_tuple = self._input_queue.get(block=False)
                batch.append(task_tuple)
            except Empty as e:
                break
        return batch

    def __process_result(self, task_id, result):
        '''Add result into the output queue'''
        self._output_queue.put((task_id, result))


    def pause(self):
        with self.__pause.get_lock():
            self.__pause.value = True

    def is_paused(self):
        return self.__pause.value

    def restart(self):
        with self.__pause.get_lock():
            self.__pause.value = False

    def destory(self):
        print('destory the worker {}'.format(self._worker_id))
        # set the stop event
        self.__stop_evt.set()

class BatchProcessor(object):

    def __init__(self, batch_func, worker_num=1, batch_size=32, task_wait_time=4):
        self._current_task_id_obj = mp.Value('i', 0, lock=True)
        self._input_queue = mp.Queue() # queue can be full and raise exception
        self._output_queue = mp.Queue()
        self._task_wait_time = task_wait_time

        self._cache_ref = _TaskCache() # a dict to save result of task

        self._result_collector = Thread(target=self.__loop_collect_result, daemon=True)
        self.__stop_collector_evt = Event()
        self._result_collector.start()

        self._worker = Worker(self._input_queue, self._output_queue, batch_size, batch_func)
        self._worker_ps = []
        for i in range(worker_num):
            self._worker_ps.append(mp.Process(target=self._worker.loop_run, name='batch_worker', daemon=True))
            self._worker_ps[-1].start()

    def __loop_collect_result(self):
        # infinite loop to collect result from output queue
        while True:
            if self.__stop_collector_evt.is_set():
                break
            try:
                task_id, res = self._output_queue.get(block=False)
                # if the task is not timeout
                task = self._cache_ref.get(task_id)
                if task:
                    task.set_result(res)
            except Empty as e:
                pass # or sleep

    def __add_request(self, req):
        with self._current_task_id_obj.get_lock():
            task_id = self._current_task_id_obj.value
            self._current_task_id_obj.value += 1
        task = Task(task_id)
        self._cache_ref[task_id] = task
        self._input_queue.put((task_id, req))
        return task_id

    def __get_result(self, task_id):
        task = self._cache_ref[task_id]
        try:
            res = task.get_result(self._task_wait_time)
        except Exception as e:
            print('have an exception')
            res = None
        # delete task from cache
        self.__delete_task(task_id)
        return res

    def __delete_task(self, task_id):
        if task_id in self._cache_ref:
            del self._cache_ref[task_id]

    def process(self, input_val):
        task_id = self.__add_request(input_val)
        res = self.__get_result(task_id)
        return res

    def __destory_collector(self):
        self.__stop_collector_evt.set()

    def terminate(self):
        print('terminate the BatchProcessor')
        for p in self._worker_ps:
            p.terminate()

        self.__destory_collector()
        self._result_collector.join()
