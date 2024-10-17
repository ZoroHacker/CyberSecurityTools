# setup.py
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="CyberSecurityTools",
    version="0.4",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "colorama",
        "pyfiglet",
        "sockets"
    ],
    description="CyberSecurityTool is a comprehensive Python package designed for performing essential cybersecurity scans. It includes features like subdomain enumeration, broken link checking, SQL injection testing, XSS detection, CSRF testing, and network vulnerability scanning. Built with ease of use and efficiency in mind, CyberSecurityTool empowers developers and security professionals to enhance their web application's security and identify vulnerabilities with minimal effort.",
    author="Ahmad_Bulbul",
    author_email="Ahmadbulbulprof1@gmail.com",
    url="https://github.com/ZoroHacker/CyberSecurityTools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    long_description=description,
    long_description_content_type="text/markdown",
)
