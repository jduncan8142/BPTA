from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open('README.md') as f:
    long_description = f.read()

setup(
    name="BPTA",
    version="0.0.1",
    author="Jason Duncan",
    author_email="jason.matthew.duncan@gmail.com",
    description="Business Process Testing Automation",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/jduncan8142/BPTA.git",
    project_urls={
        "Bug Tracker": "https://github.com/jduncan8142/BPTA/issues",
        "Documentation": "https://github.com/jduncan8142/BPTA/wiki"
    },
    packages=find_packages(where="BPTA"),
    classifiers=(
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE",
    ),
    package_dir={"": "BPTA"},
    python_requires=">=3.10",
    install_requires=[]
)