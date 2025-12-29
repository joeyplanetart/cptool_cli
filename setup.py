from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cptools",
    version="1.1.0",
    author="Joey Zhou",
    author_email="Joeyz@planetart.com",
    description="命令行工具集，包含截屏、URL检测等功能",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joeyplanetart/cptool_cli",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "playwright>=1.40.0",
        "click>=8.1.0",
        "aiohttp>=3.9.0",
        "pandas>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "cptools=cptools.cli:cli",
        ],
    },
)

