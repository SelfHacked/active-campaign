import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="active-campaign-eldano1995",
    version="0.0.1",
    author="Umar Kahn",
    author_email="umar@selfdecode.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SelfHacked/active-campaign",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
