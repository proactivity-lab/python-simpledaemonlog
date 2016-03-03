"""
simpledaemonlog: Set up simple logging for a daemon.
This is basically a preferred configuration for logging with python in some
situations and has been made available for easy reuse with different daemons.
"""

from setuptools import setup

doclines = __doc__.split("\n")

setup(name='simpledaemonlog',
      version='0.1.0',
      description='Set up simple logging for a python daemon.',
      long_description='\n'.join(doclines[2:]),
      url='http://github.com/proactivity-lab/python-simpledaemonlog',
      author='Raido Pahtma',
      author_email='raido.pahtma@ttu.ee',
      license='MIT',
      platforms = ["any"],
      install_requires=["pyyaml", "argconfparse"],
      packages=['simpledaemonlog'],
      zip_safe=False)
