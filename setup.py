from setuptools import setup, find_packages

setup(
    name="distvsprice",
    version="0.1",
    packages=find_packages(include=["datasets", "gerarlink", "distancia", "datasets.*", "gerarlink.*", "distancia.*"]),
    install_requires=[],
)
