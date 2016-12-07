import os
from setuptools import setup, find_packages

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(WORKING_DIR, 'requirements.txt')) as reqs:
  REQUIREMENTS = [ req for req in reqs ]

setup(
    name='pyimpact',
    version='0.1.0',
    py_modules=['pyimpact'],
    package_dir={'pyimpact': 'src'},
    install_requires=REQUIREMENTS,
)


