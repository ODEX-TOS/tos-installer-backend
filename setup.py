from setuptools import setup

setup(
   name='installer-backend',
   version='0.5.0',
   description='Install POSIX compliant Operating systems using a yaml file',
   author='Meyers Tom',
   author_email='tom@odex.be',
   packages=['installer', 'installer.model', 'installer.model.build', 'installer.model.gen', 'installer.model.model', 'installer.parser'],  #same as name
   install_requires=['PyYAML'], #external packages as dependencies
)
