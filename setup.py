from setuptools import setup, find_packages

setup(
    name='pygame-cv',
    author="Tanguy Dugas du Villard",
    author_mail="tanguy.dugas01@gmail.com",
    version='1.0.0',
    description="PygameCV module is a set of functions helping game developpers using pygame to apply some transformations on their surfaces using CV.",
    packages=find_packages(),
    install_requires=[
        'pygame',
        'numpy',
        'opencv-python'
    ],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Tanguy-ddv/pygameCV",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: pygame"
        "Topic :: Games/Entertainment"
    ],
    python_requires='>=3.6'
)