import os

from setuptools import setup, find_packages

NAME = "trading-bots"
DESCRIPTION = "Trading bots for automation tasks in trading (place pending orders and manage risk) "
AUTHOR = "GeorgeQuantAnalyst"
URL = ""
VERSION = None

about = {}

with open(
        os.path.join(os.path.dirname(__file__), "requirements.txt"), "r"
) as fh:
    requirements = fh.readlines()

root = os.path.abspath(os.path.dirname(__file__))

if not VERSION:
    with open(os.path.join(root, "trading_bots", "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

setup(
    name=NAME,
    version=about["__version__"],
    license="BSD 2",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    AUTHOR=AUTHOR,
    url=URL,
    keywords=["Algo-trading", "Bybit"],
    install_requires=[req for req in requirements],
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3.11"
    ],
    python_requires=">=3.11",
)