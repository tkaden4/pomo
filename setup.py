from setuptools import setup, find_packages


setup(
    name="pomo",
    version="0.1.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["pomo = pomo.__main__:cli"]},
    install_requires=[line for line in open("./requirements.txt")],
)
