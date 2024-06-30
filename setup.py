"""
    setup file
"""
from setuptools import setup, find_packages

with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='trading_api',
    version='0.0.1',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'trading_api = trading_api.__main__:__main__',
        ],
    },
    author='Jorge Ribeiro',
    author_email='mateusribeirojorge@gmail.com',
    description='Forex trading platform API',
)
