"""
simpledaemonlog: Set up simple logging for a daemon.
This is basically a preferred configuration for logging with python in some
situations and has been made available for easy reuse with different daemons.
"""

from setuptools import setup, find_packages

import simpledaemonlog

doclines = __doc__.split("\n")

setup(name='simpledaemonlog',
      version=simpledaemonlog.version,
      description='Set up simple logging for a python daemon.',
      long_description='\n'.join(doclines[2:]),
      url='http://github.com/proactivity-lab/python-simpledaemonlog',
      author='Raido Pahtma',
      author_email='raido.pahtma@ttu.ee',
      license='MIT',
      platforms=["any"],
      install_requires=["pyyaml", "colorlog"],
      packages=find_packages(),
      zip_safe=False)
