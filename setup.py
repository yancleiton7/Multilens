from setuptools import find_packages, setup


def read(filename: str) -> list:
    with open(filename, "r", encoding="utf-8") as file:
        return [f.strip("\n") for f in file.readlines()]


setup(
    name="multilens",
    version="0.1.0",
    description="Site para controle de clientes e estoque da multilens",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read("requirements.txt"),
    extras_require={"dev": read("requirements-dev.txt")},
)
