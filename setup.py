"""Setup for OTE-API."""
from pathlib import Path

from setuptools import find_packages, setup

TOP_DIR = Path(__file__).resolve().parent

BASE = [
    f"{_.strip()}"
    for _ in (TOP_DIR / "requirements.txt").read_text(encoding="utf8").splitlines()
    if not _.startswith("#") and "git+" not in _
]

setup(
    name="oteapi-core",
    version="0.0.1",
    author="TEAM 4.0 devs",
    author_email="team4.0@SINTEF.onmicrosoft.com",
    url="https://github.com/EMMC-ASBL/oteapi-core",
    description="OTE-API (Open Translation Environment) API.",
    long_description=(TOP_DIR / "README.md").read_text(encoding="utf8"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=BASE,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
)
