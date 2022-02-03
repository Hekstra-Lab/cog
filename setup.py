from setuptools import setup, find_packages

# Testing requirements
tests_require = ["pytest", "pytest-xdist"]

setup(
    name="cog",
    version="0.4.3",
    author="Jack B. Greisman",
    author_email="greisman@g.harvard.edu",
    packages=find_packages(),
    description="Wrapper for Precognition to simplify Laue data reduction",
    install_requires=[
        "ipython",
        "numpy",
        "pandas",
        "matplotlib",
    ],
    setup_requires=["pytest-runner"],
    tests_require=tests_require,
    entry_points={
        "console_scripts": [
            "cog.up=cog.up:main",
            "cog.facet=cog.facet:main",
            "cog.load=cog.load:main",
        ]
    },
)
