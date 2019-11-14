from setuptools import setup, find_packages

setup(
    name='cog',
    version='0.1.0',
    author='Jack B. Greisman',
    author_email='greisman@g.harvard.edu',
    packages=find_packages(),
    description='Wrapper for Precognition to simplify Laue data reduction',
    install_requires=[],
    scripts=['bin/cog.py']
)
