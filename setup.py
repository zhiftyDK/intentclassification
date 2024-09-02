from setuptools import setup, find_packages

VERSION = "0.0.2"
DESCRIPTION = "A package that allows to build simple streams of video, audio and camera data."

# Setting up
setup(
    name="intentclassification",
    version=VERSION,
    author="zhiftyDK",
    author_email="<juulstausholmoscar@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["tensorflow", "nltk", "numpy"],
    keywords=["python", "ai", "intentclassification", "classification", "keyworddetection", "trigger"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)