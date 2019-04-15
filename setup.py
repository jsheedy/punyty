from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='punyty',
    version='0.0.0',
    description='Punyty rendering engine',
    author='Joseph Sheedy',
    author_email='joseph.sheedy@gmail.com',
    url='https://github.com/jsheedy/punyty',
    install_requires=requirements,
    packages=find_packages()
)