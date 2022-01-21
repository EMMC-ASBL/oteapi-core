"""Setup for OTE-API."""
import re
from pathlib import Path

from setuptools import find_packages, setup

TOP_DIR = Path(__file__).resolve().parent
PACKAGE_NAME = "oteapi-core"

with open(
    TOP_DIR / PACKAGE_NAME.split("-", maxsplit=1)[0] / "__init__.py",
    "r",
    encoding="utf8",
) as handle:
    VERSION = AUTHOR = AUTHOR_EMAIL = None
    for line in handle.readlines():
        VERSION_match = re.match(r'__version__ = (\'|")(?P<version>.+)(\'|")', line)
        AUTHOR_match = re.match(r'__author__ = (\'|")(?P<author>.+)(\'|")', line)
        AUTHOR_EMAIL_match = re.match(
            r'__author_email__ = (\'|")(?P<email>.+)(\'|")', line
        )

        if VERSION_match is not None:
            VERSION = VERSION_match
        if AUTHOR_match is not None:
            AUTHOR = AUTHOR_match
        if AUTHOR_EMAIL_match is not None:
            AUTHOR_EMAIL = AUTHOR_EMAIL_match

    for info, value in {
        "version": VERSION,
        "author": AUTHOR,
        "author email": AUTHOR_EMAIL,
    }.items():
        if value is None:
            raise RuntimeError(
                f"Could not determine {info} from "
                f"{TOP_DIR / PACKAGE_NAME.split('-', maxsplit=1)[0] / '__init__.py'} !"
            )
    VERSION = VERSION.group("version")  # type: ignore[union-attr]
    AUTHOR = AUTHOR.group("author")  # type: ignore[union-attr]
    AUTHOR_EMAIL = AUTHOR_EMAIL.group("email")  # type: ignore[union-attr]

BASE = [
    f"{_.strip()}"
    for _ in (TOP_DIR / "requirements.txt").read_text(encoding="utf8").splitlines()
    if not _.startswith("#") and "git+" not in _
]

DOCS = [
    f"{_.strip()}"
    for _ in (TOP_DIR / "requirements_docs.txt").read_text(encoding="utf8").splitlines()
    if not _.startswith("#") and "git+" not in _
]

DEV = [
    f"{_.strip()}"
    for _ in (TOP_DIR / "requirements_dev.txt").read_text(encoding="utf8").splitlines()
    if not _.startswith("#") and "git+" not in _
] + DOCS

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url="https://github.com/EMMC-ASBL/oteapi-core",
    description="Open Translation Environment (OTE) API.",
    long_description=(TOP_DIR / "README.md").read_text(encoding="utf8"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=BASE,
    extras_require={"dev": DEV, "docs": DOCS},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
)
