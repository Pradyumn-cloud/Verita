from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smart-test-generator",
    version="2.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-Powered Python Test File Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/smart-test-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
        "google-generativeai>=0.3.0",
        "python-dotenv>=0.19.0",
        "pytest>=6.0.0",
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.0.0',
            'black>=21.0',
            'flake8>=3.9.0',
        ],
    },
    entry_points={
        "console_scripts": [
            "smart-test=smart_test.cli:cli",  # CHANGED from main:main to cli:cli
        ],
    },
)