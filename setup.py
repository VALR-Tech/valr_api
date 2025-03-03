from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="valr-api",
    version="0.1.0",
    author="VALR API Python Client Contributors",
    author_email="",
    description="Python client for the VALR cryptocurrency exchange API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/valr-api",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/valr-api/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(include=["valr_api", "valr_api.*"]),
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.8",
)
