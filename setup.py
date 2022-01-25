from setuptools import setup, find_packages

with open("README.md", "r", encoding = "UTF-8") as file:
    long_desc = file.read()
 
setup(
    name = "aerics",
    version = "0.0.1",
    description = "A networking library for multiplayer games.",
    long_description = long_desc,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Aermoss/Aerics",
    author = "Yusuf Rencber",
    author_email = "yusufrencber546@gmail.com",
    license = "MIT",
    keywords = "",
    packages = find_packages(),
    include_package_data = True,
    install_requires = []
)