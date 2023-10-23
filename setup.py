from setuptools import setup
from setuptools import find_packages


VERSION = "1.0.0"

with open('README.md', "r") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='CawBus',
    author='fakerick',
    author_email='rick@guaik.io',
    version=VERSION,
    description='Robot Communication Bus',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    project_urls={
        "Documentation": "https://caw.guaik.io/",
        "Code": "https://github.com/fake-rick/caw-bus-python",
        "Issue tracker": "https://github.com/fake-rick/caw-bus-python/issues",
    },
    python_requires=">=3.7",
    install_requires=[
        "pyserial>=3.5",
        "python-can>=4.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    zip_safe=False,
)