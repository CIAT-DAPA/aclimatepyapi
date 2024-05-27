from setuptools import setup, find_packages

setup(
    name="aclimate_api",
    version="0.1",
    author="Minotriz02",
    author_email="sebastian.lopez@cgiar.org",
    description="API for the AClimate project",
    url="https://github.com/CIAT-DAPA/aclimatepyapi",
    download_url="https://github.com/CIAT-DAPA/aclimatepyapi",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords=["aclimate", "api", "climate", "agriculture"],
)