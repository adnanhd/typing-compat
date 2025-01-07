import os
import re
from setuptools import find_packages, setup

# Helper functions for setup

def read_file(filepath: str) -> str:
    """Read and return the content of a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip()

def get_dependencies() -> list:
    """Retrieve dependencies from the requirements file."""
    depfile = "requirements.txt"
    if os.path.exists(depfile):
        return [line.strip() for line in read_file(depfile).splitlines() if line.strip()]
    return []

def get_package_name() -> str:
    """Retrieve the package name from the project directory structure."""
    packages = find_packages()
    if packages:
        return packages[0]
    raise RuntimeError("No package found. Ensure your project contains a valid Python package.")
 
def get_version() -> str:
    """Retrieve the package version from the version file."""
    package = get_package_name()
    versionfile = os.path.join(package, "_version.py")

    if os.path.exists(versionfile):
        verstrline = read_file(versionfile)
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", verstrline, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string in '_version.py'.")

    raise FileNotFoundError("Version file '_version.py' not found.")
# 
# # Metadata constants (replace these with actual values)
# AUTHOR = "Your Name"
# DESCRIPTION = "A short description of your package."
# GITID = "your-github-username"
# 
setup(version=get_version())

# # Setup function
# setup(
#     name=get_package_name(),
#     version=get_version(),
#     author=AUTHOR,
#     author_email="your-email@example.com",  # Add email field
#     url=f"https://github.com/{GITID}/{get_package_name()}",
#     description=DESCRIPTION,
#     long_description=read_file("README.md"),
#     long_description_content_type="text/markdown",
#     packages=find_packages(exclude=("docs", "tests*")),
#     include_package_data=True,
#     install_requires=get_dependencies(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires=">=3.7",
# )
