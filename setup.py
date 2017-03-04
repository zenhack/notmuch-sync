from setuptools import setup

setup(name='notmuch-sync',
      setup_requires=['setuptools_scm'],
      use_scm_version=True,
      py_modules=['notmuch_sync'],
      test_suite='tests',
      entry_points={
          'console_scripts': [
              'notmuch-sync=notmuch_sync:main',
          ],
      })
