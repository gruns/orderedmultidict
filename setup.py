import os
import sys

from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
  os.system('python setup.py sdist upload')
  sys.exit()

long_description = ('''omdict: Ordered Multivalue Dictionary.

A multivalue dictionary is a dictionary that can store multiple values for the
same key. An ordered multivalue dictionary is a multivalue dictionary that
retains the order of insertions and deletions.

omdict retains method parity with dict.

Information and documentation at: https://github.com/gruns/orderedmultidict''')

required = []
if sys.version_info[:2] <= (2,6):
  required.append('ordereddict')

setup(name='orderedmultidict',
      version='0.6',
      author='Arthur Grunseid',
      author_email='grunseid@gmail.com',
      url='https://github.com/gruns/orderedmultidict',
      packages=find_packages(),
      license='Unlicense',
      include_package_data=True,
      description='OrderedMultiDict: Ordered Multivalue Dictionary',
      long_description=long_description,
      platforms=['any'],
      classifiers=['Topic :: Software Development :: Libraries',
                   'Natural Language :: English',
                   'Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: Freely Distributable',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   ],
      install_requires=required,
      test_suite='tests',
      tests_require=[],
      )
