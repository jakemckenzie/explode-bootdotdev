from setuptools import setup, find_packages

setup(
    name="explode-bootdotdev",
    version="0.0.1",
    description="a project to show off my skills issues generating a site that blows up bootdotdev",
    author="Jake McKenzie",
    author_email="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},   # Tells Python to look for packages in the src directory
    install_requires=[
        "setuptools==78.1.0"
    ],
)
