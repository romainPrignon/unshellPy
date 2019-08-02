from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Unshell",
    version="0.1.2",
    python_requires=">=3.7",
    packages=find_packages(exclude=["spec"]),
    entry_points={
        "console_scripts": ['unshell = src.cli:main']
    },

    author="Romain Prignon",
    author_email="pro.rprignon@gmail.com",
    description="Set your shell free !",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="shell subprocess scripting",
    url="https://github.com/romainPrignon/unshellPy",
    project_urls={
        "Bug Tracker": "https://github.com/romainPrignon/unshellPy/issue",
        "Source Code": "https://github.com/romainPrignon/unshellPy",
    },
    license="MIT"
)
