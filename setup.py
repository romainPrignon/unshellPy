from setuptools import setup, find_packages

setup(
    name="Unshell",
    version="0.1",
    python_requires=">=3.7",
    packages=find_packages(),
    scripts=['src/cli.py'],

    author="Romain Prignon",
    author_email="pro.rprignon@gmail.com",
    description="Set your shell free",
    keywords="shell subprocess scripting",
    url="https://github.com/romainPrignon/unshellPy",
    project_urls={
        "Bug Tracker": "https://github.com/romainPrignon/unshellPy/issue",
        "Source Code": "https://github.com/romainPrignon/unshellPy",
    },
    license="MIT"
)
