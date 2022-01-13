"""Setup for OTE-API."""
from pathlib import Path
from typing import TYPE_CHECKING

import yaml
from setuptools import find_packages, setup

if TYPE_CHECKING:
    from typing import Dict, List

TOP_DIR = Path(__file__).resolve().parent

BASE = [
    f"{_.strip()}"
    for _ in (TOP_DIR / "requirements.txt").read_text(encoding="utf8").splitlines()
    if not _.startswith("#") and "git+" not in _
]

ENTRY_POINTS: "Dict[str, List[str]]" = yaml.safe_load(
    (TOP_DIR / "plugins.yml").read_text(encoding="utf8")
)

setup(
    name="oteapi",
    version="0.0.1",
    author="TEAM 4.0 devs",
    author_email="team40@SINTEF.onmicrosoft.com",
    url="https://github.com/EMMC-ASBL/oteapi",
    description="OTE-API (Open Translation Environment) API.",
    long_description=(TOP_DIR / "README.md").read_text(encoding="utf8"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=BASE,
    entry_points=ENTRY_POINTS,
)
