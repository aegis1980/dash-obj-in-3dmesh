"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from os import path

HERE = path.dirname(path.abspath(__file__))

GITHUB_URL = "https://github.com/aegis1980/dash-obj-in-3dmesh/"

def _get_long_description():
    """
    Get the long description from the README file
    """
    with open(path.join(HERE, "README.md")) as f:
        return f.read()


setup(
    name='dash-obj-in-3dmesh',
    version='0.3.1',
    description='Some tools for getting Wavefront OBJ files into a Plotly Dash 3dmesh graph',
    long_description=_get_long_description(),
    long_description_content_type='text/markdown', 
    author='Jon Robinson',
    author_email='jonrobinson1980@gmail.com',
    license='CC Attribution 4.0 International',
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'numpy', 
        'dash',
        'multimethod'
    ], #external packages as dependencies
    classifiers=[
        "Framework :: Dash"
    ]
)