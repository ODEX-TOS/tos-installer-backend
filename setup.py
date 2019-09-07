from setuptools import setup

setup(
   name='installer-backend',
   version='0.5.0',
   description='Install POSIX compliant Operating systems using a yaml file',
   author='Meyers Tom',
   author_email='tom@odex.be',
   packages=['installer.model', 'installer.parser', 'installer'],  #same as name
   install_requires=['yaml'], #external packages as dependencies
)
