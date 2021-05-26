import sys
from setuptools import setup, find_packages

#install_requires = ["matplotlib", "hapiclient @ git+https://github.com/hapi-server/client-python#egg=hapiclient"]
install_requires = ["matplotlib", "hapiclient>0.1.7"]

if sys.argv[1] == 'develop':
    install_requires.append("deepdiff<3.3.0")
    if sys.version_info < (3, 6):
        install_requires.append("pytest<5.0.0")
    else:
        # Should not be needed, as per
        # https://docs.pytest.org/en/stable/py27-py34-deprecation.html
        # Perhaps old version of pip causes this?
        install_requires.append("pytest")

# version is modified by misc/version.py (executed from Makefile). Do not edit.
setup(
    name='hapiplot',
    version='0.0.1b3',
    author='Bob Weigel',
    author_email='rweigel@gmu.edu',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/hapiplot/',
    license='LICENSE.txt',
    description='Plot data from HAPI server',
    long_description=open('README.rst').read(),
    install_requires=install_requires
)