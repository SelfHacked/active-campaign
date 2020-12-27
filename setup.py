import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    version="1.0.0",
    name="active-campaign",
    packages=["active_campaign"],
    long_description=long_description,
    long_description_content_type="text/markdown",

)
