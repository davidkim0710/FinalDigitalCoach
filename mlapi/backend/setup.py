from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [
        line
        for line in f.read().splitlines()
        if not line.strip().startswith("--") and not " --" in line
    ]
setup(
    name="backend",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
)
