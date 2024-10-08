import pathlib
import setuptools

setuptools.setup(
    name="intentclassification",
    version="0.1.1",
    description="Intentclassification AI in python, easy to use intentclassifier package.",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="zhiftyDK",
    author_email="juulstausholmoscar@gmail.com",
    license="The Unlicense",
    project_urls={
        "Source": "https://github.com/zhiftyDK/intentclassification",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    install_requires=["nltk", "numpy", "tensorflow"],
    packages=setuptools.find_packages(),
    include_package_data=True,
)