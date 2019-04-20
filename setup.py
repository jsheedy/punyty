from setuptools import setup, find_packages

setup(
    name='punyty',
    version='0.0.0',
    description='Punyty rendering engine',
    author='Joseph Sheedy',
    author_email='joseph.sheedy@gmail.com',
    url='https://github.com/jsheedy/punyty',
    install_requires=['numpy'],
    extras_require={
        'SDL': ['PySDL2'],
    },
    packages=find_packages()
)