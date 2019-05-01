from setuptools import setup, find_packages

setup(
    name='punyty',
    version='0.0.0',
    description='Punyty rendering engine',
    author='Joseph Sheedy',
    author_email='joseph.sheedy@gmail.com',
    url='https://github.com/jsheedy/punyty',
    install_requires=['numpy', 'scikit-image'],
    extras_require={
        'SDL': ['PySDL2'],
    },
    entry_points = {
        'console_scripts': [
            'punytty = demo.punytty:punytty'
        ]
    },
    packages=find_packages(),
    package_data={'models': ['*']}
)