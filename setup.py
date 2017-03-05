from setuptools import setup, find_packages

setup(name='notmuch-sync',
      setup_requires=['setuptools_scm'],
      use_scm_version=True,
      packages=find_packages(),
      test_suite='tests',
      entry_points={
          'console_scripts': [
              'notmuch-sync=notmuch_sync:main',
          ],
      })
