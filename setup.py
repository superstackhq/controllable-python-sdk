from setuptools import setup, find_packages

setup(
    name='controllable',
    version='0.1.0',
    packages=find_packages(include=["controllable", "controllable.*"]),
    install_requires=[
        "requests"
    ]
)
