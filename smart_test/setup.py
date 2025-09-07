from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smart_test",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for analyzing and generating tests for Python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/smart-test",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
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
)