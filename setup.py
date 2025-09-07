from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smart-test",
    version="0.1.0",
    author="Prady",
    author_email="pradyumnprasad.567@gmail.com",
    description="A tool for analyzing and generating tests for Python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pradyumn-cloud/VERITA",
    packages=find_packages(exclude=["tests", "examples", "*.tests", "*.examples"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0.0",
        "pytest>=6.0.0",
        "pyyaml>=5.1",
        "toml>=0.10.2",
    ],
    entry_points={
        "console_scripts": [
            "smart-test=smart_test.main:main",
        ],
    },
    # Reduce test file discovery during installation
    zip_safe=False,
    include_package_data=False,
)