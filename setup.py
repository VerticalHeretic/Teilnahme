from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

print(requirements)

setup(
    name="teilnahme",
    version="0.0.2",
    author="Łukasz Stachnik",
    author_email="lukasz.marek.stachnik@gmail.com",
    description="Attendance management system for university",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/VerticalHeretic/Teilnahme",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": ["teilnahme=src.cli.cli:main"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
