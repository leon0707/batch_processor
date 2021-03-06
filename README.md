# batch_processor

[![CircleCI](https://circleci.com/gh/leon0707/batch_processor.svg?style=svg)](https://circleci.com/gh/leon0707/batch_processor)
[![codecov](https://codecov.io/gh/leon0707/batch_processor/branch/master/graph/badge.svg)](https://codecov.io/gh/leon0707/batch_processor)

## install
```shell
pip install batch_processor
```

## quickstart
```python
from threading import Thread
from batch_processor import BatchProcessor

def batch_func(batch):
    return [v + v for v in batch]

def create_bulk_request(n, processor):
    print(n, processor.process(n))

processor = BatchProcessor(batch_func, worker_num=2, batch_size=32)

threads = []
for i in range(200):
    t = Thread(target=create_bulk_request, args=(i, self.processor))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
```

This piece of code generates discrete 200 incomming requests that can be processed in batches whose size is 32. There are 2 workers processing these requests. They take batches and double each integers in the batch, then return results in batches.

## test
* run test cases
  ```shell
  python tests/test_runner.py
  ```
* generate coverage
  ```shell
  coverage run tests/test_runner.py
  ```
* generate coverage html
  ```shell
  coverage html
  ```

## build
build the distribution
```shell
python setup.py sdist bdist_wheel
```
upload to registry
```shell
python -m twine upload dist/*
```