from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open('README.md') as f:
    long_description = f.read()

setup(
    name="BPTACore",
    version="0.0.1",
    author="Jason Duncan",
    author_email="jason.matthew.duncan@gmail.com",
    description="Business Process Testing Automation - Core Module",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/jduncan8142/BPTA",
    project_urls={
        "Bug Tracker": "https://github.com/jduncan8142/BPTA/issues",
        "Documentation": "https://github.com/jduncan8142/BPTA/wiki"
    },
    packages=find_packages(where="BPTA"),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={},
    python_requires=">=3.11",
    install_requires=["sqlalchemy"], 
    extras_require={"dev": []}
)