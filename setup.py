from setuptools import setup, find_packages

setup(
    name='cog',
    version='0.3.1',
    author='Jack B. Greisman',
    author_email='greisman@g.harvard.edu',
    packages=find_packages(),
    description='Wrapper for Precognition to simplify Laue data reduction',
    install_requires=[
        "pandas",
        "matplotlib",
    ],
    entry_points={
        'console_scripts': [
            'cog=cog.main:main',
            'cog.up=cog.up:main',
            'cog.facet=cog.facet:main',            
        ]
    }
)
