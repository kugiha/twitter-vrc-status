from setuptools import setup

setup(
    name="vrchat-api",
    version="0.1.0",
    description="An unofficial Python library for the VRChat API",
    url="https://github.com/y23586/vrchat-api-python",
    author="y23586",
    license="MIT",
    packages=["vrchat_api"],
    install_requires=["requests>=2.21.0"]
)
