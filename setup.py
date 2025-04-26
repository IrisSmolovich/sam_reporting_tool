
from setuptools import setup, find_packages


def parse_requirements(filename):
    """
    :param filename:
    :return:
    """
    with open(filename, "r") as f:
        return [
            line.strip()  # Remove extra spaces and line breaks
            for line in f.readlines()
            if line.strip() and not line.startswith("#")  # Skip empty lines and comments
        ]


setup(
    name="reputation-cli",
    version="1.0",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "reptest=reputation_tool.main:main",
        ],
    },
)
