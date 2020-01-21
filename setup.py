# encoding: utf-8
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='batch_processor',
      version='0.0.3',
      description='This library is used to enable batch processing by implementing python multiprocessing',
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Operating System :: OS Independent',
      ],      
      keywords='batch, multiprocessing, performance',
      url='https://github.com/leon0707/batch_processor',
      packages=find_packages(exclude=['tests']),
      install_requires=[],
      include_package_data=True,
      python_requires='>=3.5',
      zip_safe=False
)