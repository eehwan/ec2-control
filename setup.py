from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("ec2ctl/__init__.py", "r") as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split("=")[1].strip().strip("'")
            break

setup(
    name='ec2ctl',
    version=version,
    packages=find_packages(where='ec2ctl'),
    include_package_data=True,
    install_requires=[
        'click',
        'boto3',
        'PyYAML',
    ],
    entry_points={
        'console_scripts': [
            'ec2ctl = ec2ctl.cli:cli',
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
