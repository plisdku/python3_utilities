from setuptools import setup

install_requires = ["numpy"]
version = "0.1.0"

setup(name="sugar",
    version=version,
    description="Paul's Python 3 utilities",
    author="Paul Hansen",
    author_email="paul.c.hansen@gmail.com",
    packages=["plisdku"],
    install_requires= install_requires,
    python_requires=">=3",
    zip_safe=False)